import tempfile
import unittest
from pathlib import Path

from core import DocumentStore, EditorError, render_markdown


class DocumentStoreTests(unittest.TestCase):
    def test_utf8_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "demo.md"
            path.write_bytes("# 标题\n\nhello".encode("utf-8"))
            store = DocumentStore()
            state = store.load(path)
            self.assertEqual(state["content"], "# 标题\n\nhello")
            store.save("# 修改")
            self.assertEqual(path.read_text(encoding="utf-8"), "# 修改")

    def test_utf8_bom_is_preserved_on_normal_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bom.md"
            path.write_bytes(b"\xef\xbb\xbf" + "# 标题".encode("utf-8"))
            store = DocumentStore()
            store.load(path)
            store.save("# 修改")
            self.assertTrue(path.read_bytes().startswith(b"\xef\xbb\xbf"))

    def test_crlf_is_preserved_on_normal_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "crlf.md"
            path.write_bytes(b"# Title\r\n\r\nline\r\n")
            store = DocumentStore()
            store.load(path)
            store.save("# Changed\n\nline\n")
            self.assertEqual(path.read_bytes(), b"# Changed\r\n\r\nline\r\n")

    def test_non_utf8_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "gbk.md"
            path.write_bytes("中文".encode("gbk"))
            with self.assertRaises(EditorError):
                DocumentStore().load(path)

    def test_save_as_adds_md_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = DocumentStore()
            state = store.save_as(Path(tmp) / "note", "hello")
            self.assertTrue(state["path"].endswith("note.md"))
            self.assertEqual((Path(tmp) / "note.md").read_text(encoding="utf-8"), "hello")


class RenderingTests(unittest.TestCase):
    def test_raw_html_is_escaped(self):
        html = render_markdown('<img src=x onerror="alert(1)">', None)
        self.assertIn("&lt;img", html)
        self.assertNotIn("onerror=", html.replace("&lt;img src=x onerror=", ""))

    def test_harmful_link_is_neutralized(self):
        html = render_markdown("[x](javascript:alert(1))", None)
        self.assertIn('href="#harmful-link"', html)

    def test_relative_image_is_inlined(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            image = base / "pixel.png"
            image.write_bytes(b"\x89PNG\r\n\x1a\n" + b"x" * 16)
            html = render_markdown("![x](pixel.png)", base)
            self.assertIn("data:image/png;base64,", html)


if __name__ == "__main__":
    unittest.main()
