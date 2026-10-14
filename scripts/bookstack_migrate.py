#!/usr/bin/env python3
"""Import a live portable BookStack ZIP and verify it through the target API.

Uses only Python's standard library. Credentials and reports belong outside Git.
An import requires an empty target and is never blindly retried after a timeout.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import secrets
import tempfile
from typing import Any
import urllib.error
import urllib.parse
import urllib.request
import zipfile


class MigrationError(RuntimeError):
    pass


def save_private(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".migration-")
    try:
        with os.fdopen(fd, "w") as handle:
            json.dump(data, handle, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_archive(path: Path) -> dict[str, Any]:
    with zipfile.ZipFile(path) as archive:
        data = json.loads(archive.read("data.json"))
    if "book" not in data:
        raise MigrationError("This tool requires a whole-book portable ZIP.")
    return data


def pages(book: dict[str, Any]) -> list[dict[str, Any]]:
    return book.get("pages", []) + [
        page for chapter in book.get("chapters", []) for page in chapter["pages"]
    ]


def inventory(book: dict[str, Any]) -> dict[str, Any]:
    content = pages(book)
    return {
        "book": book["name"],
        "chapters": len(book.get("chapters", [])),
        "pages": len(content),
        "tables": sum(len(re.findall(r"<table\b", p.get("html", ""))) for p in content),
        "images": sum(len(p.get("images", [])) for p in content),
        "attachments": sum(len(p.get("attachments", [])) for p in content),
    }


class Api:
    def __init__(self, config: Path):
        data = json.loads(config.read_text())
        self.url = data["url"].rstrip("/")
        if urllib.parse.urlsplit(self.url).scheme != "https":
            raise MigrationError("The target must use HTTPS.")
        if urllib.parse.urlsplit(self.url).hostname == "wiki.sandiahomeowners.org":
            raise MigrationError("Refusing to write to the DigitalOcean source.")
        self.authorization = f"Token {data['token_id']}:{data['token_secret']}"

    def request(self, endpoint: str, method: str = "GET", body: bytes | None = None,
                content_type: str | None = None) -> bytes:
        headers = {"Authorization": self.authorization, "Accept": "application/json"}
        if content_type:
            headers["Content-Type"] = content_type
        request = urllib.request.Request(
            f"{self.url}/api/{endpoint}", data=body, headers=headers, method=method
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            # Never print API response bodies, private content or credentials.
            raise MigrationError(f"API {method} {endpoint}: HTTP {error.code}") from None
        except (TimeoutError, urllib.error.URLError):
            raise MigrationError(
                f"API {method} {endpoint}: response unavailable; reconcile before retrying writes."
            ) from None

    def json(self, endpoint: str, method: str = "GET", body: bytes | None = None,
             content_type: str | None = None) -> dict[str, Any]:
        return json.loads(self.request(endpoint, method, body, content_type))

    def listing(self, endpoint: str) -> list[dict[str, Any]]:
        found: list[dict[str, Any]] = []
        while True:
            separator = "&" if "?" in endpoint else "?"
            result = self.json(f"{endpoint}{separator}count=100&offset={len(found)}")
            batch = result["data"]
            found.extend(batch)
            if len(found) >= result["total"]:
                return found
            if not batch:
                raise MigrationError("API pagination ended before the reported total.")


def import_book(api: Api, archive: Path, report_path: Path) -> dict[str, Any]:
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if report_path.exists():
        report = json.loads(report_path.read_text())
        if report.get("source_sha256") != digest or report.get("target") != api.url:
            raise MigrationError("Existing report belongs to another source or target.")
        if report.get("book_id"):
            return report
        raise MigrationError("A prior import needs reconciliation; it will not be retried blindly.")
    if api.listing("books") or api.listing("chapters") or api.listing("pages"):
        raise MigrationError("Initial content import requires an empty target.")
    source = read_archive(archive)
    report = {
        "started_at": datetime.now(timezone.utc).isoformat(),
        "target": api.url,
        "source_sha256": digest,
        "source_exported_at": source["exported_at"],
        "source_inventory": inventory(source["book"]),
        "state": "uploading",
    }
    save_private(report_path, report)
    boundary = "BookStackMigration" + secrets.token_hex(16)
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; '
        'filename="bookstack-live-export.zip"\r\nContent-Type: application/zip\r\n\r\n'
    ).encode() + archive.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    uploaded = api.json("imports", "POST", body, f"multipart/form-data; boundary={boundary}")
    report.update(import_id=uploaded["id"], state="uploaded")
    save_private(report_path, report)
    details = api.json(f"imports/{uploaded['id']}")
    if details["type"] != "book":
        raise MigrationError("Uploaded import is not a book.")
    report["state"] = "running"
    save_private(report_path, report)
    imported = api.json(f"imports/{uploaded['id']}", "POST", b"{}", "application/json")
    report.update(book_id=imported["id"], state="imported")
    save_private(report_path, report)
    return report


class ContentParser(HTMLParser):
    def __init__(self, markup: str):
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.ids: set[str] = set()
        self.table_count = 0
        self.feed(markup)

    def handle_starttag(self, tag: str, attributes: list[tuple[str, str | None]]) -> None:
        attributes_dict = dict(attributes)
        if tag == "a" and attributes_dict.get("href"):
            self.links.append(str(attributes_dict["href"]))
        if attributes_dict.get("id"):
            self.ids.add(str(attributes_dict["id"]))
        self.table_count += tag == "table"


def unique_named(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result = {item["name"]: item for item in items}
    if len(result) != len(items):
        raise MigrationError("Duplicate names require an explicit mapping.")
    return result


def ordered_names(items: list[dict[str, Any]]) -> list[str]:
    return [item["name"] for item in sorted(items, key=lambda item: item["priority"])]


def tags(items: list[dict[str, Any]]) -> list[tuple[str, str]]:
    return [(item["name"], item.get("value", "")) for item in items]


def verify(api: Api, source: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    source_book = source["book"]
    target = api.json(f"books/{report['book_id']}")
    if target["name"] != source_book["name"]:
        raise MigrationError("Imported book name differs.")
    target_chapters = unique_named([x for x in target["contents"] if x["type"] == "chapter"])
    source_chapters = unique_named(source_book.get("chapters", []))
    if target_chapters.keys() != source_chapters.keys():
        raise MigrationError("Chapter inventory differs.")
    # Native imports renumber priorities. Compare displayed sibling order.
    source_children = source_book.get("chapters", []) + source_book.get("pages", [])
    if ordered_names(source_children) != ordered_names(target["contents"]):
        raise MigrationError("Book contents order differs.")
    reference_urls = {("book", source_book["id"]): f"{api.url}/books/{target['slug']}"}
    mapping: dict[str, dict[str, Any]] = {"books": {}, "chapters": {}, "pages": {}}
    mapping["books"][str(source_book["id"])] = target["id"]
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for name, original in source_chapters.items():
        chapter = target_chapters[name]
        mapping["chapters"][str(original["id"])] = chapter["id"]
        reference_urls[("chapter", original["id"])] = (
            f"{api.url}/books/{target['slug']}/chapter/{chapter['slug']}"
        )
        originals = unique_named(original["pages"])
        targets = unique_named(chapter["pages"])
        if originals.keys() != targets.keys():
            raise MigrationError("Chapter page inventory differs.")
        if ordered_names(original["pages"]) != ordered_names(chapter["pages"]):
            raise MigrationError("Chapter page order differs.")
        pairs.extend((page, targets[name]) for name, page in originals.items())
    unchaptered = unique_named([x for x in target["contents"] if x["type"] == "page"])
    originals = unique_named(source_book.get("pages", []))
    if originals.keys() != unchaptered.keys():
        raise MigrationError("Unchaptered page inventory differs.")
    pairs.extend((page, unchaptered[name]) for name, page in originals.items())
    for original, imported in pairs:
        mapping["pages"][str(original["id"])] = imported["id"]
        reference_urls[("page", original["id"])] = (
            f"{api.url}/books/{target['slug']}/page/{imported['slug']}"
        )
    def substitute(match: re.Match[str]) -> str:
        key = (match[1], int(match[2]))
        if key not in reference_urls:
            raise MigrationError("Export references an entity outside the imported book.")
        return reference_urls[key]

    def resolve(markup: str) -> str:
        return re.sub(r"\[\[bsexport:([a-z]+):(\d+)]]", substitute, markup)

    descriptors = [(source_book, target)]
    descriptors.extend(
        (original, api.json(f"chapters/{target_chapters[name]['id']}"))
        for name, original in source_chapters.items()
    )
    for original, imported in descriptors:
        if resolve(original.get("description_html", "")).strip() != imported.get("description_html", "").strip():
            raise MigrationError("Book or chapter description differs.")
        if tags(original.get("tags", [])) != tags(imported.get("tags", [])):
            raise MigrationError("Book or chapter tags differ.")
    mismatches: list[str] = []
    entity_normalizations: list[str] = []
    external_links = 0
    tables = 0
    actual_pages: dict[str, ContentParser] = {}
    for original, imported in pairs:
        detail = api.json(f"pages/{imported['id']}")
        raw = detail.get("raw_html", detail.get("html", ""))
        expected = resolve(original.get("html", ""))
        if raw.strip() != expected.strip():
            if raw.strip().replace("\u00a0", "&nbsp;") == expected.strip().replace("\u00a0", "&nbsp;"):
                entity_normalizations.append(original["name"])
            else:
                mismatches.append(original["name"])
        if tags(original.get("tags", [])) != tags(detail.get("tags", [])):
            raise MigrationError("Page tags differ.")
        before, after = ContentParser(expected), ContentParser(raw)
        if Counter(before.links) != Counter(after.links):
            raise MigrationError("Page link destinations differ.")
        if before.table_count != after.table_count:
            raise MigrationError("Page table count differs.")
        actual_pages[reference_urls[("page", original["id"])]] = after
        external_links += sum(not link.startswith(api.url) for link in after.links)
        tables += after.table_count
    if mismatches:
        raise MigrationError("Page HTML differs: " + ", ".join(mismatches))
    broken_anchors = 0
    for parsed in actual_pages.values():
        for link in parsed.links:
            destination, _, fragment = link.partition("#")
            if fragment and destination in actual_pages:
                broken_anchors += urllib.parse.unquote(fragment) not in actual_pages[destination].ids
    report.update(
        state="verified", verified_at=datetime.now(timezone.utc).isoformat(),
        mapping=mapping, book_url=f"{api.url}/books/{target['slug']}",
        verification={"pages": len(pairs), "chapters": len(source_chapters),
                      "tables": tables, "external_link_occurrences_preserved": external_links,
                      "html_exact_after_reference_mapping": not entity_normalizations,
                      "html_equivalent_after_reference_mapping": True,
                      "html_entity_normalization_pages": len(entity_normalizations),
                      "broken_cross_page_anchors": broken_anchors},
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["inspect", "import", "verify"])
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--config", type=Path,
                        default=Path.home() / ".config/shha-wiki/target-api.json")
    parser.add_argument("--report", type=Path,
                        default=Path.home() / ".config/shha-wiki/migration/import-report.json")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        source = read_archive(args.archive)
        if args.action == "inspect":
            print(json.dumps(inventory(source["book"])))
            return
        api = Api(args.config)
        if args.action == "import":
            if not args.apply:
                raise MigrationError("Import requires --apply.")
            report = import_book(api, args.archive, args.report)
        else:
            report = json.loads(args.report.read_text())
            if report["target"] != api.url:
                raise MigrationError("Verification target does not match the import report.")
        report = verify(api, source, report)
        save_private(args.report, report)
        print(json.dumps({"book_url": report["book_url"], **report["verification"]}))
    except MigrationError as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
