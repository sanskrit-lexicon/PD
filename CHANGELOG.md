_Created: 31-07-2026 · Last updated: 31-10-2026_

# Changelog

All notable changes to **PD** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- **Root restructure** (31-10-2026, GLM 5.3 Flash, 5 MG grill rulings — record in
  [`docs/DECISIONS_ROOT_RESTRUCTURE_2026-10-31.md`](docs/DECISIONS_ROOT_RESTRUCTURE_2026-10-31.md)):
  the 30 root files are down to 9 — 19 front-matter files (five KoshaSHRI PDFs + their
  `.md`/`_ocr.md` transcriptions, `ES.md`, `IW.md`, `IW.tsv`, `PREFACE.md`) moved into
  [`front_matter/`](front_matter) with `pref_manifests/` →
  [`front_matter/manifests/`](front_matter/manifests); comparison reports, the PWG bake-off
  artifacts, `HANDOFF_OCR_PD.md`, `about.md`, `aboutDictionary.md` and `RIGHTS.md` into
  [`docs/`](docs); the four root scripts and the probes (`tests/` → `scripts/tests/`) into
  [`scripts/`](scripts). Paths fixed in the same change: `run_ocr.py` resolves bare
  `--only` names against `front_matter/` and writes siblings there,
  `parse_pd_frontmatter.py` emits into `front_matter/`, and
  `compare_pwg_a_vs_b.py`'s output dir is no longer a hardcoded `C:\Users\...` path
  (now repo-relative). External deep links repointed in Uprava; one-line link-repair PRs
  opened on PWG/PWK `prefaces/METHODS.md`.
- **README refresh** (31-10-2026, GLM 5.3 Flash): repo map completed — comparison reports named,
  [`tests/`](scripts/tests/README.md) probes, `scripts/` changelog guards, `HANDOFF_OCR_PD.md` and
  `CITATION.cff` listed; new **CI** section documenting the four workflows (`validate`,
  `f821-gate`, `changelog-lint`, `dependabot-auto-merge`); `extract_html_pref.py` + the PE/BUR
  manifests described; remaining absolute self-links converted to relative links; knowledge-page
  line notes the 8 evidence-labelled sections.

### Added
- **Sourced knowledge page** (24-10-2026, DeepSeek Flash `deepseek-flash`; grown since — 8 sections
  as of 30-10-2026): `PD_KNOWLEDGE.md` —
  8 sections, each carrying an evidence label (`observed` / `derived` / `inferred` / `reviewed`);
  the canon ledger with every base that has been quoted and its 118/N; three verbatim entry exhibits
  with full loci; the do-not-quote list; a 10-row verification checklist. Every outbound link is
  public — 0 links into private repositories, 0 internal handoff IDs.
- **Essay + Index of Works front matter** (H6945, DeepSeek v4.1 Flash): `ES.md`
  (pp. I-XXVIII), `IW.md` (pp. LXXXIX-CXXVII), `IW.tsv` (subject-code × siglum
  index) and `parse_pd_frontmatter.py`, transcribed from the 2023-06-17 Internet
  Archive vol. 1 scan with SHA-256 pinning; manifest at
  `front_matter/manifests/pd_vol1_frontmatter_manifest.tsv`. No dictionary `.txt` touched.

- **Preface (pp. V–VI)** transcribed from the archive.org scan of Vol. 1 (1976),
  leaves 8–9, as [`PREFACE.md`](https://github.com/sanskrit-lexicon/PD/blob/main/front_matter/PREFACE.md)
  (Tesseract 5.5.3 `eng` base, manual collation against the page images; printed
  defects retained, damaged sorts restored where unambiguous). This is the one
  front-matter section that was not among the five KoshaSHRI PDFs.

## [0.1.0] - 2026-07-31

### Added
- **Initial changelog** (H2012 Phase F residual, Grok 4.5 `grok-4.5`): records current
  repository state after 7 commits since first recorded commit (2026-07-21). Historical
  detail was not reconstructed commit-by-commit; see `git log` for the full trail.

_Dr. Mārcis Gasūns_
