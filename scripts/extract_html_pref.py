"""Extract CDSL pref pages that are HTML text layers (not multi-scan toctrees)."""
from __future__ import annotations

import re
import sys
import html as htmllib
from pathlib import Path
from urllib.request import Request, urlopen

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BASE = "https://sanskrit-lexicon.uni-koeln.de/scans/csldev/csldoc/build/dictionaries/prefaces"

CODES = {
    "ap90": Path(r"C:\Users\user\Documents\GitHub\AP90\prefaces"),
    "ae": Path(r"C:\Users\user\Documents\GitHub\prefaces_ae\prefaces"),
    "ben": Path(r"C:\Users\user\Documents\GitHub\BEN\prefaces"),
    "acc": Path(r"C:\Users\user\Documents\GitHub\ACC\prefaces"),
}


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 cologne-preface-ocr"})
    with urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8", errors="replace")


def strip_tags(s: str) -> str:
    s = re.sub(r"(?is)<script[^>]*>.*?</script>", " ", s)
    s = re.sub(r"(?is)<style[^>]*>.*?</style>", " ", s)
    s = re.sub(r"(?is)<br\s*/?>", "\n", s)
    s = re.sub(r"(?is)</(p|div|li|h\d|tr)>", "\n", s)
    s = re.sub(r"(?is)<li[^>]*>", "- ", s)
    s = re.sub(r"(?is)<[^>]+>", "", s)
    s = htmllib.unescape(s)
    s = s.replace("\r", "")
    s = re.sub(r"[ \t]+\n", "\n", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def sections_from_html(html: str) -> list[tuple[str, str]]:
    m = re.search(r'(?is)<div class="body"[^>]*>(.*?)<div class="clearer"', html)
    body = m.group(1) if m else html
    parts = re.split(r"(?is)<h1[^>]*>", body)
    secs: list[tuple[str, str]] = []
    for p in parts[1:]:
        hm = re.match(r"(?is)(.*?)</h1>(.*)$", p, re.S)
        if not hm:
            continue
        title = strip_tags(hm.group(1))
        title = re.sub(r"¶", "", title).strip()
        content = strip_tags(hm.group(2))
        content = re.split(r"(?im)^Previous\s*\||^Next\s*\||©\.\s*\|", content)[0].strip()
        if title:
            secs.append((title, content))
    return secs


def main() -> None:
    for code, outdir in CODES.items():
        url = f"{BASE}/{code}pref.html"
        print(f"=== {code} {url}", flush=True)
        try:
            html = fetch(url)
        except Exception as e:
            print(f"  FETCH FAIL: {e}", flush=True)
            continue
        secs = sections_from_html(html)
        print(f"  sections={len(secs)}", flush=True)
        outdir.mkdir(parents=True, exist_ok=True)
        (outdir / "scans").mkdir(exist_ok=True)
        for i, (title, content) in enumerate(secs, 1):
            nn = f"{i:02d}"
            slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
            md = (
                f"---\n"
                f"source_scan: (html text layer; no per-page PNG for {code})\n"
                f"source_page: {title}\n"
                f"volume: 1\n"
                f"source_url: {url}#{slug}\n"
                f"extraction: csldoc-html-text\n"
                f"---\n\n"
                f"# {title}\n\n"
                f"{content}\n"
            )
            path = outdir / f"{code}pref{nn}.md"
            path.write_text(md, encoding="utf-8")
            print(f"  wrote {path.name} ({len(content)} chars) — {title[:70]}", flush=True)
        lines = [
            f"# {code.upper()} — Front matter (from csldoc HTML text layer)",
            "",
            f"_Created: 23-07-2026 · Last updated: 23-07-2026_",
            "",
            f"Extracted from [{code}pref.html]({url}).",
            "Source language: **English** (HTML already transcribed in csl-doc — not scan-band vision OCR).",
            "Russian translations: add as `.ru.md` (Phase 4).",
            "",
            "| NN | Section | Source |",
            "|---|---|---|",
        ]
        for i, (title, _) in enumerate(secs, 1):
            nn = f"{i:02d}"
            lines.append(f"| {nn} | {title} | [{code}pref{nn}.md]({code}pref{nn}.md) |")
        lines.append("")
        lines.append("_Dr. Mārcis Gasūns_")
        lines.append("")
        (outdir / "README.md").write_text("\n".join(lines), encoding="utf-8")
        print("  README written", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
