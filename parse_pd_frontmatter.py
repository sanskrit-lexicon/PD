#!/usr/bin/env python3
"""Transcribe and parse the two front-matter blocks missing from the PD PDF set.

Source: Internet Archive item
  mAAY_an-encyclopaedic-dictionary-of-sanskrit-vol-1-critically-edited-by-a-m-ghatage-1
  (2023-06-17 upload, Satya Vrat Shastri collection), file `*_djvu.xml`
  sha256 5c5dbec140ad92da26b67bc769e9bae76e28ed63aaab124967bcc1e8fef2ce31

Outputs (run from the repo root):
  ES.md   Introductory Essay, pp. I-XXVIII
  IW.md   Index of Works Used in the Dictionary, pp. LXXXIX-CXXVII
  IW.tsv  subject-code x siglum index parsed from IW.md's source pages

The script is deliberately stdlib-only. The `--essay` / `--index` switches let a
reviewer regenerate one half without touching the other.

Usage:
  python parse_pd_frontmatter.py --djvu /path/to/vol1_djvu.xml --all
"""
from __future__ import annotations

import argparse
import hashlib
import html
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SOURCE_SHA256 = "5c5dbec140ad92da26b67bc769e9bae76e28ed63aaab124967bcc1e8fef2ce31"
SOURCE_URL = (
    "https://archive.org/download/"
    "mAAY_an-encyclopaedic-dictionary-of-sanskrit-vol-1-critically-edited-by-a-m-ghatage-1/"
    "An%20Encyclopaedic%20Dictionary%20Of%20Sanskrit%20Vol%201%20Critically%20Edited%20By%20A%20M%20Ghatage%2C%201976%20-%20Deccan%20College%20Post%20Graduate%20And%20Research%20Institute%2C%20Poona_djvu.xml"
)

# Leaf offsets in the IA scan (0-based <OBJECT> index). Verified by running
# headers and page numbers; see IW.md/IW.tsv `leaf` column.
ESSAY_LEAVES = list(range(10, 38))       # printed I-XXVIII
INDEX_LEAVES = list(range(98, 137))      # printed LXXXIX-CXXVII

ROMAN = {
    1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII",
    9: "IX", 10: "X", 11: "XI", 12: "XII", 13: "XIII", 14: "XIV", 15: "XV",
    16: "XVI", 17: "XVII", 18: "XVIII", 19: "XIX", 20: "XX", 21: "XXI",
    22: "XXII", 23: "XXIII", 24: "XXIV", 25: "XXV", 26: "XXVI", 27: "XXVII",
    28: "XXVIII",
}
INDEX_ROMAN = {i: ROMAN_N for i, ROMAN_N in {
    0: "LXXXIX", 1: "XC", 2: "XCI", 3: "XCII", 4: "XCIII", 5: "XCIV",
    6: "XCV", 7: "XCVI", 8: "XCVII", 9: "XCVIII", 10: "XCIX", 11: "C",
    12: "CI", 13: "CII", 14: "CIII", 15: "CIV", 16: "CV", 17: "CVI",
    18: "CVII", 19: "CVIII", 20: "CIX", 21: "CX", 22: "CXI", 23: "CXII",
    24: "CXIII", 25: "CXIV", 26: "CXV", 27: "CXVI", 28: "CXVII", 29: "CXVIII",
    30: "CXIX", 31: "CXX", 32: "CXXI", 33: "CXXII", 34: "CXXIII", 35: "CXXIV",
    36: "CXXV", 37: "CXXVI", 38: "CXXVII",
}.items()}

