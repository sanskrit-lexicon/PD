# PD

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23151371.svg)](https://doi.org/10.5281/zenodo.23151371)

Front-matter OCR for *An Encyclopaedic Dictionary of Sanskrit on Historical Principles*
(Deccan College / KoshaSHRI).

_Created: 23-07-2026 · Last updated: 18-10-2026_

## Sources → Markdown

| PDF | Pages | Content | Output |
|-----|------:|---------|--------|
| `GA.pdf` | 2 | General Abbreviations | [`GA.md`](https://github.com/sanskrit-lexicon/PD/blob/main/GA.md) |
| `AUB.pdf` | 2 | Abbreviations Used in the Bibliography | [`AUB.md`](https://github.com/sanskrit-lexicon/PD/blob/main/AUB.md) |
| `RG.pdf` | 5 | Reader’s Guide | [`RG.md`](https://github.com/sanskrit-lexicon/PD/blob/main/RG.md) |
| `SWC.pdf` | 9 | Subject-wise Classification & Chronology | [`SWC.md`](https://github.com/sanskrit-lexicon/PD/blob/main/SWC.md) |
| `AOB.pdf` | 42 | Abbreviations of Books Quoted | [`AOB.md`](https://github.com/sanskrit-lexicon/PD/blob/main/AOB.md) |
| — (IA vol. 1 scan) | 28 | Introductory Essay (front matter pp. I-XXVIII) | [`ES.md`](https://github.com/sanskrit-lexicon/PD/blob/main/ES.md) |
| — (IA vol. 1 scan) | 39 | Index of Works Used in the Dictionary (pp. LXXXIX-CXXVII) | [`IW.md`](https://github.com/sanskrit-lexicon/PD/blob/main/IW.md) · [`IW.tsv`](https://github.com/sanskrit-lexicon/PD/blob/main/IW.tsv) |

Baselines from the first OCR pass are kept as `*_ocr.md` for diffing.

The Essay and the Index of Works have no source PDF in this repo. They are
transcribed from the 2023-06-17 Internet Archive scan of vol. 1
(`mAAY_an-encyclopaedic-dictionary-of-sanskrit-vol-1-critically-edited-by-a-m-ghatage-1`)
with [`parse_pd_frontmatter.py`](parse_pd_frontmatter.py), which pins the source
`djvu.xml` by SHA-256 and emits both Markdown files, the `IW.tsv`
subject-code × siglum index, and
[`pref_manifests/pd_vol1_frontmatter_manifest.tsv`](pref_manifests/pd_vol1_frontmatter_manifest.tsv)
(printed page → scan leaf). The original dictionary `.txt` files are untouched.

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

See [`about.md`](https://github.com/sanskrit-lexicon/PD/blob/main/about.md) and [`aboutDictionary.md`](https://github.com/sanskrit-lexicon/PD/blob/main/aboutDictionary.md) (KoshaSHRI / Deccan College).

---

_Dr. Mārcis Gasūns_
