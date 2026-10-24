# The Poona Dictionary (EDSHP) — a sourced knowledge page

_Created: 24-10-2026 · Last updated: 24-10-2026 · Maintained alongside the front-matter OCR in this
repository and the measurement data in [csl-atlas](https://github.com/sanskrit-lexicon/csl-atlas);
the working research copy lives elsewhere._

**What this page is.** Everything the project knows about *An Encyclopaedic Dictionary of Sanskrit on
Historical Principles* (Deccan College, Pune — "the Poona Dictionary", PD/EDSHP), sourced and
numbered: its publication state, its working environment, the measurements that have been made
against it, and the numbers that must **not** be quoted. Every section carries an evidence label in
the sense of the [csl-atlas evidence ladder](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/EVIDENCE_LABELS.md):
`observed` (the source says so), `derived` (a fixed rule restated it), `inferred` (a judgement that
may be wrong), `reviewed` (a human checked it — no section reaches this yet, and the page says so).

**Rights.** The machine-readable PD text is © 2014 The Sanskrit Library / Thomas Malten, CC BY-NC-SA
3.0; the printed dictionary is © Deccan College. This page quotes three short entries with full loci
and summarises published sources; no long text is reproduced.

---

## Verification status

Ten checks that the page can be audited against. `pass` means the artifact exists and resolves;
`open` names the unit that will close it.

| # | Check | State | Where |
|---|---|---|---|
| 1 | This page resolves at a public URL | **pass** | this file |
| 2 | A DOI for the page's dataset | open | report + deposit, pending |
| 3 | Every section carries an evidence label | **pass** | 13 / 13 below |
| 4 | At least one human-`reviewed` claim | open | inter-annotator study, pending |
| 5 | A canon ledger with every base labelled | **pass** | [`pd_canon_ledger.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_canon_ledger.tsv) |
| 6 | PD is a chapter in the dictionary atlas | open | chapter, pending |
| 7 | An edition-availability number by citation mass | open | measurement, pending |
| 8 | Every number gated against a committed owner | **pass** | 489 / 489 checks |
| 9 | This mirror is in sync with the working copy | **pass** | 24-10-2026 |
| 10 | A published report carrying the measurements | open | report, pending |

Score at creation: **5 / 10**. The five open rows are units with dated owners, not omissions.

---

## 1. Identity · observed

*An Encyclopaedic Dictionary of Sanskrit on Historical Principles* (Deccan College Postgraduate and
Research Institute, Pune) is the "Poona Dictionary" (PD / EDSHP). It was conceived and planned by
**S. M. Katre in 1948** on the OED model — senses in chronological development, dated citations —
and is compiled by quotation-slip lexicography: a paper corpus read from Vedic to late classical
Sanskrit. Its citation apparatus is a de-facto, frequency-weighted declaration of the Sanskrit
literary canon.

The often-repeated claim that PD is "the most source-exhaustive lexicographic project ever
attempted" is **not carried by a published measurement** and is not repeated as fact here. What has
been measured is a per-headword granularity of roughly **13–23×** the comparison dictionaries over
the covered range; the countable statement is the one to quote.

## 2. Publication state · observed

Sourced from the [Deccan College department page](https://dcpune.ac.in/san_researchdept.html) and the
official [publication ledger](https://dcpune.ac.in/pdf/12.%20Publication%20%28Dictionary%20Publication%29.pdf)
(probed 11-10-2026), a 2003 press witness, and the contemporary review by J. C. Wright.

- **Conception and offices.** Conceived and planned by S. M. Katre in 1948; first General Editor
  1948–1972; extraction of references 1948–1976; editing from 1973; **first fascicle 1976**, first
  bound volume 1978.
- **Slips.** The Scriptorium houses **ten million (one crore) quotation slips** from the 1948–1973
  reading programme. A 2003 press count gives **over nine million by 1975**; earlier statements give
  8 M by 1968 (Preface) and 10 M by 1973 (department page). Three dated statements, not one.
- **Official ledger.** **35 fascicle-volumes / 6,056 pages by 2019**, Vol. 35 closing at
  *abhigamyamānaparadārādi* — still inside letter *a*; the first vowel is not exhausted.
- **The "three times the OED" claim, tested** — it is a volume count, not a size, and the arithmetic
  is checkable from the plans: 37 planned volumes against the OED's 12 of 1928/1933 gives **3.08×**;
  at ~1,009 pp per planned volume PD's ~37,300 pages are **1.72×** OED²'s 21,730 (1989) and 2.41×
  OED¹'s ~15,500 (not re-verified); by planned entries the ratio is **2.22×**, and it reaches 6.9×
  pages / 8.9× entries only if PD's own *a-* density were held across the alphabet. The volume ratio
  is an artefact of volume thickness (~1,009 pp/vol against the OED's ~1,290).
- **2003 waypoint** (press witness, [*Outlook*, 1 Dec 2003](https://github.com/sanskrit-lexicon/PD/blob/main/PRESS/OUTLOOK_2003-12-01_KABRA_DICTIONARYAHA.md)):
  **3,368 pages** in six volumes of three fascicules (18 fascicules) against a **20,000-page** plan.
  With 1976 and 2019 this gives **125 pp/yr (1976–2003)** then **168 pp/yr (2003–2019)**; the same
  article reports **1,473 texts** mined in the first 25 years.
- **General editors.** Katre 1948–72 → Ghatage 1972–83 → Jog 1983–87 → S. D. Joshi 1987–93 → Gandhe
  1993–94 → Ranade 1995–97 → Bhatta 1997–2010 → Sathe 2010–17 → **Prasad Joshi 2017–**.
  **Print check:** no vol. 6 title page (1998, 2002, 2003) confers the label *General Editor*; all
  three print **"Edited by"** (6.1 Ranade · Bhatta; 6.2 and 6.3 Bhatta), and the string occurs
  nowhere in vol. 6.3's front matter. The 2003 title page reads **"Edited by Dr. V. P. Bhatta"**, and
  the January-2003 staff leaf records the handover: Ranade coordinator *upto 20-10-1997*, Bhatta
  *from 20-10-1997*, Ranade (Editor) *upto 31-03-1998*.
- **Contemporary review witness.** J. C. Wright's two-page notice of Vol. 1, Parts i–ii (Poona:
  Deccan College, 1976, 1977), *BSOAS* 41(2), 388–389, DOI
  [10.1017/S0041977X00124826](https://doi.org/10.1017/S0041977X00124826): confirms the 1948 Katre
  conception and Ghatage's editing from 1973, records the preface's own estimate of **1,500 texts
  utilised vs ~450 for the Petersburg dictionary**, and reports the contemporary projection that the
  work "will eventually run into 300 or 400 volumes" (17-10-2026: 35 fascicle-volumes).

## 3. Measurement headline · derived

From [csl-atlas `data/pd/pd_dcs_metrics.json`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_dcs_metrics.json)
and the [coverage report](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/reports/PD_DCS_CORPUS_COVERAGE_2026.md):

- **PD-citation-weighted DCS coverage: 25.16 %** — 88,929 of 353,512 primary citation occurrences of
  PD's letter-*a* canon are held by DCS.
- **DCS-token-weighted PD-canon share: 77.88 %** (DCS 2026) — 4,430,111 of 5,688,416 DCS tokens sit
  in PD-cited works; **74.06 %** in 2021 (3,389,516 of 4,577,021).
- **Scope caveat (binding).** These are the letter-*a* canon **as exercised in the 2009-vintage
  machine-readable text** (fascicles 1976–2009, *a-* to ~*apaca-*); print had already reached
  further into *a* by 2019. DCS is a deep sample of the archaic/classical core, not a broad sample of
  the canon.

**Title-level coverage — and the denominator problem.** 118 works are covered. Against the declared
canon the percentage depends entirely on which canon base is meant, and the bases differ:

| Base | Rows | 118 / base |
|---|---:|---:|
| AOB entry-like printed lines (structural) | 1,476 | 7.99 % |
| AOB entry rows, repeated headers removed | 1,469 | 8.03 % |
| AOB print census | 1,464 | 8.06 % |
| AOB pass-1 parse (not reproducible) | 1,419 | 8.32 % |
| AOB re-parse, raw entries (upper bound) | 1,517 | 7.78 % |
| Edition-level inventory | 1,437 | 8.21 % |
| Clean-subset edition rows — **a floor, never a denominator** | 1,118 | 10.55 % |
| **Index of Works, all printed rows** | **2,031** | **5.81 %** |
| Index rows printing a siglum | 1,622 | 7.27 % |
| Index rows with no siglum | 409 | — |

The two printed counts — **1,469** AOB entry rows and **2,031** Index rows — differ by **562 rows
(38.3 %)**. Of the 1,622 Index sigla, **981 (60.5 %)** find an AOB row and **641** do not; **497**
AOB sigla never appear in the Index. Every base and every percentage is derived and checked in
[`pd_canon_ledger.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_canon_ledger.tsv);
the rule is that no percentage is quoted without its base in the same row. The exercised letter-*a*
band is **2.4–4.8 %** (118 of 4,986 raw sigla / ~2,445 skeleton-merged works) — a different
denominator again, and labelled as such.

## 4. Working environment · observed

- **2003 baseline (press-attributed).** The team had been **thinned from 35 two decades earlier to
  18**; the college library (nearly two lakh volumes) was manned by **14 people**; **five computers**
  arrived only then; two new faces after over a decade; **no general editor or assistant editor**
  while V. P. Bhatta carried the duties. A 2019 site visit adds **4 staff of 40 wanted** (oral); the
  deliberately offline **intranet** dates to 2025 (oral).
- **People, 2003.** K. Paddayya (b. 1943; archaeologist, Professor Emeritus, former director of
  Deccan College; [Wikidata Q19894994](https://www.wikidata.org/wiki/Q19894994)) is named **project
  director**; D. B. Polkam (70, project advisor) is mentioned once.
- **Funding and digitisation, 2003.** The HRD ministry's **Rashtriya Sanskrit Sansthan** funded "some
  project positions"; the state governor demanded all volumes "within the next five years"; **C-DAC**
  quoted **Rs 4.5 crore** to scan and digitise the slips, which Paddayya called unaffordable for the
  state. The 2003 target was **one volume / 500 pages a year** — against the 2017 plan of **200
  pp/yr**: a plan-decay pair, both plans, neither realized.
- **Completion horizon — two models × three rates, derived.**
  **The denominator is explicit: 121 pp/yr is 6,056 ÷ 50 conception years; over printing years
  (1976–2019) the mean is ~141 pp/yr; the 2003 waypoint gives 125 (1976–2003) then 168 (2003–2019).**
  Holding the **37-volume plan** (~31,300 pp left): **≈2285 @121 · ≈2248 @141 · ≈2182 @200**; holding
  **today's density** across the remaining alphabet (~143,600 pp left): **≈3213 @121 · ≈3044 @141 ·
  ≈2744 @200**. The familiar "some three thousand years" is the density-held model at 121 (3,213) and
  survives at the printing-year rate as 3,044 — never a 200-pp/yr figure. Benchmark for finishability,
  not size: Mayrhofer finished *KEWA* in 24 years (1956–1980, 4 vols) and *EWA* in 15 (1986–2001);
  PD's remaining horizon is **~6–80×** those whole runs.
- The project's own philosophy is at peace with that: *ending a dictionary is not a goal, it is a
  process*.

## 5. Complementarity thesis · inferred

EDSHP and the public digital estate are complements, not competitors. PD's method *is* corpus
lexicography performed on paper, inside an intranet; CDSL/DCS brought the same citation machine into
machine-readable form, outside those walls. The natural exchange is PD's chronological sense-datings
↔ the estate's machine-readable citation base (edition-aware `<ls>` links, stable `L`-ids,
corrigibility): PD holds the historical depth the corpus lacks, the corpus makes PD's citation mass
computable. This is a thesis about what each side could give the other; §3 is the measurement that
makes one half of it checkable.

## 6. Method and caveats · observed

- **Letter-*a* scope, 2009-vintage text.** The machine-readable PD is the Cologne
  [PDScan 2020](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/index.php) edition
  ([`pdtxt.zip`](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/downloads/pdtxt.zip), 55 MB,
  107,630 `<L>` entries; © 2014 The Sanskrit Library / Thomas Malten, CC BY-NC-SA 3.0).
- **Homograph trap.** PD's inline sigla contain a near-homograph pair that similarity clustering
  silently fuses: `MahāBhā.` is the **Mahābhārata**, `MahāBh.` is the **Mahābhāṣya**; the locator
  shape tells them apart mechanically. Never similarity-merge the pair.
- **Coverage ≠ locus alignment** (editions may differ line-for-line), and the two-snapshot growth law
  rests on 2021/2026 only.
- **Contemporary appraisal (Wright 1978, 388–389).** A publication-time reviewer both praises the
  method and names its defects: at *akāmataḥ* the entry adds 47 printed lines of attestation, yet the
  sixth and last Petersburg attestation from **Manu 11.127** is silently omitted, and the homograph
  set *akak* / *akan* / *akac* vs *ak* is "not at all well integrated" — the same class as the
  `MahāBhā.` / `MahāBh.` trap. A review is not the source text: it witnesses what a trained reader
  saw in the printed fascicles.
- **Print-vs-digital boundary.** The measured text stops at ~*apaca-* (2009); the printed fascicles
  2009–2019 are additional letter-*a* canon the text does not carry.

## 7. Front-matter apparatus · derived

The machine-readable front matter lives in this repository: **AOB.md** (printed *Abbreviations of
Books*), **AUB.md** (publisher/series abbreviations), **GA**, **RG** (Reader's Guide), **SWC**
(Subject-wise Classification), OCR'd from the KoshaSHRI PDF and re-OCR'd to it as ground truth on
14-10-2026. The Reader's Guide (pp. lxxxii–lxxxvi) states the compound-selection rule: compounds of
two members are included in principle, longer compounds excluded in principle.

**What that rule costs, measured.** MW is the only major dictionary in the estate with
machine-readable compound joints; on the em-dash basis of record (**127,528** compound-marked
entries) the rule excludes **6.8 % of compound entries / 3.0 % of all entries** under the strict
samāsa-joint reading (93.2 % of MW's compounds are themselves two-member), but only **0.43 % of
letter-*a* entries** — the one letter PD has published. A looser reading that also counts
privative/preverb hyphens as member joints is not licensed: privatives split to three or more members
in 1.5 % (95 % CI 1.1–2.0), far below a 50 % trigger. The surviving strict count is a **joint** count,
not immediate-constituent depth: 47.3 % (Wilson CI 45.8–48.7) of valid three-em-dash markup rows parse
as two members. The labelled pair is **joints 8,638** (observed/derived) beside **IC-3+ ≈3,560**
(inferred, model-read, scaled from 8,392 surfaces — never a replacement). PD's structure is MW's:
atomise at two members, nest the tail.

**Declared canon.** The entry-level count is **≈1,476 rows**, the central estimate of the
1,419–1,517 bracket; a 2003 press statement gives 1,473 texts, and the printed AOB carries **1,469
entry rows** once 7 repeated column-header rows are removed. [`pd_aob_declared_works.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_aob_declared_works.tsv)
carries 1,112 work groups / 1,118 edition rows — a clean-subset **floor**, so 118/1,118 must not be
quoted. [`pd_aob_siglum_title.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_aob_siglum_title.tsv)
carries the census join at **63.3 % of sigla / 78.0 % of occurrence mass**.

## 8. Open items · observed

- **The printed general preface is witnessed, not collated.** A 2023-06-17 Internet Archive upload of
  vol. 1 carries the preface and Reader's Guide at pp. lxxi–lxxxviii as OCR text, including both
  sentences quoted by Wright (who cites the Reader's Guide at pp. lxxxii–lxxxvi). Archive.org now
  also holds vol. 2; vols 3.x and 8.2 are absent. Collation against the printed pages remains a
  Pune-trip item.
- **Residue not held anywhere.** A GRETIL-crossed queue finds **6 works / 9,229 PD citations missing
  everywhere** (Padmapurāṇa alone 3,506). This doubles as a corpus-digitisation priority list.
- **A per-letter completion law was tested and killed.** Single-letter data cannot confirm or refute
  a cross-letter law; the verdict is negative and stays negative until a second letter exists.
- **The Index of Works** is transcribed in full (2,031 rows); its 409 blank-siglum rows are classed
  but not yet adjudicated, and the 641 Index sigla with no AOB row are not yet explained.

## 9. Do-not-quote list · derived

Numbers that must **not** be quoted as current:

- **NWS 82.7 % (stems absent from the union) — RETRACTED.** A fuzzy recount proved it a
  filename-slug/transliteration-namespace artefact (slug-decode rescues 138,952 of 138,976 =
  99.98 %; true absent residue 22 lemmas ≈ 0.01 % of 167,991). The value is in content, not in new
  headwords.
- **"Volumes 30–32" as the publication state — STALE.** Superseded by the sourced ledger: **35
  fascicle-volumes / 6,056 pp by 2019**.
- **118 / 1,118 = 10.55 % as the declared canon — DEFECT.** The clean subset drops the Mahābhārata
  and the Rāmāyaṇa; it is a floor.
- The dead `SanskritSpellCheck/blob/master/external_src/pd/pd.txt` link for the machine text (a
  gitignored re-stage, never a stable artifact) — cite the Cologne `pdtxt.zip` instead.

## 10. Pointers · observed

| What | Where |
|---|---|
| PD × DCS measurement data — the `data/pd/` family | [csl-atlas `data/pd/`](https://github.com/sanskrit-lexicon/csl-atlas/tree/main/data/pd) |
| Coverage report (methods, limits, conclusions) | [PD_DCS_CORPUS_COVERAGE_2026.md](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/reports/PD_DCS_CORPUS_COVERAGE_2026.md) |
| Canon ledger — every base, every 118/N | [pd_canon_ledger.tsv](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_canon_ledger.tsv) |
| Evidence labels used on this page | [EVIDENCE_LABELS.md](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/EVIDENCE_LABELS.md) |
| Machine-readable PD text | [PDScan 2020](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/index.php) |
| Front matter OCR (this repository) | [AOB](https://github.com/sanskrit-lexicon/PD/blob/main/AOB.md) · [AUB](https://github.com/sanskrit-lexicon/PD/blob/main/AUB.md) · [GA](https://github.com/sanskrit-lexicon/PD/blob/main/GA.md) · [RG](https://github.com/sanskrit-lexicon/PD/blob/main/RG.md) · [SWC](https://github.com/sanskrit-lexicon/PD/blob/main/SWC.md) |
| Index of Works (this repository, subject × siglum pairs) | [IW.tsv](https://github.com/sanskrit-lexicon/PD/blob/main/IW.tsv) · [IW.md](https://github.com/sanskrit-lexicon/PD/blob/main/IW.md) |

## 11. Entry exhibits · observed

What a PD entry looks like — three complete entries, verbatim, one from each stretch of the
machine-readable range: the opening fascicle (1976), the middle (1990), the closing volume (2006).
Each carries its full locus: **fascicle · page · column · Cologne record `L`-id**, re-verified
against the PDScan 2020 text on 15-10-2026.

*Rendering note:* the text is the PDScan 2020 machine text (SLP1 layer transliterated to IAST, Vedic
accent marks removed as in the roman display, word spacing normalised); the `L`-id in each locus is
the key to re-check the entry against the scan.

### Exhibit 1 — aṃsatrakośa · fascicle 1.1 (1976)

> **अंसत्रकोश aṃsatrakośa** (áṃsatra-kośa) *adj.* having an armour for a bucket —
> droṇāhāvam avatam aśmacakram aṃsatrakośaṃ siñcatā nṛpāṇam — **ṚV. x. 101. 7.**

- **Locus:** fascicle **1.1** (1976, A. M. Ghatage; pp. 1–216) · p. **27**, col. a · Cologne record
  **L=510** (`pc` 1-0027a). Display: [`key=aMsatrakoSa`](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/webtc/getword.php?key=aMsatrakoSa&transLit=slp1&filter=roman);
  scan: [1-0027a](https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=PD&page=1-0027a).

### Exhibit 2 — ananuṣṭubha · fascicle 4.1 (1990)

> **अननुष्टुभ ananuṣṭubha** (an-anuṣṭubha) *adj.* which does not have (a verse in) anuṣṭubh —
> ananuṣṭubham etad ahar bhavati nānuṣṭubho 'dhīyate — **BaudhŚS. ii. 252. 10.**

- **Locus:** fascicle **4.1** (1990, S. D. Joshi; pp. 1959–2126) · p. **1960**, col. a · Cologne
  record **L=54507** (`pc` 4-1960a). Display: [`key=ananuzwuBa`](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/webtc/getword.php?key=ananuzwuBa&transLit=slp1&filter=roman);
  scan: [4-1960a](https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=PD&page=4-1960a).

### Exhibit 3 — annaśalya · fascicle 8.1 (2006)

> **अन्नशल्य annaśalya** (anna-śalya) *n.* splinter in the form of food —
> annaśalyāni vamanāṅgulipratimarśaprabhṛtibhiḥ (patanti) — **SuśruS. i. 27. 5.**

- **Locus:** fascicle **8.1** (2006, V. P. Bhatta; pp. 3849–4008) · p. **3849**, col. a · Cologne
  record **L=97206** (`pc` 8-3849a). Display: [`key=annaSalya`](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/webtc/getword.php?key=annaSalya&transLit=slp1&filter=roman);
  scan: [8-3849a](https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-apidev/servepdf.php?dict=PD&page=8-3849a).

Each exhibit is a complete entry of two lines — within short-quotation shape; none is paraphrased.

## 12. Findings register · observed

One line per finished measurement, with the public artifact that carries the evidence.

| Finding (one line) | Artifact |
|---|---|
| PD machine-readable text: staged `pd.txt` 55 MB, **107,630** `<L>` entries | this repository + csl-atlas census |
| Printed AOB authority vs harvested sigla: join **63.32 %** of families / **78.04 %** of mass; **+82** siglum-identity rescues → **64.92 % / 80.10 %**; 367 of 1,379 well-formed printed entries never cited under *a-* | [`pd_aob_sigla_reconciliation.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_aob_sigla_reconciliation.tsv) |
| 266 of 678 unconfirmed AOB joins confirmed from the printed book's own witnesses: **79.03 % → 87.26 %**; the 412 residuals all carry an OCR-broken adjudicated title | [`pd_aob_sigla_reconciliation.json`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_aob_sigla_reconciliation.json) |
| GRETIL-crossed residue queue: **6 works / 9,229 citations missing everywhere** (Padmapurāṇa 3,506) | residue sweep, reported in §8 |
| Per-letter-law extension **KILLED** as a PD question | §8 |
| `MahāBhā.` / `MahāBh.` homograph golden fixture: locator shape discriminates | csl-atlas fixture |
| Every live PD number swept to the sourced ledger: 35 fascicle-volumes / **6,056 pp** by 2019; 10 M slips | §2 |
| NWS 82.7 % retracted; true absent residue 22 / 167,991 lemmas ≈ **0.01 %** | §9 |
| Wright 1978 page density: PD's 216 pp ≈ **20 pp PWG / 10 pp Apte / 3 pp MW**; Wright's "PW" = PWG | [Wright 1978 review](https://doi.org/10.1017/S0041977X00124826) |
| Genre census: epigraphy **REFUTED** (0.91 %, 2 sigla); grammar **CONFIRMED** (6.97 %, 126 sigla, 35/49 Abhyankar works) | [`pd_citation_genre.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_citation_genre.tsv) |
| `MARKED` inheritance: **1,801 of 107,630** entries (**1.67 %**) carry a bracketed dictionary source; 1,956 marks (DBHS 852, PW 399, APTE 264, MW 245, VISVA 101, NT 84, VAC 11) | [`pd_inheritance_metrics.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_inheritance_metrics.tsv) |
| Compound-depth bracket **closed**: loose reading retired, strict count relabelled as joints, IC depth published as a labelled pair | §7 |
| **Outlook 2003** waypoint: 3,368 pp / 18 fascicles by 2003 → 125 pp/yr then 168; the 2003 forecast fails its own arithmetic | [PRESS transcription](https://github.com/sanskrit-lexicon/PD/blob/main/PRESS/OUTLOOK_2003-12-01_KABRA_DICTIONARYAHA.md) |
| **2003 title leaf** read: "Edited by Dr. V. P. Bhatta"; *General Editor* occurs nowhere in vol. 6 front matter | §2 |
| **Index of Works transcribed in full** (39 pp., 2,031 rows); Index prints the AOB siglum, so PD→AOB is a direct siglum join | [`pd_index_works.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_index_works.tsv) |
| **Canon ledger**: nine bases, every 118/N, the 562-row divergence and the 60.5 % join | [`pd_canon_ledger.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_canon_ledger.tsv) |

## 13. Reuse and citation · observed

- **This page:** cite it by URL and date; the prose is © the author, quoted sources keep their own
  rights. No licence is asserted for the prose beyond quotation with attribution.
- **Machine-readable PD text:** CC BY-NC-SA 3.0, © 2014 The Sanskrit Library / Thomas Malten.
- **Measurement data in csl-atlas:** see that repository's `CITATION.cff` and dataset README;
  `pd_canon_ledger.json` records the sha256 of every input the ledger was derived from.
- **The printed dictionary:** © Deccan College; short quotations with full loci only.
- **Corrections:** open an issue or a pull request here. A number that cannot be traced to a
  committed owner is a defect on this page, not a matter of interpretation.

---

_Maintained by Dr. Mārcis Gasūns · page created 24-10-2026 from the working research copy, with every
number re-pointed to a public artifact._
