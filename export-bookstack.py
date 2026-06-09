#!/usr/bin/env python3
"""Export the SHHA BookStack guide to local Markdown and HTML files.

Environment:
  BOOKSTACK_TOKEN_ID
  BOOKSTACK_TOKEN_SECRET

Optional:
  BOOKSTACK_URL      default: https://wiki.sandiahomeowners.org
  BOOKSTACK_BOOK_ID  default: 1

The export is read-only. It writes:
  bookstack-current/manifest.json
  bookstack-current/book.md
  bookstack-current/pages-md/*.md
  bookstack-current/pages-html/*.html
"""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE_URL = os.environ.get("BOOKSTACK_URL", "https://wiki.sandiahomeowners.org").rstrip("/")
TOKEN_ID = os.environ.get("BOOKSTACK_TOKEN_ID", "")
TOKEN_SECRET = os.environ.get("BOOKSTACK_TOKEN_SECRET", "")
BOOK_ID = int(os.environ.get("BOOKSTACK_BOOK_ID", "1"))
OUTPUT_DIR = Path("bookstack-current")


@dataclass(frozen=True)
class PageRef:
    id: int
    name: str
    slug: str
    chapter: str
    chapter_slug: str
    priority: int
    url: str


def api_request(endpoint: str, *, accept: str = "application/json") -> bytes:
    if not TOKEN_ID or not TOKEN_SECRET:
        raise SystemExit("Set BOOKSTACK_TOKEN_ID and BOOKSTACK_TOKEN_SECRET.")

    request = urllib.request.Request(
        f"{BASE_URL}/api/{endpoint.lstrip('/')}",
        headers={
            "Authorization": f"Token {TOKEN_ID}:{TOKEN_SECRET}",
            "Accept": accept,
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read()
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"BookStack API error {error.code} for {endpoint}: {body}") from error


def api_json(endpoint: str) -> dict[str, Any]:
    return json.loads(api_request(endpoint).decode("utf-8"))


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "page"


def html_document(title: str, body_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape_html(title)}</title>
</head>
<body>
{body_html}
</body>
</html>
"""


def escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def page_refs(book: dict[str, Any]) -> list[PageRef]:
    refs: list[PageRef] = []
    for item in book.get("contents", []):
        item_type = item.get("type")
        if item_type == "chapter":
            chapter_name = item.get("name", "Unchaptered")
            chapter_slug = item.get("slug") or slugify(chapter_name)
            for page in item.get("pages", []):
                refs.append(
                    PageRef(
                        id=int(page["id"]),
                        name=page["name"],
                        slug=page.get("slug") or slugify(page["name"]),
                        chapter=chapter_name,
                        chapter_slug=chapter_slug,
                        priority=int(page.get("priority") or 0),
                        url=page.get("url", ""),
                    )
                )
        elif item_type == "page":
            refs.append(
                PageRef(
                    id=int(item["id"]),
                    name=item["name"],
                    slug=item.get("slug") or slugify(item["name"]),
                    chapter="Unchaptered",
                    chapter_slug="unchaptered",
                    priority=int(item.get("priority") or 0),
                    url=item.get("url", ""),
                )
            )
    return refs


def reset_output_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    (path / "pages-md").mkdir(parents=True)
    (path / "pages-html").mkdir(parents=True)


def write_page_exports(ref: PageRef, sequence: int, out_dir: Path) -> dict[str, Any]:
    detail = api_json(f"pages/{ref.id}")
    markdown = api_request(f"pages/{ref.id}/export/markdown", accept="application/octet-stream").decode(
        "utf-8", errors="replace"
    )
    raw_html = detail.get("raw_html") or detail.get("html") or ""

    filename_base = f"{sequence:02d}-{ref.slug}"
    md_path = out_dir / "pages-md" / f"{filename_base}.md"
    html_path = out_dir / "pages-html" / f"{filename_base}.html"

    md_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    html_path.write_text(html_document(ref.name, raw_html), encoding="utf-8")

    return {
        "id": ref.id,
        "name": ref.name,
        "slug": ref.slug,
        "chapter": ref.chapter,
        "priority": ref.priority,
        "updated_at": detail.get("updated_at"),
        "url": ref.url,
        "markdown": md_path.as_posix(),
        "html": html_path.as_posix(),
        "revision_count": detail.get("revision_count"),
    }


def write_combined_markdown(book: dict[str, Any], pages: list[dict[str, Any]], out_dir: Path) -> None:
    parts = [
        f"# {book.get('name', 'BookStack Export')}",
        "",
        f"Exported from {BASE_URL} on {datetime.now(timezone.utc).isoformat(timespec='seconds')}.",
        "",
    ]

    current_chapter = None
    for page in pages:
        if page["chapter"] != current_chapter:
            current_chapter = page["chapter"]
            parts.extend([f"## {current_chapter}", ""])
        markdown = Path(page["markdown"]).read_text(encoding="utf-8").strip()
        parts.extend([markdown, ""])

    (out_dir / "book.md").write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    os.chdir(root)

    book = api_json(f"books/{BOOK_ID}")
    refs = page_refs(book)
    reset_output_dir(OUTPUT_DIR)

    pages: list[dict[str, Any]] = []
    for index, ref in enumerate(refs, start=1):
        print(f"{index:02d}. Exporting {ref.name}")
        pages.append(write_page_exports(ref, index, OUTPUT_DIR))

    manifest = {
        "source": BASE_URL,
        "book_id": BOOK_ID,
        "book_name": book.get("name"),
        "book_updated_at": book.get("updated_at"),
        "exported_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pages": pages,
        "code_to_keep": [
            "export-bookstack.py",
            "README.md",
            "bookstack-current/",
            "guide/",
        ],
        "stale_assets_replaced": [
            "standalone top-level HTML pages",
            "standalone top-level Markdown pages",
            "one-off update/upload scripts with hard-coded BookStack IDs",
        ],
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    write_combined_markdown(book, pages, OUTPUT_DIR)

    print(f"Exported {len(pages)} pages to {OUTPUT_DIR}/")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
