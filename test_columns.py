import sys
sys.stdout.reconfigure(encoding='utf-8')

import fitz, pytesseract, numpy as np, re
from PIL import Image
from bs4 import BeautifulSoup

# --- inline the functions from run_ocr.py for quick test ---
NOISE_WORDS = re.compile(r'^[~`|*।॥\-_=+^°©"\',.;:!?@#$%&(){}\[\]<>/\\]+$')

def is_noise(word):
    if not word or not word.strip(): return True
    w = word.strip()
    if NOISE_WORDS.match(w): return True
    if len(w) == 1 and w not in 'IAa': return True
    return False

def is_italic(img_np, bbox, margin=2):
    x0,y0,x1,y1 = bbox
    h_img,w_img = img_np.shape[:2]
    x0,y0,x1,y1 = max(0,x0-margin),max(0,y0-margin),min(w_img,x1+margin),min(h_img,y1+margin)
    region = img_np[y0:y1,x0:x1]
    if region.size == 0: return False
    rh,rw = region.shape[:2]
    if rh < 8 or rw < 8: return False
    gray = np.mean(region,axis=2).astype(float) if len(region.shape)==3 else region.astype(float)
    inv = 255.0 - gray
    if inv.max() < 30: return False
    binary = (inv > inv.max()*0.45).astype(float)
    top,bot = binary[:rh//2,:], binary[rh//2:,:]
    def cx(h):
        s=h.sum(axis=0); t=s.sum()
        return float(np.dot(s,np.arange(rw))/t) if t>=5 else rw/2.0
    return (cx(top)-cx(bot))/max(rw,1) > 0.07

def detect_column_split(words_data, page_width):
    if not words_data: return None
    x_centers = [(b[0]+b[2])//2 for _,b in words_data]
    hist = [0]*(page_width+1)
    for xc in x_centers: hist[max(0,min(page_width,xc))] += 1
    window=40
    smoothed=[sum(hist[max(0,i-window//2):min(len(hist),i+window//2)]) for i in range(len(hist))]
    mid_lo,mid_hi=int(page_width*0.40),int(page_width*0.60)
    middle=smoothed[mid_lo:mid_hi]
    if not middle: return None
    min_val,max_val=min(middle),max(smoothed)
    if max_val==0 or min_val/max_val>0.05: return None
    return middle.index(min_val)+mid_lo

def parse_hocr_words(hocr_str):
    soup=BeautifulSoup(hocr_str,'html.parser')
    words=[]
    for elem in soup.find_all(class_='ocrx_word'):
        text=elem.get_text(strip=True)
        if not text: continue
        m=re.search(r'bbox (\d+) (\d+) (\d+) (\d+)',elem.get('title',''))
        if m: words.append((text,tuple(int(v) for v in m.groups())))
    return words

def words_to_lines(words, img_np, tol=10):
    if not words: return []
    words_sorted=sorted(words,key=lambda w:(w[1][1]+w[1][3])/2)
    lines,cur=[],[]
    cur_y=(words_sorted[0][1][1]+words_sorted[0][1][3])/2
    for word,bbox in words_sorted:
        wy=(bbox[1]+bbox[3])/2
        if abs(wy-cur_y)>tol:
            lines.append(cur); cur=[]; cur_y=wy
        cur.append((word,bbox))
    if cur: lines.append(cur)
    md=[]
    for line in lines:
        line=sorted(line,key=lambda w:w[1][0])
        tokens=[('*'+w+'*' if is_italic(img_np,b) else w) for w,b in line if not is_noise(w)]
        if tokens: md.append(' '.join(tokens))
    return md

# Test on GA.pdf page 1
doc = fitz.open('GA.pdf')
page = doc[0]
pix = page.get_pixmap(dpi=300)
img = Image.frombytes('RGB',[pix.width,pix.height],pix.samples)
img_np = np.array(img)

hocr_bytes = pytesseract.image_to_pdf_or_hocr(img,lang='eng+san',extension='hocr',config='--psm 1 -c preserve_interword_spaces=1')
hocr_str = hocr_bytes.decode('utf-8')
all_words = parse_hocr_words(hocr_str)

split_x = detect_column_split(all_words, img_np.shape[1])
print(f"Page width: {img_np.shape[1]}, column split at x={split_x}")

if split_x:
    left  = [(t,b) for t,b in all_words if (b[0]+b[2])/2 < split_x]
    right = [(t,b) for t,b in all_words if (b[0]+b[2])/2 >= split_x]
    print("\n=== LEFT COLUMN ===")
    for line in words_to_lines(left,img_np)[:25]: print(line)
    print("\n=== RIGHT COLUMN ===")
    for line in words_to_lines(right,img_np)[:25]: print(line)
else:
    print("Single column detected")
    for line in words_to_lines(all_words,img_np)[:30]: print(line)
