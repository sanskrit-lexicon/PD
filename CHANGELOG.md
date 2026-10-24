_Created: 31-07-2026 · Last updated: 18-10-2026_

# Changelog

All notable changes to **PD** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- **Sourced knowledge page** (24-10-2026, DeepSeek Flash `deepseek-flash`): `PD_KNOWLEDGE.md` —
  13 sections, each carrying an evidence label (`observed` / `derived` / `inferred` / `reviewed`);
  the canon ledger with every base that has been quoted and its 118/N; three verbatim entry exhibits
  with full loci; the do-not-quote list; a 10-row verification checklist. Every outbound link is
  public — 0 links into private repositories, 0 internal handoff IDs.
- **Essay + Index of Works front matter** (H6945, DeepSeek v4.1 Flash): `ES.md`
  (pp. I-XXVIII), `IW.md` (pp. LXXXIX-CXXVII), `IW.tsv` (subject-code × siglum
  index) and `parse_pd_frontmatter.py`, transcribed from the 2023-06-17 Internet
  Archive vol. 1 scan with SHA-256 pinning; manifest at
  `pref_manifests/pd_vol1_frontmatter_manifest.tsv`. No dictionary `.txt` touched.

- **Preface (pp. V–VI)** transcribed from the archive.org scan of Vol. 1 (1976),
  leaves 8–9, as [`PREFACE.md`](https://github.com/sanskrit-lexicon/PD/blob/main/PREFACE.md)
  (Tesseract 5.5.3 `eng` base, manual collation against the page images; printed
  defects retained, damaged sorts restored where unambiguous). This is the one
  front-matter section that was not among the five KoshaSHRI PDFs.

## [0.1.0] - 2026-07-31

### Added
- **Initial changelog** (H2012 Phase F residual, Grok 4.5 `grok-4.5`): records current
  repository state after 7 commits since first recorded commit (2026-07-21). Historical
  detail was not reconstructed commit-by-commit; see `git log` for the full trail.

_Dr. Mārcis Gasūns_
