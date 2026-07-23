# PD

Front-matter OCR for *An Encyclopaedic Dictionary of Sanskrit on Historical Principles*
(Deccan College / KoshaSHRI).

_Created: 23-07-2026 · Last updated: 23-07-2026_

## Sources → Markdown

| PDF | Pages | Content | Output |
|-----|------:|---------|--------|
| `GA.pdf` | 2 | General Abbreviations | [`GA.md`](GA.md) |
| `AUB.pdf` | 2 | Abbreviations Used in the Bibliography | [`AUB.md`](AUB.md) |
| `RG.pdf` | 5 | Reader’s Guide | [`RG.md`](RG.md) |
| `SWC.pdf` | 9 | Subject-wise Classification & Chronology | [`SWC.md`](SWC.md) |
| `AOB.pdf` | 42 | Abbreviations of Books Quoted | [`AOB.md`](AOB.md) |

Baselines from the first OCR pass are kept as `*_ocr.md` for diffing.

## Pipeline

```text
python run_ocr.py                  # all five PDFs
python run_ocr.py --only GA.pdf    # one file
python run_ocr.py --only AOB.pdf --start-page 20   # resume AOB from page 21
```

**Requirements:** Python 3, Tesseract 5.x with `eng` + `san` traineddata, plus:

```text
pymupdf  pillow  pytesseract  numpy  beautifulsoup4
```

### v2 features (`run_ocr.py`)

1. **Crop-then-OCR** per column strip (not full-page OCR + post-split)
2. **Layout modes**
   - `multi_pair` — key \| expansion tables (GA, AUB); format `` `Abl.` Ablative ``
   - `multi_seq` — Abbreviation \| Title \| Mode (AOB); format `` `Abbr.` Title — Mode ``
   - `prose_2col` — left column then right (RG, SWC)
3. **Italics** from native PDF Times-Italic spans; skew heuristic only as fallback; stopwords banned
4. **Provenance header** + `## Page N` markers
5. **Resume** via `--start-page` / `--end-page`

PDFs are image scans with a partial native text layer (Latin + italics; Devanāgarī is mojibake in the layer). Tesseract `eng+san` supplies Unicode Devanāgarī.

## About the dictionary

See [`about.md`](about.md) and [`aboutDictionary.md`](aboutDictionary.md) (KoshaSHRI / Deccan College).

---

_Dr. Mārcis Gasūns_
