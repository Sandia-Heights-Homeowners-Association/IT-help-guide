#!/usr/bin/env python3
"""Mirror one BookStack book using anonymous, GET-only native exports.

No API token or login cookie is accepted. Restricted content and unpublished
drafts are therefore outside this public mirror. Standard library only.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from datetime import datetime, timezone
import hashlib
from html import escape
from html.parser import HTMLParser
import http.client
import io
import json
import mimetypes
import os
from pathlib import Path
import re
import shutil
import socket
import ssl
import tempfile
import time
import urllib.parse
import zipfile

BASE_URL = "https://wiki.sandiahomeowners.org"
BOOK_PATH = "/books/shha-it-help-guide"
MAX_BYTES = 50 * 1024 * 1024


class SyncError(RuntimeError):
    pass


class RoutedHTTPSConnection(http.client.HTTPSConnection):
    """Optional Azure routing override, retaining canonical TLS SNI/Host."""

    def __init__(self, host: str, connect_host: str | None):
        super().__init__(host, timeout=45, context=ssl.create_default_context())
        self.connect_host = connect_host

    def connect(self):
        raw = socket.create_connection((self.connect_host or self.host, 443), self.timeout)
        try:
            self.sock = self._context.wrap_socket(raw, server_hostname=self.host)
        except Exception:
            raw.close()
            raise


class PublicClient:
    def __init__(self, base_url: str, connect_host: str | None = None):
        parsed = urllib.parse.urlsplit(base_url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.port not in (None, 443) or parsed.username or parsed.password or parsed.path not in ("", "/") or parsed.query or parsed.fragment:
            raise SyncError("The public origin must be a plain HTTPS hostname")
        self.base_url = base_url.rstrip("/")
        self.host = parsed.hostname
        self.netloc = parsed.netloc
        if connect_host and not re.fullmatch(r"[A-Za-z0-9.-]+\.azurewebsites\.net", connect_host):
            raise SyncError("Routing override must be an Azure App Service hostname")
        self.connect_host = connect_host

    def get(self, path: str) -> tuple[str, bytes]:
        current = self.base_url + path
        for _ in range(6):
            parsed = urllib.parse.urlsplit(current)
            if parsed.scheme != "https" or parsed.netloc != self.netloc or parsed.username or parsed.password:
                raise SyncError("Refusing a redirect outside the public origin")
            route = parsed.path + ("?" + parsed.query if parsed.query else "")
            for attempt in range(3):
                connection = RoutedHTTPSConnection(self.host, self.connect_host)
                try:
                    connection.request("GET", route, headers={"Accept": "*/*", "User-Agent": "SHHA-public-wiki-mirror/1.0"})
                    response = connection.getresponse()
                    status = response.status
                    location = response.getheader("Location")
                    if status in (429, 502, 503, 504) and attempt < 2:
                        retry_after = response.getheader("Retry-After", "")
                        delay = min(60, int(retry_after)) if retry_after.isdigit() else 10 * (attempt + 1)
                        connection.close()
                        time.sleep(max(1, delay))
                        continue
                    if status in (301, 302, 303, 307, 308) and location:
                        current = urllib.parse.urljoin(current, location)
                        if urllib.parse.urlsplit(current).path.startswith(("/login", "/oidc")):
                            raise SyncError("Public reading/export is unavailable; sign-in is never attempted")
                        break
                    if status != 200:
                        raise SyncError(f"Anonymous export returned HTTP {status}")
                    body = response.read(MAX_BYTES + 1)
                    if len(body) > MAX_BYTES:
                        raise SyncError("Export exceeds the download size limit")
                    return current, body
                except (OSError, http.client.HTTPException):
                    # No response bodies, page content, or credential values in logs.
                    raise SyncError("Public export network/TLS request failed") from None
                finally:
                    connection.close()
        raise SyncError("Too many public redirects")


def read_book_archive(body: bytes) -> tuple[dict, dict[int, str]]:
    try:
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            if sum(info.file_size for info in archive.infolist()) > MAX_BYTES:
                raise SyncError("Uncompressed portable export exceeds the size limit")
            entry = archive.getinfo("data.json")
            if entry.file_size > MAX_BYTES:
                raise SyncError("Export JSON exceeds the size limit")
            book = json.loads(archive.read(entry))["book"]
            if not isinstance(book, dict) or not isinstance(book.get("name"), str):
                raise ValueError()
            if book.get("cover"):
                name = book["cover"]
                asset = archive.read("files/" + name)
                book["cover"] = hashlib.sha256(asset).hexdigest() + Path(name).suffix.lower()
            images = {}

            def normalize_assets(value, relation=None):
                if isinstance(value, list):
                    for child in value:
                        normalize_assets(child, relation)
                elif isinstance(value, dict):
                    if value.get("file"):
                        name = value["file"]
                        info = archive.getinfo("files/" + name)
                        if info.file_size > MAX_BYTES:
                            raise SyncError("Public attachment exceeds the size limit")
                        asset = archive.read(info)
                        # BookStack randomizes portable asset filenames each export.
                        value["file"] = hashlib.sha256(asset).hexdigest() + Path(name).suffix.lower()
                        if relation == "images":
                            if len(asset) > 2 * 1024 * 1024:
                                raise SyncError("Image exceeds the 2 MiB public mirror limit")
                            mime = mimetypes.guess_type(name)[0]
                            if not mime or not mime.startswith("image/"):
                                raise SyncError("Expected a portable image asset")
                            images[int(value["id"])] = "data:" + mime + ";base64," + base64.b64encode(asset).decode()
                    for key, child in value.items():
                        normalize_assets(child, key)

            normalize_assets(book)
        return book, images
    except (ValueError, KeyError, zipfile.BadZipFile):
        raise SyncError("Expected a public whole-book portable ZIP") from None


def ordered_pages(book: dict) -> list[tuple[dict, dict | None]]:
    children = [(p, None) for p in book.get("pages", [])]
    children += [(c, c) for c in book.get("chapters", [])]
    result = []
    for child, chapter in sorted(children, key=lambda item: item[0].get("priority", 0)):
        if chapter is None:
            result.append((child, None))
        else:
            result += [(p, chapter) for p in sorted(chapter.get("pages", []), key=lambda p: p.get("priority", 0))]
    ids = [p["id"] for p, _ in result]
    if not ids or len(set(ids)) != len(ids):
        raise SyncError("Empty book or duplicate page IDs; keeping the existing mirror")
    return result


def normalized_html(body: bytes) -> bytes:
    text = body.decode("utf-8")
    if "<html" not in text.lower():
        raise SyncError("Expected a standalone HTML page export")
    # Contained HTML has a fresh CSP nonce on each request. Normalize only the
    # generated CSP metadata, never the page body, to avoid meaningless commits.
    text = re.sub(r'<meta\b[^>]*http-equiv="Content-Security-Policy"[^>]*>',
                  lambda m: re.sub(r"nonce-[A-Za-z0-9+/=_-]+", "nonce-bookstack-export", m[0]), text, flags=re.I)
    return (text.rstrip() + "\n").encode()


class PublicEntityLinks(HTMLParser):
    def __init__(self, body: bytes, client: PublicClient, book_path: str):
        super().__init__()
        self.links = {}
        self.client = client
        self.book_path = book_path
        self.feed(body.decode("utf-8"))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        kind = attrs.get("data-entity-type")
        entity_id = attrs.get("data-entity-id", "")
        if tag == "a" and kind in ("page", "chapter") and entity_id.isdigit():
            url = urllib.parse.urljoin(self.client.base_url, attrs.get("href", ""))
            parsed = urllib.parse.urlsplit(url)
            if parsed.netloc != urllib.parse.urlsplit(self.client.base_url).netloc or not re.fullmatch(re.escape(self.book_path) + "/" + kind + r"/[a-z0-9-]+", parsed.path):
                raise SyncError("Public contents link points outside the configured book")
            self.links[(kind, int(entity_id))] = url


def markdown_sections(book: dict, markdown: str) -> dict[int, str] | None:
    # Native book Markdown concatenates book/chapter/page sections, each with
    # '# Name'. Only split when every expected boundary is unambiguous. If a
    # body repeats one of those headings, use native individual page exports.
    boundaries = [("book", book)]
    children = [(p, None) for p in book.get("pages", [])] + [(c, c) for c in book.get("chapters", [])]
    for child, chapter in sorted(children, key=lambda item: item[0].get("priority", 0)):
        if chapter:
            boundaries.append(("chapter", chapter))
            boundaries += [("page", p) for p in sorted(chapter.get("pages", []), key=lambda p: p.get("priority", 0))]
        else:
            boundaries.append(("page", child))
    expected = [entity["name"] for _, entity in boundaries]
    pattern = r"^# (" + "|".join(re.escape(name) for name in set(expected)) + r")\n(?=\n)"
    matches = list(re.finditer(pattern, markdown + "\n\n", flags=re.M))
    actual = [m[1] for m in matches]
    if Counter(actual) != Counter(expected) or actual != expected:
        return None
    return {entity["id"]: markdown[matches[i].start():matches[i + 1].start() if i + 1 < len(matches) else len(markdown)].rstrip() + "\n"
            for i, (kind, entity) in enumerate(boundaries) if kind == "page"}


def snapshot_digest(files: dict[str, bytes]) -> str:
    digest = hashlib.sha256()
    for path, body in sorted(files.items()):
        digest.update(path.encode() + b"\0" + body + b"\0")
    return digest.hexdigest()


def sync(client: PublicClient, output: Path, book_path: str = BOOK_PATH) -> dict:
    if not re.fullmatch(r"/books/[a-z0-9-]+", book_path):
        raise SyncError("Expected a single BookStack book path")
    if output.is_symlink():
        raise SyncError("Mirror directory must not be a symlink")
    if output.name != "bookstack-current" or (output / ".git").exists():
        raise SyncError("Only a bookstack-current content directory may be replaced")
    book, images = read_book_archive(client.get(book_path + "/export/zip")[1])
    content = ordered_pages(book)
    links = PublicEntityLinks(client.get(book_path)[1], client, book_path).links
    links[("book", int(book["id"]))] = client.base_url + book_path
    _, combined_body = client.get(book_path + "/export/markdown")
    combined = combined_body.decode("utf-8").replace("\r\n", "\n")
    sections = markdown_sections(book, combined)
    files = {"book.json": (json.dumps(book, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode()}
    manifest_pages = []

    def replace_reference(match):
        kind, entity_id = match[1], int(match[2])
        if kind == "image" and entity_id in images:
            return images[entity_id]
        if kind == "attachment":
            return client.base_url + "/attachments/" + str(entity_id)
        if (kind, entity_id) in links:
            return links[(kind, entity_id)]
        raise SyncError("Portable content reference could not be resolved")

    for index, (page, chapter) in enumerate(content, start=1):
        url = links.get(("page", int(page["id"])))
        if not url:
            raise SyncError("Exported page is absent from the anonymous book contents")
        path = urllib.parse.urlsplit(url).path
        if not re.fullmatch(re.escape(book_path) + r"/page/[a-z0-9-]+", path):
            raise SyncError("Page permalink did not resolve to this public book")
        if sections is None:
            markdown = client.get(path + "/export/markdown")[1].decode("utf-8")
        else:
            markdown = sections[page["id"]]
        body = re.sub(r"\[\[bsexport:(page|chapter|book|image|attachment):(\d+)\]\]", replace_reference, page.get("html", ""))
        html = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                '<title>' + escape(page["name"]) + '</title>'
                '<style>body{max-width:60rem;margin:2rem auto;padding:0 1rem;font-family:system-ui,sans-serif;line-height:1.5}'
                'table{border-collapse:collapse}td,th{border:1px solid #aaa;padding:.4rem}img{max-width:100%}</style>'
                '</head><body><h1>' + escape(page["name"]) + '</h1>\n' + body + '\n</body></html>\n').encode()
        slug = path.rsplit("/", 1)[-1]
        filename = f"{index:02d}-{slug}"
        md_path = f"pages-md/{filename}.md"
        html_path = f"pages-html/{filename}.html"
        files[md_path] = (markdown.rstrip() + "\n").encode()
        files[html_path] = normalized_html(html)
        manifest_pages.append({"id": page["id"], "name": page["name"], "slug": slug,
                               "chapter": chapter["name"] if chapter else "Unchaptered",
                               "priority": page.get("priority", 0), "url": url,
                               "markdown": "bookstack-current/" + md_path,
                               "html": "bookstack-current/" + html_path})
    files["book.md"] = (combined.rstrip() + "\n").encode()
    closing, _ = read_book_archive(client.get(book_path + "/export/zip")[1])
    if closing != book:
        raise SyncError("Content/visibility changed during export; keeping the previous mirror")
    digest = snapshot_digest(files)
    metadata = {"source": client.base_url, "book_id": book.get("id"), "book_name": book["name"],
                "book_path": book_path, "visibility": "anonymous-public", "content_sha256": digest,
                "chapters": len(book.get("chapters", [])), "pages": manifest_pages}
    if output.exists():
        actual = {str(p.relative_to(output)): p.read_bytes() for p in output.rglob("*") if p.is_file() and p.name != "manifest.json"}
        previous_manifest = json.loads((output / "manifest.json").read_text()) if (output / "manifest.json").exists() else {}
        previous_manifest.pop("exported_at", None)
        if actual == files and previous_manifest == metadata:
            return {"changed": False, "pages": len(content), "chapters": metadata["chapters"], "content_sha256": digest}
    metadata["exported_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    files["manifest.json"] = (json.dumps(metadata, indent=2, ensure_ascii=False) + "\n").encode()
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".sync-staging-", dir=output.parent))
    previous = None
    try:
        for name, body in files.items():
            path = staging / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        if output.exists():
            previous = Path(tempfile.mkdtemp(prefix=".sync-previous-", dir=output.parent))
            previous.rmdir()
            os.rename(output, previous)
        try:
            os.rename(staging, output)
        except OSError:
            if previous:
                os.rename(previous, output)
            raise
        if previous:
            shutil.rmtree(previous)
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    return {"changed": True, "pages": len(content), "chapters": metadata["chapters"], "content_sha256": digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=os.environ.get("BOOKSTACK_URL", BASE_URL))
    parser.add_argument("--connect-host", default=os.environ.get("BOOKSTACK_CONNECT_HOST"))
    parser.add_argument("--book-path", default=os.environ.get("BOOKSTACK_BOOK_PATH", BOOK_PATH))
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "bookstack-current")
    args = parser.parse_args()
    try:
        print(json.dumps(sync(PublicClient(args.url, args.connect_host), args.output, args.book_path)))
    except (SyncError, OSError, ValueError, KeyError) as error:
        print("Public BookStack sync failed: " + (str(error) if isinstance(error, SyncError) else type(error).__name__))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
