# PD

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23151371.svg)](https://doi.org/10.5281/zenodo.23151371)

Front-matter OCR for *An Encyclopaedic Dictionary of Sanskrit on Historical Principles*
(Deccan College / KoshaSHRI).

**Knowledge page:** [`PD_KNOWLEDGE.md`](PD_KNOWLEDGE.md) — sourced facts, measurements, canon
denominators and a do-not-quote list for the dictionary itself, each section carrying an evidence
label.

_Created: 23-07-2026 · Last updated: 24-10-2026_

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

**Preface (pp. V–VI).** The printed Preface is not among the KoshaSHRI PDFs. It is
transcribed from the archive.org scan of Vol. 1 (1976), leaves 8–9, as
[`PREFACE.md`](https://github.com/sanskrit-lexicon/PD/blob/main/PREFACE.md).

**Introductory Essay (pp. I–XXVIII) and Index of Works (pp. LXXXIX–CXXVII).** No
source PDF for either ships in this repo; both are transcribed from the 2023-06-17
Internet Archive scan of vol. 1
(`mAAY_an-encyclopaedic-dictionary-of-sanskrit-vol-1-critically-edited-by-a-m-ghatage-1`)
with [`parse_pd_frontmatter.py`](parse_pd_frontmatter.py), which pins the source
`djvu.xml` by SHA-256 and emits [`ES.md`](ES.md), [`IW.md`](IW.md), the
[`IW.tsv`](IW.tsv) subject-code × siglum index and
[`pref_manifests/pd_vol1_frontmatter_manifest.tsv`](pref_manifests/pd_vol1_frontmatter_manifest.tsv)
(printed page → scan leaf). The original dictionary `.txt` files are untouched.

**Additional Abbreviations (p. CXXVIII)** remains outside this pack.

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

`PREFACE.md` is a one-off transcription and is **not** produced by `run_ocr.py`: Tesseract 5.5.3 supplied a column-cropped base text, which was then collated line by line against the page images.

## About the dictionary

See [`about.md`](https://github.com/sanskrit-lexicon/PD/blob/main/about.md) and [`aboutDictionary.md`](https://github.com/sanskrit-lexicon/PD/blob/main/aboutDictionary.md) (KoshaSHRI / Deccan College).


## Rights

Original contributions are [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt)
([`LICENSE`](https://github.com/sanskrit-lexicon/PD/blob/main/LICENSE)); the Cologne machine text,
the printed dictionary and the press witness each keep their own regime. The layering is stated in
[`RIGHTS.md`](https://github.com/sanskrit-lexicon/PD/blob/main/RIGHTS.md).

---

_Dr. Mārcis Gasūns_
