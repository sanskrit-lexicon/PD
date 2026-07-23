import sys
sys.stdout.reconfigure(encoding='utf-8')

"""
Improved Hybrid OCR script for Sanskrit/IAST PDFs.

Improvements over v1:
1. Column detection  - separates 2-column pages and reads each column top-to-bottom
2. Noise filtering   - strips stray scan artifacts (~, `, |, *, lone punctuation)
3. Italic tuning     - raises threshold, skips very short/narrow words
"""
import os
import re
import fitz
import pytesseract
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# Noise filtering
# ---------------------------------------------------------------------------
# Words that are almost certainly scan artifacts
NOISE_WORDS = re.compile(
    r'^[~`|*।॥\-_=+^°©"\',.;:!?@#$%&(){}\[\]<>/\\]+$'
)
# Very short words made entirely of digits or single stray punctuation
NOISE_SHORT = re.compile(r'^[\d\W]{1,2}$')


def is_noise(word):
    """Return True if the word is a scan artifact to be discarded."""
    if not word or not word.strip():
        return True
    w = word.strip()
    if NOISE_WORDS.match(w):
        return True
    # Single characters that are clearly not real content
    if len(w) == 1 and w not in 'IAa':
        return True
    return False


# ---------------------------------------------------------------------------
# Italic detection via horizontal skew analysis
# ---------------------------------------------------------------------------
def is_italic(img_np, bbox, margin=2):
    """
    Detect italic text by measuring horizontal shift of dark-pixel mass
    between the top and bottom halves of the word region.
    Returns True if the word appears italic.
    """
    x0, y0, x1, y1 = bbox
    h_img, w_img = img_np.shape[:2]
    x0 = max(0, x0 - margin)
    y0 = max(0, y0 - margin)
    x1 = min(w_img, x1 + margin)
    y1 = min(h_img, y1 + margin)

    region = img_np[y0:y1, x0:x1]
    if region.size == 0:
        return False
    rh, rw = region.shape[:2]
    # Skip very narrow or short regions (punctuation, single chars) — too noisy
    if rh < 8 or rw < 8:
        return False

    gray = np.mean(region, axis=2).astype(float) if len(region.shape) == 3 else region.astype(float)
    inv = 255.0 - gray
    maxval = inv.max()
    if maxval < 30:   # nearly blank — no text
        return False

    binary = (inv > maxval * 0.45).astype(float)

    top_half = binary[:rh // 2, :]
    bot_half = binary[rh // 2:, :]

    def col_center(half):
        col_sum = half.sum(axis=0)
        total = col_sum.sum()
        if total < 5:   # too few dark pixels — unreliable
            return rw / 2.0
        return float(np.dot(col_sum, np.arange(rw)) / total)

    top_cx = col_center(top_half)
    bot_cx = col_center(bot_half)

    shift = (top_cx - bot_cx) / max(rw, 1)
    # Raised threshold (0.07 instead of 0.05) to reduce false positives
    return shift > 0.07


# ---------------------------------------------------------------------------
# Column detection
# ---------------------------------------------------------------------------
def detect_column_splits(words_data, page_width, max_splits=2):
    """
    Find up to max_splits column separators in the page.
    Returns a sorted list of x-coordinates where columns split.
    Strategy: build a smoothed word-density histogram, then find the deepest
    valleys that represent clear whitespace gutters between columns.
    """
    if not words_data:
        return []

    x_centers = [(b[0] + b[2]) // 2 for _, b in words_data]

    # Build histogram
    hist = [0] * (page_width + 1)
    for xc in x_centers:
        hist[max(0, min(page_width, xc))] += 1

    # Smooth with a 60px window
    window = 60
    smoothed = []
    for i in range(len(hist)):
        lo = max(0, i - window // 2)
        hi = min(len(hist), i + window // 2)
        smoothed.append(sum(hist[lo:hi]))

    max_val = max(smoothed) if smoothed else 0
    if max_val == 0:
        return []

    # Normalise
    norm = [v / max_val for v in smoothed]

    # Find all valleys below 5% of max, ignoring page margins (10-90%)
    margin_lo = int(page_width * 0.10)
    margin_hi = int(page_width * 0.90)

    valleys = []
    in_valley = False
    valley_start = 0
    for i in range(margin_lo, margin_hi):
        if norm[i] <= 0.05:
            if not in_valley:
                in_valley = True
                valley_start = i
        else:
            if in_valley:
                # Record the centre of this valley
                valley_center = (valley_start + i) // 2
                valley_width = i - valley_start
                # Must be at least 30px wide to count as a real column gap
                if valley_width >= 30:
                    valleys.append((norm[valley_center], valley_center))
                in_valley = False
    # Close any open valley at the margin boundary
    if in_valley:
        valley_center = (valley_start + margin_hi) // 2
        valley_width = margin_hi - valley_start
        if valley_width >= 30:
            valleys.append((norm[valley_center], valley_center))

    if not valleys:
        return []

    # Sort by depth (lowest density first), take top max_splits
    valleys.sort(key=lambda v: v[0])
    splits = sorted(v[1] for v in valleys[:max_splits])
    return splits


# ---------------------------------------------------------------------------
# Parse hOCR into a flat list of (text, bbox) pairs
# ---------------------------------------------------------------------------
def parse_hocr_words(hocr_str):
    """Return list of (text, (x0,y0,x1,y1)) for every word in hOCR."""
    soup = BeautifulSoup(hocr_str, 'html.parser')
    words = []
    for elem in soup.find_all(class_='ocrx_word'):
        text = elem.get_text(strip=True)
        if not text:
            continue
        m = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', elem.get('title', ''))
        if m:
            bbox = tuple(int(v) for v in m.groups())
            words.append((text, bbox))
    return words


# ---------------------------------------------------------------------------
# Reconstruct lines from a (possibly filtered) word list
# ---------------------------------------------------------------------------
def words_to_lines(words, img_np, line_tolerance=10):
    """
    Group words into lines by y-coordinate proximity, then sort left-to-right.
    Applies noise filtering and italic detection.
    Returns a list of markdown strings (one per line).
    """
    if not words:
        return []

    # Sort by vertical centre
    words_sorted = sorted(words, key=lambda w: (w[1][1] + w[1][3]) / 2)

    lines = []
    current_line = []
    current_y = (words_sorted[0][1][1] + words_sorted[0][1][3]) / 2

    for word, bbox in words_sorted:
        word_y = (bbox[1] + bbox[3]) / 2
        if abs(word_y - current_y) > line_tolerance:
            lines.append(current_line)
            current_line = []
            current_y = word_y
        current_line.append((word, bbox))
    if current_line:
        lines.append(current_line)

    md_lines = []
    for line in lines:
        # Sort left-to-right within line
        line_sorted = sorted(line, key=lambda w: w[1][0])
        tokens = []
        for word, bbox in line_sorted:
            if is_noise(word):
                continue
            italic = is_italic(img_np, bbox)
            tokens.append(f'*{word}*' if italic else word)
        if tokens:
            md_lines.append(' '.join(tokens))

    return md_lines


# ---------------------------------------------------------------------------
# Process one page image -> markdown string
# ---------------------------------------------------------------------------
def page_to_markdown(img, tess_config):
    img_np = np.array(img)
    page_width = img_np.shape[1]

    hocr_bytes = pytesseract.image_to_pdf_or_hocr(
        img, lang='eng+san', extension='hocr', config=tess_config
    )
    hocr_str = hocr_bytes.decode('utf-8')
    all_words = parse_hocr_words(hocr_str)

    splits = detect_column_splits(all_words, page_width)

    if splits:
        # Build column boundaries: [0, split1, split2, ..., page_width]
        boundaries = [0] + splits + [page_width]
        all_col_lines = []
        for i in range(len(boundaries) - 1):
            lo, hi = boundaries[i], boundaries[i + 1]
            col_words = [(t, b) for t, b in all_words if lo <= (b[0] + b[2]) / 2 < hi]
            col_lines = words_to_lines(col_words, img_np)
            if col_lines:
                all_col_lines.extend(col_lines)
                all_col_lines.append('')  # blank line between columns
        md_lines = all_col_lines
    else:
        md_lines = words_to_lines(all_words, img_np)

    return '\n'.join(md_lines)



# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
pdf_files = ['GA.pdf', 'AUB.pdf', 'RG.pdf', 'SWC.pdf', 'AOB.pdf']

# --psm 1 = automatic page segmentation with OSD (best for mixed layouts)
tess_config = r'--psm 1 -c preserve_interword_spaces=1'

for pdf_file in pdf_files:
    if not os.path.exists(pdf_file):
        print(f"Skipping {pdf_file}, not found.")
        continue

    md_file = pdf_file.replace('.pdf', '.md')
    print(f"Processing {pdf_file} -> {md_file}")

    try:
        doc = fitz.open(pdf_file)
        pages_md = []

        for page_num in range(len(doc)):
            print(f"  Page {page_num + 1}/{len(doc)}...")
            page = doc[page_num]
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)

            page_md = page_to_markdown(img, tess_config)
            pages_md.append(page_md)

        with open(md_file, 'w', encoding='utf-8') as f:
            f.write('\n\n---\n\n'.join(pages_md))

        print(f"  Done: {md_file}")

    except Exception as e:
        print(f"  ERROR on {pdf_file}: {e}")
        import traceback
        traceback.print_exc()