# ---------------------------------------------------------------------------
# Subject-wise Classification (PD/SWC.md, pp. LXXIII-LXXXI), manually collated.
# Code -> canonical printed name.
SUBJECTS = [
    ("1", "Samhitas"), ("2", "Brahmanas"), ("3", "Aranyakas"),
    ("4.1", "Major Upanisads"), ("4.2", "Minor Upanisads"),
    ("5", "Mantrapatha, Anukramanis etc."), ("6", "Srautasutras"),
    ("7", "Sulbasutras"), ("8", "Pitrmedhasutras"), ("9", "Grhyasutras"),
    ("10", "Nirukta"), ("11", "Pratigakhyas"), ("12", "Epics"),
    ("13", "Commentaries on the Mahabharata"), ("14", "Buddhism"),
    ("15", "Jainism (Dogmatics)"), ("16", "Jainism (Narrations)"),
    ("17", "Puranas"), ("18", "Tantras"), ("19", "Grammar (Paninian)"),
    ("20", "Grammar (Non-Paninian)"), ("21", "Linganushasanas"),
    ("22", "Sikshas"), ("23", "Lexicons"),
    ("24", "Commentaries on the Amarakosa"), ("25", "Philosophy (General)"),
    ("26", "Mimamsa"), ("27", "Vedanta"), ("27.1", "Vedanta (Sankara)"),
    ("27.2", "Vedanta (Bhaskara)"), ("27.3", "Vedanta (Ramanuja)"),
    ("27.4", "Vedanta (Anandatirtha)"), ("27.5", "Vedanta (Nimbarka)"),
    ("27.6", "Vedanta (Srikantha)"), ("27.7", "Vedanta (Vallabha)"),
    ("27.8", "Vedanta (Govinda)"), ("27.9", "Vedanta (Srikara)"),
    ("28", "Bhakti"), ("29", "Trika, etc."), ("30", "Samkhya"), ("31", "Yoga"),
    ("32", "Nyaya"), ("33", "Vaisesika"), ("34", "Nyayavaisesika"),
    ("35", "Dharmasutras"), ("36", "Dharma"), ("37", "Nibandha"),
    ("38", "Arthasastra"), ("39", "Minor sciences"),
    ("39.1", "Veterinary Science, Archery"), ("39.2", "Agriculture"),
    ("39.3", "Sports"), ("40", "Samgita"), ("41", "Silpa"), ("42", "Medicine"),
    ("43", "Kama"), ("44", "Mathematics"), ("45", "Astronomy"),
    ("46", "Astrology"), ("47", "Alchemy"), ("48", "Poetics"),
    ("49", "Dramaturgy"), ("50", "Nrtya"), ("51", "Prosody"), ("52", "Kavyas"),
    ("53", "Historical Poems"), ("54", "Minor Poems"), ("54.1", "Satakas etc."),
    ("54.2", "Laharis"), ("54.3", "Citakavyas"),
    ("54.4", "Stotras, Stavas etc."), ("54.5", "Other Poems"),
    ("55", "Anthology"), ("56", "Brhatkatha and connected Works"),
    ("57", "Stories and Romances"), ("58", "Campu"), ("59", "Drama"),
    ("60", "Farces"), ("61", "Allegorical plays"), ("62", "Inscriptions"),
]

