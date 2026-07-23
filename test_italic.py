import sys
sys.stdout.reconfigure(encoding='utf-8')
import fitz, pytesseract, numpy as np, re
from PIL import Image
from bs4 import BeautifulSoup

doc = fitz.open('GA.pdf')
page = doc[0]
pix = page.get_pixmap(dpi=300)
img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
img_np = np.array(img)

hocr_bytes = pytesseract.image_to_pdf_or_hocr(img, lang='eng+san', extension='hocr', config='--psm 6')
hocr_str = hocr_bytes.decode('utf-8')
soup = BeautifulSoup(hocr_str, 'html.parser')

count = 0
for word_elem in soup.find_all(class_='ocrx_word'):
    text = word_elem.get_text(strip=True)
    if not text:
        continue
    title = word_elem.get('title', '')
    m = re.search(r'bbox (\d+) (\d+) (\d+) (\d+)', title)
    if m:
        x0, y0, x1, y1 = [int(v) for v in m.groups()]
        region = img_np[max(0,y0-2):y1+2, max(0,x0-2):x1+2]
        gray = np.mean(region, axis=2) if len(region.shape)==3 else region.astype(float)
        inv = 255.0 - gray
        maxval = inv.max()
        if maxval == 0:
            italic = False
        else:
            binary = (inv > maxval*0.5).astype(float)
            h, w = binary.shape
            if h >= 4 and w >= 4:
                top_sum = binary[:h//2, :].sum()
                bot_sum = binary[h//2:, :].sum()
                top_cx = np.dot(binary[:h//2,:].sum(axis=0), np.arange(w)) / max(top_sum, 1)
                bot_cx = np.dot(binary[h//2:,:].sum(axis=0), np.arange(w)) / max(bot_sum, 1)
                shift = (top_cx - bot_cx) / max(w, 1)
                italic = shift > 0.05
            else:
                italic = False

        label = "ITALIC" if italic else "      "
        print(repr(text) + " -> " + label)
        count += 1
        if count >= 40:
            break
