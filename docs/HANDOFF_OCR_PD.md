# HANDOFF: Finish OCR of PD Prefaces (Antigravity → Grok)

_Created: 23-07-2026 · Last updated: 17-10-2026_

**Date of handoff:** 2026-07-23  
**Previous agent:** Antigravity → continued by Grok 4.5  
**Local path:** `C:\Users\user\Documents\GitHub\PD`  
**Goal:** High-quality OCR of 5 scanned Sanskrit-related PDF prefaces into clean Markdown.

## Status — 🔴 EXECUTED (v2 pipeline shipped)

| Step | Status |
|------|--------|
| Source PDFs present | ✅ all 5 |
| Tesseract `eng`+`san` | ✅ 5.5.0 |
| Column-aware v1 | ✅ (superseded) |
| **v2 crop-then-OCR pipeline** | ✅ [`run_ocr.py`](https://github.com/sanskrit-lexicon/PD/blob/main/.github/scripts/run_ocr.py) |
| Regenerated `*.md` | ✅ GA AUB RG SWC; AOB re-run with force=`multi_seq` |
| Provenance + page markers | ✅ |
| Italic stopword ban | ✅ (~0 false `*of*`/`*and*`) |
| Pair format `` `key` expansion `` | ✅ (plan option a) |

### Preface (pp. V–VI) — 17-10-2026

The printed Preface is not among the five KoshaSHRI PDFs and was not part of the v2 run.
It is transcribed from the archive.org scan of Vol. 1 (1976), leaves 8–9
(`mAAY_an-encyclopaedic-dictionary-of-sanskrit-vol-1-...`), as
[`PREFACE.md`](https://github.com/sanskrit-lexicon/PD/blob/main/front_matter/PREFACE.md).
Method: Tesseract 5.5.3 `eng`, column crops, then line-by-line collation against the
page images; printed defects retained, damaged sorts restored where unambiguous.

### Layout modes in v2

| PDF | Mode | Notes |
|-----|------|-------|
| GA | `multi_pair` | 3× (key\|exp) abbreviation grid |
| AUB | `multi_pair` | 2× (key\|exp) bibliography abbrevs |
| AOB | `multi_seq` | Abbreviation \| Title \| Mode of reference |
| RG | `prose_2col` | Reader’s Guide |
| SWC | `prose_2col` | Subject-wise classification |

### Residual quality limits (Tesseract, not pipeline)

- Character-level OCR noise remains (`2110100.` for `anom.`, comma/period swaps, truncated long lines).
- Devanāgarī better than native PDF mojibake, still imperfect conjuncts.
- Vision-band repair (cologne-preface-ocr style) only if scholarly perfection needed later.

### How to re-run

```text
python .github/scripts/run_ocr.py
python .github/scripts/run_ocr.py --only AOB.pdf --start-page 20
```

See [`README.md`](https://github.com/sanskrit-lexicon/PD/blob/main/README.md).

---

_Dr. Mārcis Gasūns_
