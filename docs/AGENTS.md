# AGENTS.md — PD

_Created: 13-09-2026 · Last updated: 17-10-2026_

## Tool manifest

- Purpose: Cologne PWG-family OCR/dictionary source pack — AOB/AUB/GA/RG/SWC
  scanned `.pdf` + extracted `.md`, extraction/compare scripts
  (`.github/scripts/extract_html_pref.py`, `.github/scripts/compare_pwg_a_vs_b.py`).
- Harnesses: Claude Code / Codex / OpenCode / Grok (this AGENTS.md) — org
  default all four.
- CI: [dependabot-auto-merge.yml](https://github.com/sanskrit-lexicon/PD/blob/main/.github/workflows/dependabot-auto-merge.yml)
  (Dependabot) + [validate.yml](https://github.com/sanskrit-lexicon/PD/blob/main/.github/workflows/validate.yml)
  (Python byte-compile smoke on push/PR).
- Repo-level MCP: none carried (no `.mcp.json`).
- Landing route: foreign owner `sanskrit-lexicon` → PR only, human merges
  (no auto-merge).
- Census: tracked by [module-spread census v2](https://github.com/gasyoun/Uprava/blob/main/data/module_spread_census_v2.json)
  (`mcp_config` marker, H4525).

_Dr. Mārcis Gasūns_
