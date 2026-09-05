# PWG front-matter OCR: Engine A vs Engine B

_Created: 23-07-2026 · Last updated: 05-09-2026_

**Question:** For PWG prefaces, how does vision-band OCR (Engine A, `/cologne-preface-ocr`) compare to Tesseract crop-then-OCR (Engine B, PD `run_ocr.py` v2 style)?

**Short answer:** **Engine A is the scholarly / canonical result** for PWG. Engine B recovers layout and much of the Latin/German skeleton but loses 19th-c. orthography fidelity, diacritics, and Devanāgarī-related romanization — not a replacement for A on CDSL scans.

---

## Setup

| | Engine A | Engine B |
|---|---|---|
| Method | Vision band OCR (native-res crops ≤1900 px, human/agent transcription) | Tesseract 5.5.0 `deu+eng+san`, crop-then-OCR (single or L→R 2-col × 3 bands) |
| Source files | [`PWG/prefaces/pwgprefNN.md`](https://github.com/sanskrit-lexicon/PWG/tree/main/prefaces) | this run: `PD/pwg_a_vs_b/B_*.md` via [`compare_pwg_a_vs_b.py`](https://github.com/sanskrit-lexicon/PD/blob/main/compare_pwg_a_vs_b.py) |
| Relation to `feat/ocr-v2-pipeline` | Cologne skill path | Same family as PD v2 (crop-then-OCR), adapted to PNG scans instead of PDF |

**Sample pages** (three layout types from vol. 1):

| Label | Scan | A file | Layout |
|---|---|---|---|
| title | `pwg1-0000--01.png` | [`pwgpref01.md`](https://github.com/sanskrit-lexicon/PWG/blob/main/prefaces/pwgpref01.md) | `single` |
| foreword | `pwg1-0000--02.png` | [`pwgpref02.md`](https://github.com/sanskrit-lexicon/PWG/blob/main/prefaces/pwgpref02.md) | `prose_2col` |
| abbreviations | `pwg1-0000--06.png` | [`pwgpref07.md`](https://github.com/sanskrit-lexicon/PWG/blob/main/prefaces/pwgpref07.md) | `prose_2col` |

---

## Metrics (token-level vs A as reference)

Tokens = Unicode word pieces after lowercasing, dropping A’s `**bold**` and `[page N]` markers. **Jaccard** = |A∩B| / |A∪B|. **Recall@A** = |A∩B| / |A| (how much of A’s vocabulary B recovers).

| Page | A chars | B chars | A tok | B tok | Jaccard | Recall@A |
|---|---:|---:|---:|---:|---:|---:|
| title | 193 | 213 | 23 | 24 | 0.406 | 0.619 |
| foreword | 4032 | 4186 | 581 | 634 | 0.728 | 0.915 |
| abbreviations | 4704 | 4658 | 612 | 651 | 0.405 | 0.631 |

**Means over 3 pages:** Jaccard **0.513**, Recall@A **0.722**.

---

## Qualitative findings

### Title page (Jaccard 0.41 · Recall@A 0.62)

| Field | A | B |
|---|---|---|
| Main title | `SANSKRIT-WÖRTERBUCH` | `SANSKRIT-WÖRTERBU` (final *CH* lost) |
| Editors | `Otto Böhtlingk und Rudolph Roth` | `orre BéuTiinen ı. Rupotes Rorn` (unusable) |
| Akademie line | `KAISERLICHEN AKADEMIE DER WISSENSCHAFTEN` | `… BER WISSENSCHAFTEN` (*DER*→*BER*) |
| Part / place / year | *ERSTER THEIL. DIE VOCALE.* · St. Petersburg · 1855 | same three lines mostly OK |

B also injects edge noise (`N  ॥   |     W  IR`). **Names on the title page fail hard** under Tesseract here — fatal for a catalog record even when place/year survive.

### Foreword (Jaccard 0.73 · Recall@A 0.92) — B’s best page type

Long German prose is where crop-then-OCR helps most: L→R column order is largely correct and ~91% of A’s content tokens appear somewhere in B.

Concrete slips in B (this run):

| Phenomenon | Example |
|---|---|
| Proper name | A `Wilson's` → B `Wıuson’s` (dotless ı / confusable) |
| Digit error | A `13 Jahre später` → B `43 Jahre später` |
| Broken compounds at band seams | A `ausserordentliche` split → B `ausser-` + later `ordentliche` |
| Spelling drift | A `Sanskrit-Literatur` → B `Sauskrit-Literatur` |
| Band garbage / Devanāgarī noise | `Ann १7. -¶ 1... "II UA _ 7)` mid-paragraph |
| Digitizer stamp leaked | `Institute of Indology & Tamil Studie.` (A deliberately omits Cologne footers) |
| Umlaut / W confusion | `WVörterbuch`, `\Vörterbuch` |

**Reading grade:** a German speaker can *skim* B’s foreword and recover the argument. **Edition grade:** no — wrong numbers, broken words, and stamp noise disqualify it as a substitute for A.

### Abbreviations list (Jaccard 0.41 · Recall@A 0.63) — B’s worst page type

| A (gold) | B (this run) |
|---|---|
| `**Âçv. Çr.** = Âçvalâjana's Çrautasûtrâni…` | `Agy. Cr. = Agvarisana’s Crautasdraint…` |
| `**Ait. Br.** = Aitarejabrâhmaṇa…` | `Ait. Ba. = Arrangsapninmana…` |
| `**AK.** = Amarakosha… Colebrooke…` | `AK. = Amanaxosna… CotesrookeE…` |
| `**Anekârthadhv.** = Anekârthadhvanimańḱarî…` | `ANEKÄRTHADHV. — AÄNEKÄRTHADHYANIMANGARi…` |

Keys and expansions are systematically wrong on diacritics and Indic romanization. Token recall ~0.63 overstates usability: many “matches” are short German scaffolding words (*ein, nach, der*), not the bibliographic keys a reader needs.

**Verdict for abbreviation pages:** B alone is not usable; A is required (or vision repair of B).

### Token-diff samples

**title**

- In A only (sample): `wörterbuch`, `böhtlingk`, `rudolph`, `otto`, `roth`, `der`, `und`, `von`
- In B only (sample): `béutiinen`, `wörterbu`, `rupotes`, `orre`, `rorn`, `ber`, `ir`, `n`

**foreword**

- In A only (sample): `ausserordentliche`, `mangelhaftigkeit`, `unbekanntschaft`, `entstellungen`, `gelehrsamkeit`, `widersprüchen`, `hinauskommen`, `überkommenen`, `aufgehenden`, `entstellten`, `erheblichen`, `geforderten`
- In B only (sample): `gelhaftigkeit`, `ordentliche`, `ersprüchen`, `irrthiimer`, `university`, `vörterbuch`, `institute`, `intschaft`

**abbreviations**

- In A only (sample): `anekârthadhvanimańḱarî`, `bṛhadâraṇjakopanishad`, `brahmavaivartapurâṇa`, `amṛtavindûpanishad`, `atharvavedasaṃhitâ`, `anekârthasaṃgraha`, `zusammengesetzten`, `aitarejabrâhmaṇa`, `aitarejopanishad`, `berücksichtigung`, `bhâshâpariḱḱheda`, `legendensammlung`
- In B only (sample): `aänekärthadhyanimangari`, `brhadäranjakopanishad`, `brahmavaivartapuräna`, `atharvavedasanibitä`, `amrtavindüpanishad`, `anbeärthasamgraha`, `arrangsapninmana`, `arrangsopanisnap`

---

## Side-by-side excerpts (~650 chars)

### Title (`pwg1-0000--01.png`)

**Engine A**

```text
SANSKRIT-WÖRTERBUCH

HERAUSGEGEBEN

VON DER

KAISERLICHEN AKADEMIE DER WISSENSCHAFTEN,

BEARBEITET

VON

Otto Böhtlingk und Rudolph Roth.

————

ERSTER THEIL.

DIE VOCALE.

St. Petersburg

1855
```

**Engine B**

```text
N  ॥   |     W  IR           ( ||
SANSKRIT-WÖRTERBU
HERAUSGEGEBEN
KAISERLICHEN AKADEMIE BER WISSENSCHAFTEN,
BEARBEITET
orre BéuTiinen ı. Rupotes Rorn.

                 ERSTER THEIL.
DIE VOCALE
St. Petersburg
1855
```

### Foreword (`pwg1-0000--02.png`)

**Engine A**

```text
[page III]

VORWORT.

In den dreissig und etlichen Jahren, welche verstrichen sind, seitdem in Calcutta H. H. Wilson's Sanskrit-Englisches Wörterbuch erschien, hat das Studium der Sanskrit-Sprache und Literatur unter uns so mächtige Fortschritte gemacht, dass der Versuch, durch eine neue Bearbeitung des Wortschatzes dem sich immer weiter ausbreitenden und höher wachsenden Bau sicherere Stützen und Pfeiler zu geben, wohl an der Zeit sein möchte.

Das bedeutende Werk, welches der berühmte englische Gelehrte, unterstützt durch die Arbeiten indischer Pandits, damals (1819) zu Stande brachte und 13 Jahre später (1832) erweitert und verbessert zum
…
```

**Engine B**

```text
VOR
In den dreissig und etlichen Jahren, welche verstrichen
sind, seitdem in Calcutta H. H. Wıuson’s Sanskrit- Englisches
Wörterbuch erschien, hat das Studium der Sanskrit-Sprache
und Literatur unter uns so mächtige Fortschritte gemacht, dass
Ann १7. -¶ 1... "II UA _ 7). _¶ "I... अ इह , 1,

der Versuch, durch eine neue Bearbeitung des Wortschatzes
dem sich immer weiter ausbreitenden und höher wachsenden
Bau sicherere Stützen und Pfeiler zu geben, wohl an der Zeit
sein möchte.

Das bedeutende Werk, welches der berühmte englische
Gelehrte, unterstützt durch die Arbeiten indischer Pandits,
damals (1819) zu Stande brachte und 43 Jahre später (183
…
```

### Abbreviations (`pwg1-0000--06.png`)

**Engine A**

```text
(Gedruckte Werke aus der Sanskrit-Literatur, die nur ganz gelegentlich citirt werden, sind mit einem Sternchen bezeichnet.)

**Âçv. Çr.** = Âçvalâjana's Çrautasûtrâni in 12 Adhjâja. Handschrift.
**Âçv. Gṛhj.** = Âçvalâjana's Gṛhjasûtrâni in 4 Adhjâja. Hdschr.
**Adbh. Br.** = Adbhutabrâhmaṇa.
**Adbhutas.** = Adbhutasâra.
**A Dict. Beng. and S. (Haughton,)** = A Dictionary Bengali and Sanskrit, explained in English.
**Agnisv.** = Agnisvâmin, ein Scholiast des Lâṭjâjana.
**Âhnikat.** = Âhnikatattva.
**Ait. Br.** = Aitarejabrâhmaṇa. Citirt nach den 8 Pańḱikâ (einer äusseren Abtheilung, in welche die 40 nach sachlichen Rücksichten gebildeten Adhjâ
…
```

**Engine B**

```text
(Gedruckte Werke aus der Sanskrit-Literatur, die nur ga
MO १ __ + 9 A ke in AI ॥ 1154; Handenh:

Agy. Cr. = Agvarisana’s Crautasdraint in 42 Adhjdja. Handschi
Acy. Gras. = Acvarisana’s Gansasdtaan in 4 Adhjäja. Hdschr.
Ansa, Br. = ADBAUTABRÄBMANA.

ADBHUTAS. == ADBHUTASARA.

A Dict. Beng. and S. (Hıvcaron,) = A Dictionary Bengali and Sansl
explained in English.

Acnisy. = AcnısvÄmın, ein Scholiast des Lärsäsana.

AanikaT, == ÄHNIKATATTVA.

Ait. Ba. = Arrangsapninmana. Citirt nach den 8  Pankika (ei
äusseren Abtheilung, in welche die 40 nach sachlichen Rücksich
gebildeten Adhjäja zerlegt sind) und den innerhalb der Pank:
durchlaufenden Kapitel
…
```

---

## Recommendation

| Use case | Winner |
|---|---|
| Canonical CDSL front-matter editions (PWG and siblings) | **A** |
| Bulk first pass on English multi-column PDF tables (PD AOB/GA style) | **B** (then optional A repair) |
| German 19th-c. prose with heavy diacritics on csldoc PNGs | **A** |
| Cost / speed at scale | B cheaper; A quality-gated |

**Do not replace PWG’s existing `pwgprefNN.md` with Engine B output.** Keep A as gold; keep B artifacts under `PD/pwg_a_vs_b/` for this bake-off only.

### Reproduce

```text
cd C:\Users\user\Documents\GitHub\PD
python compare_pwg_a_vs_b.py
```

Requires: Tesseract 5.x with `deu` + `eng` + `san`, `pillow`, `pytesseract`.

---

_Dr. Mārcis Gasūns_

_Auto-generated metrics by Grok 4.5 (`grok-4.5`) via compare_pwg_a_vs_b.py on 2026-07-23._

_Dr. Mārcis Gasūns_
