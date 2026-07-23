"""
OCR pipeline v2 for Deccan College Encyclopaedic Dictionary front-matter PDFs.

Improvements over v1:
1. Crop-then-OCR per column (not full-page OCR + post-split)
2. Layout modes: single | prose_2col | multi_pair (abbrev | expansion)
3. Italics from native PDF Times-Italic spans (primary) + skew heuristic
4. Stopword italic ban; noise filtering
5. Provenance header + ## Page N markers
6. Resume support for long PDFs (--start-page / --only)
"""
from __future__ import annotations

import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import argparse
import os
import re
from datetime import date
from typing import List, Optional, Sequence, Tuple

import fitz
import numpy as np
import pytesseract
from bs4 import BeautifulSoup
from PIL import Image

BBox = Tuple[int, int, int, int]
Word = Tuple[str, BBox]  # text, (x0,y0,x1,y1) in image coords

DPI = 300
TESS_LANG = "eng+san"
TESS_PSM_BLOCK = r"--psm 6 -c preserve_interword_spaces=1"
TESS_PSM_SPARSE = r"--psm 4 -c preserve_interword_spaces=1"

# Words that must never be italicized (common FP from skew heuristic)
ITALIC_STOPWORDS = frozenset(
    w.lower()
    for w in """
    of and are or the to in a an for as on by with from is was were be been
    that this these those it its at not no nor but if then than so such
    e g etc etc. i ii iii iv v vi vii viii ix x xi xii xiii xiv xv xvi
    page pages vol vols note notes see also
    """.split()
)

NOISE_WORDS = re.compile(
    r'^[~`|*।॥\-_=+^°©"\',.;:!?@#$%&(){}\[\]<>/\\]+$'
)

# High-confidence whole-token OCR confusions (conservative)
IAST_TOKEN_MAP = {
    "Ace,": "Acc.",
    "Ace.": "Acc.",
    "ane,": "anc.",
    "ane.": "anc.",
    "ani.": "ani.",
    "By.": "Bv.",
    "foaryt.": "baryt.",
    "«comin.": "comm.",
    "comin.": "comm.",
    "AustroAs.": "AustroAs.",
    "AustroAs,": "AustroAs.",
    "aluCpd.": "alukCpd.",
    "aluCpd,": "alukCpd.",
    "appelative": "appellative",
    "Dramaturey": "Dramaturgy",
    "noetronymic": "metronymic",
    "foot-onte": "foot-note",
    "Sveq:": "freq.",
    "Jutp.": "futp.",
    "Adverhbs,.": "Adverbs,",
    "Adverhbs,": "Adverbs,",
    "indentical": "identical",
    "parasararna": "parasarṇa",
    "coihpound": "compound",
    "Bahuvrlhi": "Bahuvrīhi",
    "ripackas": "rūpakas",
}


# ---------------------------------------------------------------------------
# Noise / post
# ---------------------------------------------------------------------------
def is_noise(word: str) -> bool:
    if not word or not word.strip():
        return True
    w = word.strip()
    if NOISE_WORDS.match(w):
        return True
    if len(w) == 1 and w not in "IAaOo":
        return True
    # Isolated pure-digit junk that is not a list number like "1." / "27"
    if re.fullmatch(r"\d{4,}", w):
        return True
    return False


def clean_token(word: str) -> str:
    w = word.strip()
    if w in IAST_TOKEN_MAP:
        return IAST_TOKEN_MAP[w]
    return w


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------
def page_scale(page: fitz.Page) -> float:
    """PDF points → image pixels at DPI."""
    return DPI / 72.0


def native_words_image_coords(page: fitz.Page) -> List[Word]:
    """Extract native PDF words mapped into 300-dpi image coordinates."""
    s = page_scale(page)
    out: List[Word] = []
    for x0, y0, x1, y1, text, *_ in page.get_text("words"):
        if not text or not text.strip():
            continue
        bbox = (int(x0 * s), int(y0 * s), int(x1 * s), int(y1 * s))
        out.append((text, bbox))
    return out


