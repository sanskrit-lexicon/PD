# AOB OCR comparison: Antigravity (`AOB_ocr.md`) vs Grok (`AOB.md`)

_Created: 23-07-2026 · Last updated: 23-07-2026_

**Question:** Which file is the final result — [`AOB.md`](https://github.com/sanskrit-lexicon/PD/blob/main/AOB.md) or [`AOB_ocr.md`](https://github.com/sanskrit-lexicon/PD/blob/main/AOB_ocr.md)?

**Short answer:** **[`AOB.md`](https://github.com/sanskrit-lexicon/PD/blob/main/AOB.md) is the final / canonical deliverable** (Grok pipeline v2). [`AOB_ocr.md`](https://github.com/sanskrit-lexicon/PD/blob/main/AOB_ocr.md) is the frozen **Antigravity v1 baseline**, kept for diffing — not the finished form.

Source PDF: [`AOB.pdf`](https://github.com/sanskrit-lexicon/PD/blob/main/AOB.pdf) (42 pages, *Abbreviations of Books Quoted in the Sanskrit Dictionary*).

---

## Provenance

| File | Agent / pipeline | When | Role |
|------|------------------|------|------|
| `AOB_ocr.md` | **Antigravity** — early full-page Tesseract / markitdown-style pass | 2026-07-23 ~12:30 | v1 baseline (pre column-aware, pre pairing) |
| `AOB.md` | **Grok 4.5** — [`run_ocr.py`](https://github.com/sanskrit-lexicon/PD/blob/main/run_ocr.py) **v2** (`multi_seq`: Abbreviation \| Title \| Mode) | 2026-07-23 ~14:02 | **Final regenerated output** |

Both are Tesseract-based OCR of the same scan; neither is a hand transcription.

---

## Quantitative comparison

| Metric | Antigravity `AOB_ocr.md` | Grok `AOB.md` | Notes |
|--------|-------------------------:|--------------:|-------|
| File size | 176 509 B | 150 794 B | Grok slightly smaller (less blank lines / less dump) |
| Characters | 166 279 | 144 627 | |
| Total lines | 9 070 | 2 007 | Antigravity is very sparse (many 1-token lines) |
| Non-empty lines | 5 805 | 1 923 | |
| `## Page N` markers | 0 | **42** | Grok: one section per PDF page |
| Provenance header | no | **yes** | engine, lang, pipeline, date |
| Devanāgarī codepoints | 267 | **508** | Grok higher count (not always cleaner glyphs) |
| Italic spans `*…*` | 3 | 53 | AOB is mostly roman; italics less critical |
| False stopword italics (`*of*` etc.) | 0 | 0 | |
| Lines starting with `` `key` `` | ~40 (noise) | **~1 879** | Grok’s intentional pair format |
| Mode separator ` — ` | 0 | **1 271** | Grok joins Mode of Reference onto the entry |
| Scan noise `~` | 26 | 5 | |
| Scan noise `\|` | 51 | 1 | |

---

## Structural comparison (the decisive difference)

Printed page layout (simplified):

```text
Abbreviation     Name of the Book, Author, Edition…     Mode of Reference
AbhidhaCin.      Abhidhanacintamani, Hemacandra…         Śloka
AbhidhK.         Abhidharmakośa, Vasubandhu…             Kośasthāna. Śloka
```

### Antigravity (`AOB_ocr.md`) — column dump, wrong reading order

Reads (or reconstructs) roughly **left column fully → middle column fully → right column fully**:

```text
AbhidhaCin,
AbhidhaMafi,
…
AitUBh,

Name of the Book, Author, Hdition ant Editor

Abhidhanacintamani, Hemacandra, Leipzig 1847, Otto Boehtlingk and
Charles Rieu
Abhidhanamafijari, Bhisagarya, VG, 2, 1942
…
```

**Effect:** abbreviation and title are **not on the same line**. Lookup requires manually re-aligning three long lists. Multi-line titles are sometimes more complete as continuous prose, but **pairing is lost**.

Tail of the file dumps leftover “Mode of Reference” fragments after all titles — confirmation of sequential column dump.

### Grok (`AOB.md`) — row-paired triple

Intended format (plan option **a** for pairs; AOB extends to three fields):

```text
`AbhidhaCin,` Abhidhanacintamani, Hemacandra, Leipzig 1847, … — Sloka
`AbhidhK,` Abhidharmakosa, Vasubandhu, TSWS, 8, 1967, … — Koéasthana. Sloka
```

**Effect:** each entry is **one logical row** — key + title (+ mode). That matches how the printed table is used. Page breaks are explicit (`## Page 1` … `## Page 42`).

**Cost:** y-alignment across multi-line titles sometimes **splits or merges** rows (see failure modes below). OCR still mangles diacritics and long lines.

---

## Side-by-side sample (page 1 opening)

| Antigravity `AOB_ocr.md` | Grok `AOB.md` |
|--------------------------|---------------|
| `AbhidhaCin,` alone, then dozens of bare keys | `` `AbhidhaCin,` Abhidhanacintéamani, Hemacandra, Leipzig 1847, Otto Boehtling] — and Sloka `` |
| Titles only after entire key list ends | Title + mode attached immediately |
| `Hdition ant Editor` (OCR error) | Same class of character errors, but co-located with key |
| No page / engine metadata | Provenance comment + `# AOB.pdf` + `## Page N` |

Both still misread many Latin diacritics (`Boehtlingk` → `Boehtling]`, `ś`/`ṣ` inconsistent). Grok occasionally injects stray Devanāgarī into Latin (`AbhinBha, धि`).

---

## Where Antigravity is stronger

1. **Raw bulk / multi-line titles** — long book titles that wrap across 2–3 print lines often appear as fuller continuous paragraphs once the title block is reached.
2. **Fewer mid-key fractures** — because it never tries to y-pair, it does not invent broken keys like Grok’s mid-document slips (`Mayi Mali. Mayakk` / split `MeghDi` rows).
3. **Slightly larger text mass** — useful as a **search backup** if a title fragment is missing from `AOB.md`.

## Where Grok is stronger

1. **Usable table structure** — key ↔ title ↔ mode on one line (primary success criterion for this PDF type).
2. **Navigation** — 42 page headers; provenance for re-runs.
3. **Less column-gutter noise** (`~`, `|`).
4. **Aligned with the maintained pipeline** ([`run_ocr.py`](https://github.com/sanskrit-lexicon/PD/blob/main/run_ocr.py) v2, `FORCE_LAYOUT_BY_STEM["AOB"] = "multi_seq"`).
5. **Higher Devanāgarī count** where Devanāgarī actually appears (still imperfect).

---

## Grok failure modes (honest residuals)

These are why `AOB.md` is “final pipeline output” but **not** a clean scholarly edition:

| Failure | Example shape | Cause |
|---------|---------------|--------|
| Multi-line title y-mismatch | Key glued to half a title; mode glued wrong | `triple_columns_by_y` + wrapped print lines |
| Split abbreviations | One printed key becomes two MD lines | Line grouping / crop edges |
| Truncated long titles | Ends mid-word before ` — ` | Column crop + Tesseract line length |
| Character OCR | `Abhidhanacintéamani`, `fiir`, `2` for `P` | Scan + `eng+san` confusion |
| Header bleed | Page 2: `` `Abbreviation* *Name` of the *Bock*… `` | Title row of table OCR’d as an entry |

Antigravity avoids some of these by never pairing — at the price of an unusable list order.

---

## Verdict

| Criterion | Winner |
|-----------|--------|
| **Canonical / final file for the repo** | **`AOB.md` (Grok v2)** |
| **Reading order matches the printed table** | **Grok** |
| **Long multi-line title fidelity (raw dump)** | Antigravity (often) |
| **Re-runnable pipeline + page structure** | **Grok** |
| **Character-level OCR accuracy** | Roughly **tie** (both noisy) |
| **Human lookup of “what does AbhidhK. mean?”** | **Grok** |

**Recommendation**

- Treat **`AOB.md` as the final result** for the PD project and for PR/docs.
- Keep **`AOB_ocr.md` as the Antigravity v1 baseline** (already named that way in README) for forensic comparison or to recover a missing title fragment.
- If a clean scholarly edition is required later: use `AOB.md` as the structural skeleton and repair hard pages with vision-band OCR (cologne-preface style), not by reverting to `AOB_ocr.md`.

### One-line summary

**Grok `AOB.md` = final structured OCR; Antigravity `AOB_ocr.md` = larger unstructured baseline dump.**

---

_Dr. Mārcis Gasūns_
