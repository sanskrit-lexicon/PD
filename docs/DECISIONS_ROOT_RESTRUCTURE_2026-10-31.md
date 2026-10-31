# Decisions — root restructure grill, 31-10-2026

_Created: 31-10-2026 · Executor: GLM 5.3 Flash (zai-coding-plan/glm-5.3-flash) · Rulings: MG, live via the grillme interactive pass._

Five rulings from the /grillme round that shaped this restructure. Homework sources are
named per ruling; the estate surfaces consulted were the repo itself at `main` `cbd6152`,
`Uprava` (deep-link grep, `PROJECT_INTERLINKS.md`, `DATA_LAYERS_CENSUS.md` §9, handoffs
H5604/H6945/H7494/H7568), `gh` code search across `sanskrit-lexicon`, and PR #30.

## R1 — Landing route: PR now, rebase after PR #30

One restructure PR off fresh `main`, opened now. PR #30 (README citation-flow figure,
`figures/`) also touches `README.md`/`CHANGELOG.md`: MG merges #30 first, the restructure
branch is rebased onto it afterwards, conflicts resolved once. The stale local branch
`docs/readme-refresh` (its commit was already merged as PR #29) was deleted.

## R2 — Layout: three new dirs, tests nested under scripts

- `front_matter/` — the five KoshaSHRI PDFs (`GA`/`AUB`/`RG`/`SWC`/`AOB`) with their
  `.md` + `_ocr.md` transcriptions (15 files), plus `ES.md`, `IW.md`, `IW.tsv`,
  `PREFACE.md`; `pref_manifests/` → `front_matter/manifests/`.
- `docs/` — `about.md`, `aboutDictionary.md`, `RIGHTS.md`, `HANDOFF_OCR_PD.md`, both
  `COMPARISON_*.md` reports, and `pwg_a_vs_b/` (bake-off artifacts) → `docs/pwg_a_vs_b/`.
- `scripts/` — the four root scripts move in; `tests/` → `scripts/tests/`.
- Root keeps only: `README.md`, `CHANGELOG.md`, `LICENSE`, `SECURITY.md`, `CITATION.cff`,
  `AGENTS.md`, `.ai_state.md`, `.gitignore`, `.pre-commit-config.yaml`, `.github/`,
  `PRESS/`, `PD_KNOWLEDGE.md` (see R4) — 12 items, plus `figures/` when PR #30 lands.
- Homework: `run_ocr.py` `DEFAULT_PDFS` + sibling-output logic, `parse_pd_frontmatter.py`
  outputs, tests opening `GA.pdf` from repo root — all path-coupled and fixed in the same
  change; CI (`compileall`, `ruff`, changelog guards) is layout-agnostic.

## R3 — External links: move all, repair every link

The 35 Uprava deep links (AOB.md ×6, AUB.md ×5, GA.md ×2, GA.pdf, both COMPARISON
reports, `PD_KNOWLEDGE.md` ×3, `run_ocr.py`, plus 10 `PRESS/` links that the move does
not touch) are repointed — active `papers/A68/` surfaces and archived handoffs alike —
and one-line link-repair PRs go to PWG and PWK `prefaces/METHODS.md`
(`COMPARISON_PWG_OCR_A_VS_B.md` → `docs/…`). GitHub does not redirect git-moved files.

## R4 — Placement refinements

- `PD_KNOWLEDGE.md` stays at repo root: the 17-10-2026 Q1–Q3 ruling
  (`Uprava/decide_briefs/DECIDE_BRIEF_pd-page-q1-q3_17-10-2026.md`) made it the standalone
  public surface, and the root should showcase it.
- `*_ocr.md` baselines sit inside `front_matter/` beside their `.md` outputs — the
  pair adjacency serves the diff workflow the README documents.

## R5 — Transcription

This file is the dated decisions record; the PR description carries the same summary;
`CHANGELOG.md` [Unreleased] documents the change; `.ai_state.md` carries the journal row
and the `@WAITING` rebase-after-#30 queue item; Uprava GTD rows track the two PWG/PWK
link-repair PRs (they outlive this session).

## R6 — Folder nesting follow-up (MG ruling, 31-10-2026, after PR #31 merged)

Direct MG instruction, no grill needed:

- `figures/a68_fig5_citation_flow.svg` → [`docs/a68_fig5_citation_flow.svg`](a68_fig5_citation_flow.svg) — the `figures/` dir dissolves.
- `PRESS/OUTLOOK_2003-12-01_KABRA_DICTIONARYAHA.md` → [`docs/OUTLOOK_2003-12-01_KABRA_DICTIONARYAHA.md`](OUTLOOK_2003-12-01_KABRA_DICTIONARYAHA.md) — the `PRESS/` dir dissolves. (The 10 Uprava deep links into `PRESS/` are re-repointed in the same open Uprava PR.)
- `scripts/` → `.github/scripts/` — the root loses its last code dir. `changelog-lint.yml`'s two steps repointed; `compare_pwg_a_vs_b.py`'s repo-root computation adjusted (`parents[2]`); the probe tests stay CWD-relative (run from the repo root).
- ⚠️ parked to MG: `changelog-lint.yml` and its two guard scripts are deployed per-repo by `Uprava/tools/cologne_batch_deploy.py` from `github-spine/changelog_guard/` ("do not fork them per repo") — a future redeploy may revert the `.github/scripts/` paths; the deploy template needs the new location.
- Root after: 10 files + 3 dirs (`.github/`, `docs/`, `front_matter/`).

## R7 — Convention files move + release cut (MG ruling, 31-10-2026, R6 follow-up)

Direct MG instruction:

- `SECURITY.md`, `LICENSE`, `CHANGELOG.md`, `AGENTS.md` → `docs/` — GitHub still detects the
  security policy and the license from `docs/`.
- `.gitignore` and `.pre-commit-config.yaml` → `.github/`.
- `CHANGELOG.md` release cut: everything from `[Unreleased]` became **`[0.2.0] - 2026-10-31`**
  (empty `[Unreleased]` kept, Keep-a-Changelog style). No git tag / GitHub Release was cut —
  tagging mints a new Zenodo version DOI and the DOI reconciliation (CITATION.cff `23151371`
  vs knowledge page `23613057`) is still parked to MG.

Caveats (each is a functional trade-off accepted by the ruling, flagged for MG):

- **`.github/.gitignore` scopes only `.github/`** — git ignores a `.gitignore` outside the root
  for its own subtree, so root-level `__pycache__/` noise returns (H5604's repo-wide ignore no
  longer functions from the new location). One-word fix if it bites: move the file back.
- **pre-commit** config discovery expects a root config — local runs need
  `pre-commit run -c .github/.pre-commit-config.yaml` (or `pre-commit install -c …`).
- **The changelog guards go dormant** — both `changelog_*.py` scripts look for the changelog at
  the repo root only and fail open ("no changelog found — nothing to check") until the
  `github-spine/changelog_guard/` deploy template learns the `docs/` location (same parked
  template as R6).
- **`SECURITY.md` is a deployed copy** (`cologne_batch_deploy.py`, security-md row, H7156 —
  "edit the row, not each repository's copy") — a redeploy would recreate a root copy unless the
  template learns `docs/`.

- Root after: 4 files (`.ai_state.md`, `CITATION.cff`, `PD_KNOWLEDGE.md`, `README.md`) + 3 dirs.

---

_Dr. Mārcis Gasūns_