def native_italic_spans_image_coords(page: fitz.Page) -> List[BBox]:
    """Bboxes of italic spans from native PDF font flags / name."""
    s = page_scale(page)
    italic_boxes: List[BBox] = []
    for block in page.get_text("dict").get("blocks", []):
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text") or ""
                if not text.strip():
                    continue
                font = (span.get("font") or "").lower()
                flags = span.get("flags", 0)
                is_it = bool(flags & 2) or "italic" in font or "oblique" in font
                if not is_it:
                    continue
                x0, y0, x1, y1 = span["bbox"]
                italic_boxes.append(
                    (int(x0 * s), int(y0 * s), int(x1 * s), int(y1 * s))
                )
    return italic_boxes


def bbox_iou(a: BBox, b: BBox) -> float:
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    ix0, iy0 = max(ax0, bx0), max(ay0, by0)
    ix1, iy1 = min(ax1, bx1), min(ay1, by1)
    iw, ih = max(0, ix1 - ix0), max(0, iy1 - iy0)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    area_a = max(1, (ax1 - ax0) * (ay1 - ay0))
    area_b = max(1, (bx1 - bx0) * (by1 - by0))
    return inter / float(min(area_a, area_b))


def word_hits_italic(bbox: BBox, italic_boxes: Sequence[BBox], thr: float = 0.25) -> bool:
    return any(bbox_iou(bbox, ib) >= thr for ib in italic_boxes)