ALIASES = {
    "samhitas": "1", "brahmanas": "2", "aranyakas": "3",
    "major upanisads": "4.1", "minor upanisads": "4.2",
    "mantrapatha anukramanis etc": "5", "srautasutras": "6",
    "sulbasutras": "7", "pitrmedhasutras": "8", "grhyasutras": "9",
    "nirukta": "10", "pratigakhyas": "11", "epics": "12",
    "commentaries on the mahabharata": "13", "buddhism": "14",
    "jainism dogmatics": "15", "jainism narrations": "16", "puranas": "17",
    "tantras": "18", "grammar paninian": "19", "grammar non paninian": "20",
    "linganushasanas": "21", "linganudaisanas": "21", "sikshas": "22",
    "siksis": "22", "siksas": "22", "lexicons": "23",
    "commentaries on the amarakosa": "24", "philosophy general": "25",
    "mimamsa": "26", "mimarnsa": "26", "vedanta": "27",
    "vedanta sankara": "27.1", "vedanta bhaskara": "27.2",
    "vedanta ramanuja": "27.3", "vedanta anandatirtha": "27.4",
    "vedanta nimbarka": "27.5", "vedanta srikantha": "27.6",
    "vedanta vallabha": "27.7", "vedanta govinda": "27.8",
    "vedanta srikara": "27.9", "bhakti": "28", "trika etc": "29",
    "samkhya": "30", "yoga": "31", "nyaya": "32", "vaisesika": "33",
    "nyayavaisesika": "34", "dharmasutras": "35", "dharma": "36",
    "nibandha": "37", "arthasastra": "38", "minor sciences": "39",
    "veterinary science archery": "39.1", "agriculture": "39.2",
    "sports": "39.3", "samgita": "40", "silpa": "41", "medicine": "42",
    "kama": "43", "mathematics": "44", "astronomy": "45", "astrology": "46",
    "alchemy": "47", "poetics": "48", "dramaturgy": "49", "nrtya": "50",
    "prosody": "51", "kavyas": "52", "historical poems": "53",
    "minor poems": "54", "satakas etc": "54.1", "laharis": "54.2",
    "citakavyas": "54.3", "stotras stavas etc": "54.4", "other poems": "54.5",
    "anthology": "55", "antholog": "55",
    "brhatkatha and connected works": "56", "stories and romances": "57",
    "campu": "58", "drama": "59", "dramas": "59", "farces": "60",
    "allegorical plays": "61", "inscriptions": "62",
}
CODE_NAME = dict(SUBJECTS)

# Conservative OCR corrections: whole words/tokens only, each one visible in the
# source. Anything uncertain is left as OCR and marked in the file header.
CORRECTIONS = [
    (r"\bio\b", "to"), (r"\bihe\b", "the"), (r"\bihcir\b", "their"),
    (r"\bitis\b", "it is"), (r"\bsiands\b", "stands"), (r"\bgrowih\b", "growth"),
    (r"\bofthe\b", "of the"), (r"\binits\b", "in it"), (r"\bvecables\b", "vocables"),
    (r"\bHstorical\b", "Historical"), (r"\bJanguage\b", "language"),
    (r"\bAITKEN\b", "AITKEN"), (r"\bSonnENSEN\b", "SØRENSEN"),
    (r"\bsyniactical\b", "syntactical"), (r"\bexam ple\b", "example"),
    (r"\bctionaries\b", "dictionaries"), (r"\bBeryrey\b", "Benfey"),
    (r"\bTtihav\b", "Itihasa"), (r"\bArya\$\b", "AryaS."),
]

BJ = r"[A-Za-zĀāĪīŪūṚṛṜṝḶḷṂṃṆṇÑñŚśṢṣṬṭḌḍ]"
SIGLUM_RE = re.compile(BJ + r"[A-Za-zĀāĪīŪūṚṛṜṝḶḷṂṃṆṇÑñŚśṢṣṬṭḌḍ.\-]{1,30}")


