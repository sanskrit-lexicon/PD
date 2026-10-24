# The Poona Dictionary (EDSHP)

_Created 24 October 2026. Sources are named in each section; every number is re-derivable from the
data linked at the end._

*An Encyclopaedic Dictionary of Sanskrit on Historical Principles* (Deccan College, Pune; "the Poona
Dictionary", EDSHP) is a Sanskrit dictionary on historical principles. S. M. Katre conceived it in
1948, and it is compiled from a corpus of quotation slips. It is unfinished: 35 fascicle-volumes by
2019, still inside the first letter of the alphabet. This page records what is known about it, with
the source and the limit of each claim.

The machine-readable text is the Cologne PDScan 2020 edition, © 2014 The Sanskrit Library / Thomas
Malten, CC BY-NC-SA 3.0. The printed dictionary is © Deccan College. Quotations below are short and
carry their loci.

## 1. The dictionary

PD is a quotation-slip dictionary on the model of the *Oxford English Dictionary*: senses are ordered
by historical development, and each sense is supported by dated citations. The slips were read from
Vedic to late classical Sanskrit, and the Scriptorium holds about ten million of them from the 1948
to 1973 reading programme. The dictionary's citations therefore amount to a declaration of the
Sanskrit literary canon, weighted by how often each work is quoted.

The machine-readable text covers fascicles issued between 1976 and 2009, from *a-* to roughly
*apaca-*, in 107,630 entries and 104,959 lemmas. The printed record reached
*abhigamyamānaparadārādi* by volume 35 (2019, page 6,056). About 4 to 6 percent of the headword span
of a completed dictionary has been published.

## 2. Publication record

- Conceived and planned by S. M. Katre in 1948; first General Editor 1948 to 1972; extraction of
  references 1948 to 1976; editing from 1973; first fascicle 1976; first bound volume 1978.
- The Scriptorium holds ten million quotation slips (1948 to 1973). A 2003 press count gives over
  nine million by 1975; earlier statements give 8 million by 1968 (Preface) and 10 million by 1973
  (department page).
- Official ledger: 35 fascicle-volumes, 6,056 pages by 2019, closing at
  *abhigamyamānaparadārādi*.
- General editors: Katre 1948 to 1972, Ghatage 1972 to 1983, Jog 1983 to 1987, S. D. Joshi 1987 to
  1993, Gandhe 1993 to 1994, Ranade 1995 to 1997, Bhatta 1997 to 2010, Sathe 2010 to 2017, Prasad
  Joshi 2017 to the present. No volume 6 title page (1998, 2002, 2003) uses the label *General
  Editor*; all three print "Edited by", and the 2003 title page reads "Edited by Dr. V. P. Bhatta".
- A 2003 press witness records 3,368 pages in 18 fascicles against a 20,000-page plan, which gives
  125 pages a year from 1976 to 2003 and 168 from 2003 to 2019. The same article reports 1,473 texts
  used in the first 25 years.
- The claim that PD is "three times the OED" is a count of volumes, not of size. Thirty-seven
  planned volumes against the OED's 12 of 1928/1933 gives 3.08 times; at about 1,009 pages per
  planned volume the page ratio is 1.72 against the OED's second edition (21,730 pages) and 2.22
  against its planned entries.
- At the historical rate of 121 printed pages a year, holding today's density across the remaining
  alphabet gives about 3,213 years; against the 37-volume plan it gives about 2,182. The project's
  own position is that ending a dictionary is a process, not a goal.

Sources: the [Deccan College department page](https://dcpune.ac.in/san_researchdept.html) and
[publication ledger](https://dcpune.ac.in/pdf/12.%20Publication%20%28Dictionary%20Publication%29.pdf)
(probed 11 October 2026); the [Outlook feature of 1 December 2003](https://github.com/sanskrit-lexicon/PD/blob/main/PRESS/OUTLOOK_2003-12-01_KABRA_DICTIONARYAHA.md);
J. C. Wright's review of volume 1, parts i and ii, *BSOAS* 41(2), 388-389, DOI
[10.1017/S0041977X00124826](https://doi.org/10.1017/S0041977X00124826).

## 3. What has been measured

The Digital Corpus of Sanskrit (DCS) is the largest lemmatised Sanskrit corpus. Measured against PD's
cited canon, it holds 25.16 percent of PD's primary citation occurrences (88,929 of 353,512), and
77.88 percent of DCS tokens fall in works PD cites (4,430,111 of 5,688,416; 74.06 percent in 2021).
DCS is a deep sample of the archaic and classical core and a narrow sample of PD's encyclopaedic
breadth: the purāṇas, the lexicographic tradition, classical kāvya and much of the grammatical
commentary layer are cited by PD and absent from DCS.

Title-level coverage has been quoted against several denominators, and the choice of denominator
changes the result. All of the following measure something different: 1,476 entry rows (the basis
used in the paper), 1,469 printed entry rows after repeated column headers are removed, 1,419 and
1,517 (bounds from two parses), 1,437 (edition-level inventory), 1,118 (a clean subset that drops the
Mahābhārata and Rāmāyaṇa, and a floor rather than a denominator), 2,031 rows of the printed Index of
Works, and 1,622 of those rows, which print a siglum. The two printed counts, 1,469 and 2,031, differ
by 562 rows. Of the 1,622 Index sigla, 981 find a row in the Abbreviations of Books and 641 do not.
Every base, with its own percentage, is derived and checked in
[`pd_canon_ledger.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_canon_ledger.tsv).
A coverage percentage is meaningless without its base; the 8.0 percent often quoted is the 1,476
basis.

The scope caveat is binding. These figures describe the letter *a-* canon as exercised in the
2009-vintage text, not the full printed dictionary, which extends further.

The measures above come from the [DCS coverage report](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/reports/PD_DCS_CORPUS_COVERAGE_2026.md)
and [data/pd/](https://github.com/sanskrit-lexicon/csl-atlas/tree/main/data/pd).

## 4. Method and known defects

- **Text and scope.** The machine text is PDScan 2020, 55 MB, 107,630 entries, ending at *apaca-*
  (page 4,327). The printed fascicles of 2009 to 2019 are not in it.
- **A homograph trap.** `MahāBhā.` is the Mahābhārata and `MahāBh.` is the Mahābhāṣya. The two are
  near-identical as strings and similarity clustering merges them; the locator shape distinguishes
  them.
- **Coverage is not alignment.** Holding a work is not holding the same lines, since editions differ.
- **A contemporary appraisal.** Wright's 1978 review praises the method and names its defects. At
  *akāmataḥ* the entry adds 47 printed lines of attestation but omits the sixth Petersburg
  attestation, Manu 11.127. The homograph set *akak*, *akan*, *akac* and *ak* is "not at all well
  integrated". The review witnesses what a trained reader saw in the printed fascicles; it is not the
  source text.

## 5. Numbers that must not be quoted

- **82.7 percent of stems absent from the union: retracted.** A recount showed the figure to be an
  artefact of filename slugs and transliteration; after normalisation the true residue is 22 lemmas,
  about 0.01 percent of 167,991.
- **"Volumes 30 to 32": stale.** The sourced ledger gives 35 fascicle-volumes and 6,056 pages by
  2019.
- **118 divided by 1,118, or 10.55 percent: a floor, not a coverage figure.** The clean subset drops
  two major works.
- The dead `SanskritSpellCheck` link to `pd.txt`: cite the Cologne `pdtxt.zip` instead.

## 6. Three entries

One complete entry from each stretch of the machine-readable text. Each carries its locus: fascicle,
page, column and Cologne record number. All three were checked against PDScan 2020 on 15 October
2026. Punctuation is normalised for this page; the words are the machine text's.

**aṃsatrakośa**, fascicle 1.1 (1976), page 27, column a, record L=510 (1-0027a).

> **अंसत्रकोश aṃsatrakośa** (áṃsatra-kośa) *adj.* having an armour for a bucket:
> droṇāhāvam avatam aśmacakram aṃsatrakośaṃ siñcatā nṛpāṇam. **ṚV. x. 101. 7.**

**ananuṣṭubha**, fascicle 4.1 (1990), page 1960, column a, record L=54507 (4-1960a).

> **अननुष्टुभ ananuṣṭubha** (an-anuṣṭubha) *adj.* which does not have (a verse in) anuṣṭubh:
> ananuṣṭubham etad ahar bhavati nānuṣṭubho 'dhīyate. **BaudhŚS. ii. 252. 10.**

**annaśalya**, fascicle 8.1 (2006), page 3849, column a, record L=97206 (8-3849a).

> **अन्नशल्य annaśalya** (anna-śalya) *n.* splinter in the form of food:
> annaśalyāni vamanāṅgulipratimarśaprabhṛtibhiḥ (patanti). **SuśruS. i. 27. 5.**

Each entry is two lines and is quoted in full with its locus.

## 7. Data and citation

- PD × DCS measurement data: [csl-atlas `data/pd/`](https://github.com/sanskrit-lexicon/csl-atlas/tree/main/data/pd)
- Canon ledger, every base and its percentage: [`pd_canon_ledger.tsv`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/data/pd/pd_canon_ledger.tsv)
- Coverage report: [PD_DCS_CORPUS_COVERAGE_2026.md](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/reports/PD_DCS_CORPUS_COVERAGE_2026.md)
- Machine-readable PD text: [PDScan 2020](https://sanskrit-lexicon.uni-koeln.de/scans/PDScan/2020/web/index.php)
- Front matter transcribed in this repository: [AOB](https://github.com/sanskrit-lexicon/PD/blob/main/AOB.md), [AUB](https://github.com/sanskrit-lexicon/PD/blob/main/AUB.md), [GA](https://github.com/sanskrit-lexicon/PD/blob/main/GA.md), [RG](https://github.com/sanskrit-lexicon/PD/blob/main/RG.md), [SWC](https://github.com/sanskrit-lexicon/PD/blob/main/SWC.md), [IW](https://github.com/sanskrit-lexicon/PD/blob/main/IW.md)
- Citable version of the data: [10.5281/zenodo.23613057](https://doi.org/10.5281/zenodo.23613057)

A number that cannot be traced to a committed source is a defect on this page. Corrections by pull
request or issue.

---

_Maintained by Dr. Mārcis Gasūns. This page is a reader-facing summary; the project's working record
is kept separately and is not published here._
