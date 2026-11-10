#!/usr/bin/env python3
"""Focused coverage/link checks for the vol.-1 front-matter pack (H7970).

Stdlib-only. Run from the repo root:

    python .github/scripts/check_frontmatter_pack.py

Checks:
  1. front_matter/AA.md <-> front_matter/AA.tsv parity: same entry count and the same
     (abbreviation, expansion, note) content in the same order (37 entries).
  2. The manifest carries the CXXVIII row for front_matter/AA.md with leaf 139.
  3. README.md links front_matter/AA.md and AA.tsv, and both targets exist on disk.
  4. AA.md provenance carries the pinned djvu.xml sha256 and the verified leaf 139.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PINNED_SHA256 = "5c5dbec140ad92da26b67bc769e9bae76e28ed63aaab124967bcc1e8fef2ce31"


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main() -> int:
    failures = []
    tsv_path = ROOT / "front_matter" / "AA.tsv"
    md_path = ROOT / "front_matter" / "AA.md"
    man_path = ROOT / "front_matter" / "manifests" / "pd_vol1_frontmatter_manifest.tsv"
    readme_path = ROOT / "README.md"

    # 1. MD <-> TSV parity -----------------------------------------------
    with tsv_path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.reader(fh, delimiter="\t"))
    header, data = rows[0], rows[1:]
    expected_header = ["printed_page", "leaf", "abbreviation", "expansion", "note"]
    if header[:5] != expected_header:
        failures.append(f"AA.tsv header {header[:5]} != {expected_header}")

    tsv_entries = []
    for r in data:
        if not r or not r[0]:
            continue
        r = r + [""] * (5 - len(r))
        if r[0] != "CXXVIII" or r[1] != "139":
            failures.append(f"AA.tsv row not CXXVIII/139: {r[:2]}")
        tsv_entries.append((norm(r[2]), norm(r[3]), norm(r[4])))

    md_entries = []
    in_table = False
    for line in md_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("| Abbreviation | Expansion | Note |"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            if re.fullmatch(r"\|[\s\-|]+\|", line):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            cells += [""] * (3 - len(cells))
            md_entries.append((norm(cells[0]), norm(cells[1]), norm(cells[2])))

    if len(tsv_entries) != len(md_entries):
        failures.append(
            f"entry count differs: AA.tsv {len(tsv_entries)} vs AA.md {len(md_entries)}")
    else:
        for i, (t, m) in enumerate(zip(tsv_entries, md_entries), 1):
            if t != m:
                failures.append(f"entry {i} differs: tsv={t!r} md={m!r}")
    if len(tsv_entries) != 37:
        failures.append(f"expected 37 entries in AA.tsv, got {len(tsv_entries)}")

    # 2. manifest row ----------------------------------------------------
    man_rows = [ln.split("\t") for ln in
                man_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    want = ["CXXVIII", "139", "Additional Abbreviations", "front_matter/AA.md"]
    if want not in [r[:4] for r in man_rows]:
        failures.append(f"manifest missing row {want}")

    # 3. README links + targets -----------------------------------------
    readme = readme_path.read_text(encoding="utf-8")
    for rel in ("front_matter/AA.md", "front_matter/AA.tsv"):
        if f"]({rel})" not in readme:
            failures.append(f"README does not link {rel}")
        if not (ROOT / rel).exists():
            failures.append(f"missing file {rel}")

    # 4. provenance pin + leaf ------------------------------------------
    md = md_path.read_text(encoding="utf-8")
    if PINNED_SHA256 not in md:
        failures.append("AA.md provenance lacks the pinned djvu.xml sha256")
    if "leaf=139" not in md:
        failures.append("AA.md provenance lacks leaf=139")

    if failures:
        for f in failures:
            print(f"FAIL {f}")
        return 1
    print(f"PASS AA.md <-> AA.tsv parity ({len(tsv_entries)} entries)")
    print("PASS manifest row CXXVIII 139 -> front_matter/AA.md")
    print("PASS README links resolve")
    print("PASS AA.md provenance pin + leaf")
    return 0


if __name__ == "__main__":
    sys.exit(main())