# ---------------------------------------------------------------------------
# Italic skew heuristic (fallback)
# ---------------------------------------------------------------------------
def is_italic_skew(img_np: np.ndarray, bbox: BBox, margin: int = 2) -> bool:
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
    if rh < 10 or rw < 12:
        return False
    gray = (
        np.mean(region, axis=2).astype(float)
        if len(region.shape) == 3
        else region.astype(float)
    )
    inv = 255.0 - gray
    maxval = inv.max()
    if maxval < 30:
        return False
    binary = (inv > maxval * 0.45).astype(float)
    top_half = binary[: rh // 2, :]
    bot_half = binary[rh // 2 :, :]

    def col_center(half: np.ndarray) -> float:
        col_sum = half.sum(axis=0)
        total = col_sum.sum()
        if total < 8:
            return rw / 2.0
        return float(np.dot(col_sum, np.arange(rw)) / total)

    shift = (col_center(top_half) - col_center(bot_half)) / max(rw, 1)
    return shift > 0.09


def should_italic(
    word: str,
    bbox: BBox,
    img_np: np.ndarray,
    italic_boxes: Sequence[BBox],
) -> bool:
    bare = re.sub(r"^[^\w\u0900-\u097F]+|[^\w\u0900-\u097F]+$", "", word)
    if not bare or len(bare) <= 2:
        return False
    if bare.lower() in ITALIC_STOPWORDS:
        return False
    if bare.isdigit():
        return False
    if word_hits_italic(bbox, italic_boxes):
        return True
    # Skew only for longer Latin words (Devanāgarī skew is unreliable)
    if re.search(r"[\u0900-\u097F]", word):
        return False
    if len(bare) < 5:
        return False
    return is_italic_skew(img_np, bbox)


# ---------------------------------------------------------------------------
# Column detection
# ---------------------------------------------------------------------------
def _column_centers(words: Sequence[Word], page_width: int, max_cols: int = 6) -> List[float]:
    """Peak-pick word x-centers into up to max_cols column centroids."""
    if not words or page_width <= 0:
        return []
    x_centers = np.array([(b[0] + b[2]) / 2.0 for _, b in words], dtype=float)
    hist, edges = np.histogram(x_centers, bins=80, range=(0, page_width))
    smooth = np.convolve(hist.astype(float), np.ones(3) / 3.0, mode="same")

    peaks: List[Tuple[float, float]] = []
    for i in range(1, len(smooth) - 1):
        if smooth[i] >= smooth[i - 1] and smooth[i] > smooth[i + 1] and smooth[i] >= 2.5:
            cx = (edges[i] + edges[i + 1]) / 2.0
            if page_width * 0.04 < cx < page_width * 0.96:
                peaks.append((float(smooth[i]), float(cx)))
    if not peaks:
        return []
    peaks.sort(key=lambda p: -p[0])
    min_sep = page_width * 0.055
    chosen: List[float] = []
    for _, cx in peaks:
        if len(chosen) >= max_cols:
            break
        if all(abs(cx - c) > min_sep for c in chosen):
            chosen.append(cx)
    return sorted(chosen)


def is_abbr_table(title_hint: str) -> bool:
    """True for key|expansion abbreviation bibliographies (not subject lists)."""
    hint = title_hint.lower()
    return any(
        k in hint
        for k in (
            "abbreviation",
            "abbrev",
            "general abbreviations",
            "books quoted",
            "mode of reference",
            "abbreviations used",
            "abbreviations of books",
        )
    )


def is_triple_abbr(title_hint: str) -> bool:
    """True for Abbreviation | Title | Mode-of-reference tables (AOB-style)."""
    hint = title_hint.lower()
    return any(
        k in hint
        for k in ("books quoted", "mode of reference", "name of the book")
    )


def detect_column_splits(
    words: Sequence[Word],
    page_width: int,
    layout_hint: str = "auto",
) -> Tuple[List[int], str]:
    """
    Return (gutter_xs, layout_mode).

    layout_hint: 'auto' | 'multi_pair' | 'prose_2col' | 'single'
    - multi_pair: keep all key|exp gutters (up to 5)
    - prose_2col / auto: keep only the single widest major gutter
    """
    centers = _column_centers(words, page_width, max_cols=6)
    if len(centers) < 2:
        return [], "single"

    gaps: List[Tuple[float, int]] = []  # (gap_width, midpoint_x)
    for i in range(len(centers) - 1):
        gap = centers[i + 1] - centers[i]
        mid = int((centers[i] + centers[i + 1]) / 2)
        gaps.append((gap, mid))

    if layout_hint in ("multi_pair", "multi_seq"):
        gap_widths = [g[0] for g in gaps]
        median_gap = float(np.median(gap_widths)) if gap_widths else 0.0
        major_mids = sorted(
            m
            for w, m in gaps
            if w >= max(median_gap * 1.35, page_width * 0.11)
        )
        if not major_mids:
            major_mids = [max(gaps, key=lambda g: g[0])[1]]

        # AOB-style triple: Abbreviation | Book title | Mode of reference
        if layout_hint == "multi_seq":
            # Prefer exactly two major gutters → 3 columns
            if len(major_mids) >= 2:
                # take the two largest major gaps
                maj_sorted = sorted(
                    [(w, m) for w, m in gaps if m in major_mids],
                    key=lambda g: -g[0],
                )
                splits = sorted(m for _, m in maj_sorted[:2])
            else:
                # tertile fallback
                splits = [int(page_width * 0.28), int(page_width * 0.78)]
            return splits, "multi_seq"

        # Pair-blocks (GA 3× pair, AUB 2× pair)
        block_bounds = [0] + major_mids + [page_width]
        splits = list(major_mids)
        for i in range(len(block_bounds) - 1):
            lo, hi = block_bounds[i], block_bounds[i + 1]
            block_centers = [c for c in centers if lo < c < hi]
            if len(block_centers) >= 2:
                splits.append(int((block_centers[0] + block_centers[1]) / 2))
            else:
                splits.append(int(lo + (hi - lo) * 0.28))
        # drop splits that create a near-empty edge strip (< 5% page width)
        splits = sorted(set(splits))
        filtered = []
        prev = 0
        for s in splits + [page_width]:
            if s - prev >= page_width * 0.06:
                if s < page_width:
                    filtered.append(s)
                prev = s
            # else skip this split (too narrow strip)
        return filtered, "multi_pair"

    # Prose / subject lists / auto: single widest gutter → 2 columns
    widest = max(gaps, key=lambda g: g[0])[1]
    if page_width * 0.20 < widest < page_width * 0.80:
        return [widest], "prose_2col"
    return [], "single"


# ---------------------------------------------------------------------------
# hOCR parse
# ---------------------------------------------------------------------------
def parse_hocr_words(hocr_str: str, x_offset: int = 0, y_offset: int = 0) -> List[Word]:
    soup = BeautifulSoup(hocr_str, "html.parser")
    words: List[Word] = []
    for elem in soup.find_all(class_="ocrx_word"):
        text = elem.get_text(strip=True)
        if not text:
            continue
        m = re.search(r"bbox (\d+) (\d+) (\d+) (\d+)", elem.get("title", ""))
        if not m:
            continue
        x0, y0, x1, y1 = (int(v) for v in m.groups())
        words.append(
            (text, (x0 + x_offset, y0 + y_offset, x1 + x_offset, y1 + y_offset))
        )
    return words


def ocr_crop(
    img: Image.Image,
    crop_box: Tuple[int, int, int, int],
    config: str = TESS_PSM_BLOCK,
) -> List[Word]:
    """OCR a crop; return words with bboxes in full-page image coords."""
    x0, y0, x1, y1 = crop_box
    # pad slightly into gutter so edge glyphs aren't clipped
    pad = 4
    cx0 = max(0, x0 - pad)
    cy0 = max(0, y0 - pad)
    cx1 = min(img.width, x1 + pad)
    cy1 = min(img.height, y1 + pad)
    if cx1 - cx0 < 20 or cy1 - cy0 < 20:
        return []
    crop = img.crop((cx0, cy0, cx1, cy1))
    try:
        hocr = pytesseract.image_to_pdf_or_hocr(
            crop, lang=TESS_LANG, extension="hocr", config=config
        )
    except Exception as e:
        print(f"    OCR error on crop {crop_box}: {e}")
        return []
    return parse_hocr_words(hocr.decode("utf-8"), x_offset=cx0, y_offset=cy0)


# ---------------------------------------------------------------------------
# Line reconstruction
# ---------------------------------------------------------------------------
def group_lines(words: Sequence[Word], line_tol: int = 12) -> List[List[Word]]:
    if not words:
        return []
    words_sorted = sorted(words, key=lambda w: (w[1][1] + w[1][3]) / 2)
    lines: List[List[Word]] = []
    current: List[Word] = []
    cur_y = (words_sorted[0][1][1] + words_sorted[0][1][3]) / 2
    for word, bbox in words_sorted:
        wy = (bbox[1] + bbox[3]) / 2
        if abs(wy - cur_y) > line_tol:
            if current:
                lines.append(current)
            current = []
            cur_y = wy
        current.append((word, bbox))
    if current:
        lines.append(current)
    return lines


def format_token(
    word: str,
    bbox: BBox,
    img_np: np.ndarray,
    italic_boxes: Sequence[BBox],
) -> Optional[str]:
    if is_noise(word):
        return None
    w = clean_token(word)
    if is_noise(w):
        return None
    if should_italic(w, bbox, img_np, italic_boxes):
        return f"*{w}*"
    return w


def words_to_md_lines(
    words: Sequence[Word],
    img_np: np.ndarray,
    italic_boxes: Sequence[BBox],
    line_tol: int = 12,
) -> List[str]:
    md: List[str] = []
    for line in group_lines(words, line_tol=line_tol):
        line_sorted = sorted(line, key=lambda w: w[1][0])
        tokens = []
        for word, bbox in line_sorted:
            tok = format_token(word, bbox, img_np, italic_boxes)
            if tok:
                tokens.append(tok)
        if tokens:
            md.append(" ".join(tokens))
    return md


def _line_y(line: Sequence[Word]) -> float:
    return sum((b[1] + b[3]) / 2 for _, b in line) / max(len(line), 1)


def _line_text(
    line: Sequence[Word],
    img_np: np.ndarray,
    italic_boxes: Sequence[BBox],
) -> str:
    toks = []
    for word, bbox in sorted(line, key=lambda w: w[1][0]):
        tok = format_token(word, bbox, img_np, italic_boxes)
        if tok:
            toks.append(tok)
    return " ".join(toks)


def _match_line(
    target_y: float,
    candidates: Sequence[List[Word]],
    used: set,
    y_tol: int,
) -> Optional[int]:
    best_j = None
    best_dy = y_tol + 1
    for j, line in enumerate(candidates):
        if j in used:
            continue
        dy = abs(_line_y(line) - target_y)
        if dy < best_dy:
            best_dy = dy
            best_j = j
    if best_j is not None and best_dy <= y_tol:
        return best_j
    return None


def pair_columns_by_y(
    left: Sequence[Word],
    right: Sequence[Word],
    img_np: np.ndarray,
    italic_boxes: Sequence[BBox],
    y_tol: int = 14,
) -> List[str]:
    """
    Pair left-column tokens with right-column tokens on the same baseline.
    Format (approved option a): `Abl.` Ablative
    """
    left_lines = group_lines(left, line_tol=y_tol)
    right_lines = group_lines(right, line_tol=y_tol)
    right_used: set = set()
    out: List[str] = []

    for ll in left_lines:
        ly = _line_y(ll)
        ltxt = _line_text(ll, img_np, italic_boxes)
        if not ltxt:
            continue
        j = _match_line(ly, right_lines, right_used, y_tol)
        if j is not None:
            right_used.add(j)
            rtxt = _line_text(right_lines[j], img_np, italic_boxes)
            if rtxt:
                bare_key = re.sub(r"^\*|\*$", "", ltxt)
                out.append(f"`{bare_key}` {rtxt}")
            else:
                out.append(ltxt)
        else:
            out.append(ltxt)

    for j, rl in enumerate(right_lines):
        if j in right_used:
            continue
        rtxt = _line_text(rl, img_np, italic_boxes)
        if rtxt:
            out.append(rtxt)
    return out


def triple_columns_by_y(
    left: Sequence[Word],
    mid: Sequence[Word],
    right: Sequence[Word],
    img_np: np.ndarray,
    italic_boxes: Sequence[BBox],
    y_tol: int = 16,
) -> List[str]:
    """AOB-style: `Abbr.` Book title — Mode of reference."""
    left_lines = group_lines(left, line_tol=y_tol)
    mid_lines = group_lines(mid, line_tol=y_tol)
    right_lines = group_lines(right, line_tol=y_tol)
    mid_used: set = set()
    right_used: set = set()
    out: List[str] = []

    for ll in left_lines:
        ly = _line_y(ll)
        ltxt = _line_text(ll, img_np, italic_boxes)
        if not ltxt:
            continue
        # skip header-only rows
        if ltxt.lower().replace("*", "") in (
            "abbreviation",
            "abbreviations",
            "name",
            "mode",
        ):
            continue
        bare_key = re.sub(r"^\*|\*$", "", ltxt)
        mj = _match_line(ly, mid_lines, mid_used, y_tol)
        rj = _match_line(ly, right_lines, right_used, y_tol)
        mtxt = _line_text(mid_lines[mj], img_np, italic_boxes) if mj is not None else ""
        rtxt = _line_text(right_lines[rj], img_np, italic_boxes) if rj is not None else ""
        if mj is not None:
            mid_used.add(mj)
        if rj is not None:
            right_used.add(rj)
        if mtxt and rtxt:
            out.append(f"`{bare_key}` {mtxt} — {rtxt}")
        elif mtxt:
            out.append(f"`{bare_key}` {mtxt}")
        elif rtxt:
            out.append(f"`{bare_key}` — {rtxt}")
        else:
            out.append(f"`{bare_key}`")
    return out


# ---------------------------------------------------------------------------
# Page → markdown
# ---------------------------------------------------------------------------
def page_title_hint(page: fitz.Page) -> str:
    """Rough title from top of native text for layout classification."""
    blocks = page.get_text("blocks")
    tops = sorted(blocks, key=lambda b: b[1])[:6]
    return " ".join((b[4] or "") for b in tops)[:200]


def process_page(
    page: fitz.Page,
    img: Image.Image,
    force_layout: Optional[str] = None,
) -> Tuple[str, str, int]:
    """
    Returns (markdown, layout_mode, word_count).
    force_layout: optional 'multi_pair' | 'multi_seq' | 'prose_2col' | 'single'
    """
    img_np = np.array(img)
    page_w, page_h = img.width, img.height

    # Geometry from native words when available; else full-page OCR for splits only
    native = native_words_image_coords(page)
    italic_boxes = native_italic_spans_image_coords(page)
    hint = page_title_hint(page)

    probe_words = native
    if len(probe_words) < 15:
        # Fall back: cheap full-page OCR just for column detection
        probe_words = ocr_crop(img, (0, 0, page_w, page_h), config=TESS_PSM_SPARSE)

    if force_layout:
        layout_hint = force_layout
    elif is_triple_abbr(hint):
        layout_hint = "multi_seq"
    elif is_abbr_table(hint):
        layout_hint = "multi_pair"
    else:
        layout_hint = "auto"
    splits, mode = detect_column_splits(probe_words, page_w, layout_hint=layout_hint)

    # Build column boundaries
    if mode == "single" or not splits:
        boundaries = [0, page_w]
        mode = "single"
    else:
        boundaries = [0] + list(splits) + [page_w]

    # OCR each column strip top-to-bottom
    col_words: List[List[Word]] = []
    for i in range(len(boundaries) - 1):
        lo, hi = boundaries[i], boundaries[i + 1]
        if hi - lo < 30:
            col_words.append([])
            continue
        strip_words = ocr_crop(img, (lo, 0, hi, page_h), config=TESS_PSM_BLOCK)
        col_words.append(strip_words)

    # Drop empty columns (failed crops / bad splits)
    col_words = [c for c in col_words if c]
    total_words = sum(len(c) for c in col_words)

    if mode == "single" or len(col_words) <= 1:
        md_lines = words_to_md_lines(col_words[0] if col_words else [], img_np, italic_boxes)
        mode = "single" if len(col_words) <= 1 else mode
    elif mode == "multi_seq" and len(col_words) >= 3:
        md_lines = triple_columns_by_y(
            col_words[0], col_words[1], col_words[2], img_np, italic_boxes
        )
    elif mode == "prose_2col":
        md_lines = []
        for cw in col_words:
            part = words_to_md_lines(cw, img_np, italic_boxes)
            if part:
                if md_lines:
                    md_lines.append("")
                md_lines.extend(part)
    elif mode == "multi_seq" and len(col_words) == 2:
        md_lines = pair_columns_by_y(col_words[0], col_words[1], img_np, italic_boxes)
    else:
        # multi_pair: pair adjacent columns (0-1), (2-3), (4-5), …
        md_lines = []
        i = 0
        while i < len(col_words):
            if i + 1 < len(col_words):
                paired = pair_columns_by_y(
                    col_words[i], col_words[i + 1], img_np, italic_boxes
                )
                if paired:
                    if md_lines:
                        md_lines.append("")
                    md_lines.extend(paired)
                i += 2
            else:
                leftover = words_to_md_lines(col_words[i], img_np, italic_boxes)
                if leftover:
                    if md_lines:
                        md_lines.append("")
                    md_lines.extend(leftover)
                i += 1

    return "\n".join(md_lines), mode, total_words


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
DEFAULT_PDFS = ["GA.pdf", "AUB.pdf", "RG.pdf", "SWC.pdf", "AOB.pdf"]


# Force layout by PDF stem when page titles are unreliable mid-document
FORCE_LAYOUT_BY_STEM = {
    "AOB": "multi_seq",   # Abbreviation | Title | Mode of reference throughout
    "GA": "multi_pair",   # General abbreviations 3×(key|exp)
    "AUB": "multi_pair",  # Bibliography abbreviations 2×(key|exp)
}


def process_pdf(
    pdf_file: str,
    start_page: int = 0,
    end_page: Optional[int] = None,
) -> None:
    if not os.path.exists(pdf_file):
        print(f"Skipping {pdf_file}, not found.")
        return

    md_file = pdf_file.replace(".pdf", ".md")
    stem = os.path.splitext(os.path.basename(pdf_file))[0]
    force_layout = FORCE_LAYOUT_BY_STEM.get(stem)
    print(f"Processing {pdf_file} -> {md_file}" + (f" (force={force_layout})" if force_layout else ""))

    doc = fitz.open(pdf_file)
    n_pages = len(doc)
    if end_page is None:
        end_page = n_pages
    end_page = min(end_page, n_pages)
    start_page = max(0, start_page)

    # Load existing page blocks so resume/partial re-runs keep untouched pages
    page_blocks: List[Optional[str]] = [None] * n_pages
    if os.path.exists(md_file):
        existing = open(md_file, encoding="utf-8").read()
        for m in re.finditer(
            r"^## Page (\d+)\s*\n([\s\S]*?)(?=^## Page \d+\s*$|\Z)",
            existing,
            flags=re.M,
        ):
            idx = int(m.group(1)) - 1
            if 0 <= idx < n_pages:
                page_blocks[idx] = f"## Page {idx + 1}\n\n{m.group(2).rstrip()}"
        kept = sum(1 for b in page_blocks if b)
        if kept:
            print(f"  Loaded {kept} existing page blocks from {md_file}")

    today = date.today().isoformat()
    header = (
        f"<!-- provenance: engine=tesseract-{pytesseract.get_tesseract_version()} "
        f"{TESS_LANG}; pipeline=run_ocr.py v2; source={pdf_file}; date={today} -->\n"
        f"# {pdf_file}\n"
    )

    for page_num in range(start_page, end_page):
        print(f"  Page {page_num + 1}/{n_pages}...", end=" ", flush=True)
        page = doc[page_num]
        pix = page.get_pixmap(dpi=DPI)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        body, mode, n_words = process_page(page, img, force_layout=force_layout)
        print(f"mode={mode} words={n_words}")
        page_blocks[page_num] = f"## Page {page_num + 1}\n\n{body}".rstrip()

        # Incremental save for long runs
        if (page_num + 1) % 5 == 0 or page_num + 1 == end_page:
            present = [b for b in page_blocks if b]
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(header + "\n" + "\n\n".join(present) + "\n")

    present = [b for b in page_blocks if b]
    missing = [i + 1 for i, b in enumerate(page_blocks) if not b]
    if missing:
        print(f"  WARNING: missing pages {missing[:20]}{'...' if len(missing) > 20 else ''}")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(header + "\n" + "\n\n".join(present) + "\n")
    print(f"  Done: {md_file} ({len(present)}/{n_pages} pages)")


def main() -> None:
    ap = argparse.ArgumentParser(description="PD preface OCR v2")
    ap.add_argument(
        "--only",
        nargs="*",
        help="Process only these PDFs (e.g. GA.pdf RG.pdf)",
    )
    ap.add_argument("--start-page", type=int, default=0, help="0-based start page")
    ap.add_argument("--end-page", type=int, default=None, help="0-based exclusive end")
    args = ap.parse_args()

    pdfs = args.only if args.only else DEFAULT_PDFS
    for pdf in pdfs:
        if not pdf.lower().endswith(".pdf"):
            pdf = pdf + ".pdf" if not pdf.endswith(".pdf") else pdf
        # allow bare stems
        if not os.path.exists(pdf) and os.path.exists(pdf.replace(".pdf", "") + ".pdf"):
            pdf = pdf.replace(".pdf", "") + ".pdf"
        if not pdf.endswith(".pdf"):
            pdf = pdf + ".pdf"
        try:
            process_pdf(pdf, start_page=args.start_page, end_page=args.end_page)
        except Exception as e:
            print(f"  ERROR on {pdf}: {e}")
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    main()
