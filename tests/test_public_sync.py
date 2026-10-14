import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sync_public_bookstack import PublicClient, SyncError, markdown_sections, normalized_html, read_book_archive, sync


def archive(book):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as output:
        output.writestr("data.json", json.dumps({"book": book, "exported_at": "variable"}))
    return stream.getvalue()


def page(page_id):
    return {"id": page_id, "name": f"Public page {page_id}", "priority": page_id,
            "html": "<p>Current rich content</p>", "tags": []}


class FakePublicClient:
    base_url = "https://wiki.example.org"

    def __init__(self, ids=(3, 4), fail=None, changing=False, nonce="one"):
        self.book = {"id": 1, "name": "Example book", "pages": [page(i) for i in ids], "chapters": []}
        self.fail = fail
        self.changing = changing
        self.nonce = nonce
        self.exports = 0

    def get(self, path):
        if self.fail and self.fail in path:
            raise SyncError("Simulated unavailable export")
        if path.endswith("/export/zip"):
            self.exports += 1
            current = copy.deepcopy(self.book)
            if self.changing and self.exports > 1:
                current["pages"][0]["html"] = "<p>Concurrent edit</p>"
            return self.base_url + path, archive(current)
        if path == "/books/example":
            body = ''.join(f'<a data-entity-type="page" data-entity-id="{p["id"]}" href="{self.base_url}/books/example/page/page-{p["id"]}">Page</a>' for p in self.book['pages'])
            return self.base_url + path, body.encode()
        if path == "/books/example/export/markdown":
            body = '# Example book\n\n' + '\n\n'.join(f'# {p["name"]}\n\nReadable text.' for p in self.book['pages'])
            if self.fail:
                body += '\n\n# Public page 3\n\nAmbiguous heading in a body.'
            return self.base_url + path, body.encode()
        if path.startswith("/link/"):
            path = "/books/example/page/page-" + path.rsplit("/", 1)[-1]
        body = b"public page"
        if path.endswith("/export/html"):
            body = ('<html><meta http-equiv="Content-Security-Policy" content="script-src &#039;nonce-'
                    + self.nonce + '&#039;"><body><table><tr><td>Rich text</td></tr></table></body></html>').encode()
        elif path.endswith("/export/markdown"):
            body = b"# Exported title\n\nReadable text.\n"
        return self.base_url + path, body


class PublicSyncTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.output = self.root / "bookstack-current"
        self.drafts = self.root / "pending-bookstack-updates"
        self.drafts.mkdir()
        (self.drafts / "unfinished.md").write_text("Do not publish this draft")

    def tearDown(self):
        self.temporary.cleanup()

    def files(self):
        return {str(p.relative_to(self.output)): p.read_bytes() for p in self.output.rglob("*") if p.is_file()}

    def test_new_and_removed_public_pages_preserve_drafts(self):
        sync(FakePublicClient(), self.output, "/books/example")
        sync(FakePublicClient(ids=(4, 5)), self.output, "/books/example")
        manifest = json.loads((self.output / "manifest.json").read_text())
        self.assertEqual([p["id"] for p in manifest["pages"]], [4, 5])
        self.assertFalse((self.output / "pages-md/01-page-3.md").exists())
        self.assertEqual((self.drafts / "unfinished.md").read_text(), "Do not publish this draft")
        self.assertFalse(any("unfinished" in path for path in self.files()))

    def test_repeated_content_and_nonce_do_not_create_changes(self):
        self.assertTrue(sync(FakePublicClient(), self.output, "/books/example")["changed"])
        before = self.files()
        self.assertFalse(sync(FakePublicClient(nonce="two"), self.output, "/books/example")["changed"])
        self.assertEqual(before, self.files())

    def test_failed_page_export_preserves_previous_mirror(self):
        sync(FakePublicClient(), self.output, "/books/example")
        before = self.files()
        with self.assertRaises(SyncError):
            sync(FakePublicClient(ids=(3, 4, 5), fail="page-5/export/markdown"), self.output, "/books/example")
        self.assertEqual(before, self.files())

    def test_concurrent_change_preserves_previous_mirror(self):
        sync(FakePublicClient(), self.output, "/books/example")
        before = self.files()
        with self.assertRaises(SyncError):
            sync(FakePublicClient(changing=True), self.output, "/books/example")
        self.assertEqual(before, self.files())

    def test_nonce_normalization_does_not_change_content(self):
        html = b'<html><meta http-equiv="Content-Security-Policy" content="nonce-abc"><p>nonce-abc</p></html>'
        result = normalized_html(html)
        self.assertIn(b'content="nonce-bookstack-export"', result)
        self.assertIn(b"<p>nonce-abc</p>", result)

    def test_ambiguous_markdown_heading_requires_native_fallback(self):
        book = FakePublicClient().book
        self.assertIsNone(markdown_sections(book, '# Example book\n\n# Public page 3\n\n# Public page 3\n\n# Public page 4\n\n'))

    def test_portable_asset_random_names_use_content_hashes(self):
        def export(filename):
            book = FakePublicClient(ids=(3,)).book
            book['pages'][0]['images'] = [{'id': 9, 'name': 'Example', 'file': filename}]
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, 'w') as output:
                output.writestr('data.json', json.dumps({'book': book}))
                output.writestr('files/' + filename, b'example public image bytes')
            return read_book_archive(stream.getvalue())
        self.assertEqual(export('random-first.png'), export('random-second.png'))

    def test_login_and_external_redirects_are_blocked_without_credentials(self):
        class Response:
            status = 302
            location = "/login"

            def getheader(self, key, default=None):
                return self.location if key == "Location" else default

        class Connection:
            headers = None
            method = None

            def __init__(self, *args):
                pass

            def request(self, method, path, headers):
                Connection.headers = headers
                Connection.method = method

            def getresponse(self):
                return Response()

            def close(self):
                pass

        with patch("sync_public_bookstack.RoutedHTTPSConnection", Connection), patch.dict("os.environ", {"BOOKSTACK_TOKEN_SECRET": "must-not-be-used"}):
            with self.assertRaises(SyncError):
                PublicClient("https://wiki.example.org").get("/books/example/export/zip")
            self.assertEqual(Connection.method, "GET")
            self.assertNotIn("Authorization", Connection.headers)
            self.assertNotIn("Cookie", Connection.headers)
            Response.location = "https://other.example.org/secret"
            with self.assertRaises(SyncError):
                PublicClient("https://wiki.example.org").get("/books/example/export/zip")

    def test_invalid_or_empty_archive_preserves_previous_mirror(self):
        sync(FakePublicClient(), self.output, "/books/example")
        before = self.files()
        with self.assertRaises(SyncError):
            sync(FakePublicClient(ids=()), self.output, "/books/example")
        self.assertEqual(before, self.files())

    def test_output_guard_prevents_overwriting_draft_directories(self):
        with self.assertRaises(SyncError):
            sync(FakePublicClient(), self.drafts, "/books/example")
        self.assertEqual((self.drafts / "unfinished.md").read_text(), "Do not publish this draft")


if __name__ == "__main__":
    unittest.main()