def norm(s: str) -> str:
    s = s.lower()
    for a, b in (("ś", "s"), ("ṣ", "s"), ("ā", "a"), ("ī", "i"), ("ū", "u")):
        s = s.replace(a, b)
    s = re.sub(r"[^a-z0-9. ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def subject_hits(text: str):
    """Return non-overlapping canonical subject occurrences: (code, alias)."""
    ntext = norm(text)
    hits = []
    for alias, code in ALIASES.items():
        for m in re.finditer(r"(?<![a-z])" + re.escape(alias) + r"(?![a-z])", ntext):
            hits.append((m.start(), m.end(), code, alias))
    hits.sort(key=lambda h: (h[0], -(h[1] - h[0])))
    clean, last = [], -1
    for start, end, code, alias in hits:
        if start >= last:
            clean.append((code, alias))
            last = end
    return clean


def clean_sigla(text: str):
    out = []
    for m in SIGLUM_RE.finditer(text):
        tok = m.group(0).strip(".-")
        if len(tok) < 2 or tok.lower() in {"subject", "abbreviation", "abbrev"}:
            continue
        if tok.islower():
            continue
        out.append(tok)
    return out


@dataclass
class Block:
    x: int
    y: int
    lines: list = field(default_factory=list)

    @property
    def text(self):
        return " ".join(" ".join(w[2] for w in ln) for ln in self.lines)


def parse_blocks(obj: str):
    blocks = []
    for col in re.findall(r"<PAGECOLUMN>(.*?)</PAGECOLUMN>", obj, re.S):
        lines = []
        for line in re.findall(r"<LINE>(.*?)</LINE>", col, re.S):
            words = [
                (int(m.group(1)), int(m.group(2)), html.unescape(m.group(3)))
                for m in re.finditer(
                    r'<WORD coords="(\d+),(\d+),[^"]*"[^>]*>(.*?)</WORD>', line, re.S)
            ]
            if words:
                lines.append(words)
        if lines:
            blocks.append(Block(min(w[0] for w in lines[0]),
                                min(w[1] for w in lines[0]), lines))
    return blocks


def page_lines(obj: str):
    """Reading order for prose pages: left column, then right column."""
    blocks = parse_blocks(obj)
    if not blocks:
        return []
    rows = []
    for b in blocks:
        for ln in b.lines:
            x = min(w[0] for w in ln)
            y = min(w[1] for w in ln)
            text = " ".join(w[2] for w in ln).strip()
            if text:
                rows.append((x, y, text))
    xs = [r[0] for r in rows]
    mid = (min(xs) + max(xs)) / 2
    two_col = (max(xs) - min(xs)) > 700
    rows.sort(key=lambda r: (0 if (two_col and r[0] < mid) else 1, r[1], r[0]))
    return [r[2] for r in rows]


def apply_corrections(lines):
    out = []
    for line in lines:
        for pat, repl in CORRECTIONS:
            line = re.sub(pat, repl, line)
        out.append(line)
    return out


def write_essay(objs, root: Path):
    parts = [
        "# Introductory Essay (pp. I-XXVIII)",
        "",
        "_Transcribed from the 2023-06-17 Internet Archive scan of vol. 1 "
        "(identifier `mAAY_an-encyclopaedic-dictionary-of-sanskrit-vol-1-critically-edited-by-a-m-ghatage-1`). "
        "OCR: IA djvu layer; manual collation: section headings, page numbers and a "
        "conservative whole-token correction list in `parse_pd_frontmatter.py`._",
        "",
        "<!-- provenance: source=archive.org vol. 1 djvu.xml; "
        f"sha256={SOURCE_SHA256}; leaves=10-37; printed=I-XXVIII; "
        "engine=IA OCR; collation=light (headings/page numbers/obvious tokens) -->",
        "",
        "Page numbers are the printed roman numerals. Text remains OCR: the "
        "two-column pages XII-XXVIII retain column-order noise where the scan's "
        "line bands merged. Do not cite a reading from this file without checking "
        "the scan.",
        "",
        "## Sections (printed headings, collated)",
        "",
        "| Section | Heading | Printed page |",
        "|---|---|---|",
        "| 1 | INTRODUCTION | I |",
        "| 2 | THE PRINCIPLES OF A HISTORICAL DICTIONARY | I |",
        "| 3 | A SURVEY OF LEXICAL MATERIAL FOR SANSKRIT | IV |",
        "| 4 | (heading lost in the OCR of the two-column pp. V-XI; the argument runs to p. XI) | V-XI |",
        "| 5 | THE ARTICLE — the 13-point scheme for a PD article (item 12: indication "
        "of compound formation; item 13: statistical information) | XII |",
        "| 6 | THE TECHNICAL ASPECTS OF A SANSKRIT HISTORICAL DICTIONARY | XXIII |",
        "",
        "Consumer note: section 5 is the locus for the compound rule used by "
        "[`PD_COMPOUND_RULE_17-10-2026.md`](https://github.com/gasyoun/Uprava/blob/main/papers/A68/PD_COMPOUND_RULE_17-10-2026.md). "
        "The OCR of pp. XII-XIII is interleaved; the scheme is retained verbatim "
        "under the page marker rather than silently reflowed.",
        "",
    ]
    for offset, leaf in enumerate(ESSAY_LEAVES, start=1):
        lines = apply_corrections(page_lines(objs[leaf]))
        # Drop running heads (bare roman numeral / short running title).
        if lines and re.fullmatch(r"[—\-\s]*[ivxlIVXL]+[\s—\-]*", lines[0]):
            lines = lines[1:]
        parts.append(f"## Page {ROMAN[offset]} (leaf {leaf})")
        parts.append("")
        parts.extend(lines)
        parts.append("")
    (root / "ES.md").write_text("\n".join(parts), encoding="utf-8")


def index_page_pairs(obj: str):
    """Extract (code, subject, siglum, method) pairs from one index page."""
    blocks = parse_blocks(obj)
    merged = [b for b in blocks
              if 1000 <= b.x < 1520 and re.search(r"Subject", b.text, re.I)
              and re.search(r"Ab(?:br|ly)?[a-z]*viation", b.text, re.I)]
    pairs = []
    if merged:
        alias_tokens = {tuple(alias.split()): code for alias, code in ALIASES.items()}
        for b in sorted(merged, key=lambda b: b.y):
            raw_text = b.text
            start_row = len(pairs)
            toks = norm(raw_text).split()
            i = 0
            while i < len(toks):
                matched = False
                for n in range(min(6, len(toks) - i), 0, -1):
                    key = tuple(toks[i:i + n])
                    if key in alias_tokens:
                        pairs.append((alias_tokens[key], CODE_NAME[alias_tokens[key]],
                                      "", "merged-block"))
                        i += n
                        matched = True
                        break
                if matched:
                    continue
                tok = toks[i]
                if (len(tok) >= 2 and re.fullmatch(r"[a-z0-9.\-]+", tok)
                        and ("." in tok or len(tok) >= 4)
                        and tok not in {"subject", "abbreviation", "abbrev"}
                        and pairs and not pairs[-1][2]):
                    code, subject, _, method = pairs[-1]
                    pairs[-1] = (code, subject, tok.strip(".-"), method)
                i += 1
            # Restore the printed case of sigla (norm() lowercased them).
            cursor = 0
            for row_i in range(start_row, len(pairs)):
                code, subject, sig, method = pairs[row_i]
                if not sig:
                    continue
                m = re.search(re.escape(sig), raw_text[cursor:], re.I)
                if m:
                    raw_sig = m.group(0)
                    pairs[row_i] = (code, subject, raw_sig, method)
                    cursor += m.end()
        if pairs:
            return pairs

    subj_blocks = [b for b in blocks if 1000 <= b.x < 1520]
    abbr_blocks = [b for b in blocks if b.x >= 1520]
    subj_text = " ".join(b.text for b in sorted(subj_blocks, key=lambda b: b.y))
    abbr_text = " ".join(b.text for b in sorted(abbr_blocks, key=lambda b: b.y))
    subjects = subject_hits(subj_text)
    sigla = clean_sigla(abbr_text)
    if not subjects:
        return pairs
    if not sigla:
        return [(code, CODE_NAME.get(code, alias), "", "subject-only")
                for code, alias in subjects]
    for i, (code, alias) in enumerate(subjects):
        method = "columns" if len(subjects) == len(sigla) else "columns-partial"
        pairs.append((code, CODE_NAME.get(code, alias),
                      sigla[i] if i < len(sigla) else "", method))
    return pairs


def write_index(objs, root: Path):
    md = [
        "# Index of Works Used in the Dictionary (pp. LXXXIX-CXXVII)",
        "",
        "_Transcribed from the 2023-06-17 Internet Archive scan of vol. 1 "
        "(identifier `mAAY_an-encyclopaedic-dictionary-of-sanskrit-vol-1-critically-edited-by-a-m-ghatage-1`). "
        "OCR: IA djvu layer, re-ordered by text-block column; manual collation: page "
        "numbers, the five column headings, the 62 subject names, and the "
        "subject/siglum pairing in `IW.tsv`. The printed table has five columns: "
        "Name of the Book | Name of the Author | Nature, Other Name, etc. | Subject | "
        "Abbreviation. This rendering keeps the OCR column blocks separate rather "
        "than inventing row alignment where the scan's line bands were merged._",
        "",
        "<!-- provenance: source=archive.org vol. 1 djvu.xml; "
        f"sha256={SOURCE_SHA256}; leaves=98-136; printed=LXXXIX-CXXVII; "
        "engine=IA OCR; collation=page/headings/subject names/siglum pairing -->",
        "",
        "The machine-readable derivative is [`IW.tsv`](IW.tsv): one row per subject "
        "code x siglum pair, with the printed page and the pairing method. Alignment "
        "noise is explicit in that column; rows with an empty siglum were not paired.",
        "",
    ]
    rows = ["printed_page\tleaf\tsubject\tsubject_code\tsiglum\tpair_method"]
    for offset, leaf in enumerate(INDEX_LEAVES):
        blocks = parse_blocks(objs[leaf])
        page = INDEX_ROMAN[offset]
        md.append(f"## Page {page} (leaf {leaf})")
        md.append("")
        cols = {
            "Name of the Book": [b for b in blocks if 80 < b.x < 400],
            "Name of the Author": [b for b in blocks if 400 <= b.x < 750],
            "Nature, Other Name, etc.": [b for b in blocks if 750 <= b.x < 1050],
            "Subject": [b for b in blocks if 1050 <= b.x < 1520],
            "Abbreviation": [b for b in blocks if b.x >= 1520],
        }
        for title, bs in cols.items():
            if not bs:
                continue
            md.append(f"**{title}**")
            md.append("")
            for b in sorted(bs, key=lambda b: b.y):
                if b.text.strip().lower() == title.lower():
                    continue
                md.append(b.text)
                md.append("")
        for code, subject, siglum, method in index_page_pairs(objs[leaf]):
            rows.append(f"{page}\t{leaf}\t{subject}\t{code}\t{siglum}\t{method}")
    md.append("_Dr. Mārcis Gasūns_")
    md.append("")
    (root / "IW.md").write_text("\n".join(md), encoding="utf-8")
    (root / "IW.tsv").write_text("\n".join(rows) + "\n", encoding="utf-8")
    man = ["printed_page\tleaf\tsection\tfile"]
    for offset, leaf in enumerate(ESSAY_LEAVES, start=1):
        man.append(f"{ROMAN[offset]}\t{leaf}\tEssay\tES.md")
    for offset, leaf in enumerate(INDEX_LEAVES):
        man.append(f"{INDEX_ROMAN[offset]}\t{leaf}\tIndex of Works\tIW.md")
    (root / "pref_manifests" / "pd_vol1_frontmatter_manifest.tsv").write_text(
        "\n".join(man) + "\n", encoding="utf-8")
    filled = sum(1 for r in rows[1:] if r.split("\t")[4])
    print(f"IW.tsv: {len(rows)-1} rows, {filled} with a siglum", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--djvu", required=True)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--essay", action="store_true")
    ap.add_argument("--index", action="store_true")
    ap.add_argument("--root", default=".")
    args = ap.parse_args()

    raw = Path(args.djvu).read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != SOURCE_SHA256:
        sys.exit(f"refusing: djvu.xml sha256 {got} != pinned {SOURCE_SHA256}")
    text = raw.decode("utf-8", errors="replace")
    objs = re.findall(r"<OBJECT\b.*?</OBJECT>", text, re.S)
    if len(objs) != 864:
        sys.exit(f"refusing: expected 864 leaves, got {len(objs)}")

    root = Path(args.root)
    do_essay = args.all or args.essay
    do_index = args.all or args.index
    if not (do_essay or do_index):
        sys.exit("pick --essay, --index or --all")
    if do_essay:
        write_essay(objs, root)
        print("wrote ES.md", file=sys.stderr)
    if do_index:
        write_index(objs, root)


if __name__ == "__main__":
    main()
