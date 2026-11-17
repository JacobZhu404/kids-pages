#!/usr/bin/env python3
"""Offline pre-deploy smoke checks for generated Cloudflare Pages files."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    pages = sorted(PUBLIC.rglob("*.html"))
    if not pages:
        fail("no HTML pages found")
    favicon = PUBLIC / "favicon.svg"
    eggy_css = PUBLIC / "assets/eggy.css"
    eggy_js = PUBLIC / "assets/eggy.js"
    for asset in (favicon, eggy_css, eggy_js):
        if not asset.is_file() or not asset.stat().st_size:
            fail(f"missing/empty asset: {asset.relative_to(ROOT)}")

    for page in pages:
        html = page.read_text(encoding="utf-8")
        rel = page.relative_to(PUBLIC)
        if html.count('rel="icon"') != 1:
            fail(f"{rel}: expected exactly one favicon link")
        if "<title>" not in html or "name=\"viewport\"" not in html or "charset=" not in html.lower():
            fail(f"{rel}: missing title, UTF-8 charset, or mobile viewport metadata")
        for meta in ('name="description"', 'name="theme-color"', 'property="og:title"'):
            if meta not in html:
                fail(f"{rel}: missing {meta}")
        if html.count('id="kg-eggy"') != 1:
            fail(f"{rel}: expected exactly one mascot")
        if html.count("/assets/eggy.js") != 1:
            fail(f"{rel}: expected one shared mascot script reference")
        if html.count("/assets/eggy.css") != 1:
            fail(f"{rel}: expected one shared mascot stylesheet reference")
        for match in re.finditer(r'(?:href|src)=["\']([^"\']+)["\']', html):
            url = match.group(1)
            if url.startswith(("https://", "http://", "data:", "#", "mailto:")):
                continue
            path = url.split("?", 1)[0].split("#", 1)[0]
            if not path:
                continue
            candidate = PUBLIC / path.lstrip("/") if path.startswith("/") else page.parent / path
            if not candidate.exists():
                fail(f"{rel}: broken local link {url}")
        scripts = re.findall(r'<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>', html, flags=re.S | re.I)
        for script in scripts:
            if not script.strip():
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8") as tmp:
                tmp.write(script)
                tmp.flush()
                result = subprocess.run(["node", "--check", tmp.name], capture_output=True, text=True)
                if result.returncode:
                    fail(f"{rel}: inline JavaScript syntax error: {result.stderr.strip()}")

    css_text = eggy_css.read_text(encoding="utf-8")
    if "#kg-eggy" not in css_text or "display:none" in css_text:
        fail("shared mascot CSS missing visibility rules")
    print(f"PASS: {len(pages)} pages, metadata, favicon, shared eggy assets, local links and inline JS")


if __name__ == "__main__":
    main()
