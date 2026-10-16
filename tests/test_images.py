import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote

from core import import_image, EditorError


class ImageImportTests(unittest.TestCase):
    def test_copy_relative_reference_and_collision(self):
        with tempfile.TemporaryDirectory() as folder:
            document = Path(folder) / '中文 文档.md'
            references = [import_image(document, b'image bytes', '.PNG') for _ in range(2)]
            self.assertNotEqual(*references)
            for reference in references:
                relative = unquote(reference[len('![图片]('):-1])
                self.assertEqual((document.parent / relative).read_bytes(), b'image bytes')
                self.assertTrue(relative.startswith('中文 文档.assets/'))
            self.assertFalse(document.exists())

    def test_reject_unsaved_unsupported_and_oversize(self):
        with self.assertRaises(EditorError):
            import_image(None, b'', '.png')
        with tempfile.TemporaryDirectory() as folder:
            for suffix, data in [('.heic', b''), ('.png', b'x' * (12 * 1024 * 1024 + 1))]:
                with self.assertRaises(EditorError):
                    import_image(Path(folder) / 'test.md', data, suffix)
            self.assertEqual(list(Path(folder).iterdir()), [])
