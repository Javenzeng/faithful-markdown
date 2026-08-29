import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from core import DocumentStore, EditorError


FIXTURES = Path(__file__).parent / "fixtures" / "fidelity"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture_bytes(name: str) -> bytes:
    return (FIXTURES / name).read_bytes()


class FidelityTests(unittest.TestCase):
    def copy_fixture(self, tmp: str, fixture: str, name: str = "doc.md") -> Path:
        path = Path(tmp) / name
        path.write_bytes(fixture_bytes(fixture))
        return path

    def temp_residue(self, path: Path) -> list[Path]:
        return list(path.parent.glob(f".{path.name}.*.tmp"))

    def test_noop_save_is_byte_identical_and_skips_safe_write(self):
        for fixture in (
            "utf8_lf.md.bin",
            "utf8_no_final_newline.md.bin",
            "utf8_bom_crlf.md.bin",
            "unicode_emoji.md.bin",
            "mixed_eol.md.bin",
        ):
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as tmp:
                path = self.copy_fixture(tmp, fixture)
                store = DocumentStore()
                state = store.load(path)
                before = sha256(path)
                with patch.object(store, "_safe_write", wraps=store._safe_write) as safe_write:
                    saved = store.save(state["content"])
                self.assertEqual(sha256(path), before)
                self.assertEqual(path.read_bytes(), fixture_bytes(fixture))
                self.assertEqual(safe_write.call_count, 0)
                self.assertEqual(saved["path"], str(path.resolve()))

    def test_mixed_eol_noop_is_byte_identical(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.copy_fixture(tmp, "mixed_eol.md.bin")
            store = DocumentStore()
            content = store.load(path)["content"]
            before = path.read_bytes()
            store.save(content)
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(store.eol_kind, "MIXED")

    def test_external_modification_is_blocked_even_for_clean_editor(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.copy_fixture(tmp, "utf8_lf.md.bin")
            store = DocumentStore()
            content = store.load(path)["content"]
            external = b"external\n"
            path.write_bytes(external)
            with self.assertRaises(EditorError):
                store.save(content)
            self.assertEqual(path.read_bytes(), external)

    def test_second_fingerprint_conflict_preserves_target_and_cleans_temp(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.copy_fixture(tmp, "utf8_lf.md.bin")
            store = DocumentStore()
            store.load(path)
            original_snapshot = store._snapshot_target
            external = b"changed after temp\n"

            def conflict_snapshot(target: Path):
                target.write_bytes(external)
                return original_snapshot(target)

            with patch.object(store, "_snapshot_target", side_effect=conflict_snapshot):
                with self.assertRaises(EditorError):
                    store.save("# Edited\n")

            self.assertEqual(path.read_bytes(), external)
            self.assertEqual(self.temp_residue(path), [])

    def test_os_replace_failure_preserves_target_and_cleans_temp(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.copy_fixture(tmp, "utf8_lf.md.bin")
            before = path.read_bytes()
            store = DocumentStore()
            store.load(path)
            with patch("core.os.replace", side_effect=OSError("replace failed")):
                with self.assertRaises(EditorError):
                    store.save("# Edited\n")
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(self.temp_residue(path), [])

    def test_save_as_same_path_delegates_to_normal_guard(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.copy_fixture(tmp, "utf8_bom_crlf.md.bin")
            store = DocumentStore()
            store.load(path)
            external = b"external replacement\n"
            path.write_bytes(external)
            with patch.object(store, "save", wraps=store.save) as normal_save:
                with self.assertRaises(EditorError):
                    store.save_as(path, "edited\n")
            self.assertEqual(normal_save.call_count, 1)
            self.assertEqual(path.read_bytes(), external)

    def test_save_as_target_races_are_blocked_and_temp_cleaned(self):
        cases = ("created", "deleted", "modified")
        for case in cases:
            with self.subTest(case=case), tempfile.TemporaryDirectory() as tmp:
                source = self.copy_fixture(tmp, "utf8_lf.md.bin", "source.md")
                target = Path(tmp) / "target.md"
                if case in {"deleted", "modified"}:
                    target.write_bytes(b"target original\n")

                store = DocumentStore()
                store.load(source)
                original_snapshot = store._snapshot_target
                calls = 0

                def racing_snapshot(path: Path):
                    nonlocal calls
                    calls += 1
                    if calls == 1:
                        return original_snapshot(path)
                    if case == "created":
                        path.write_bytes(b"created by other actor\n")
                    elif case == "deleted":
                        path.unlink()
                    else:
                        path.write_bytes(b"modified by other actor\n")
                    return original_snapshot(path)

                with patch.object(store, "_snapshot_target", side_effect=racing_snapshot):
                    with self.assertRaises(EditorError):
                        store.save_as(target, "my save\n")

                if case == "created":
                    self.assertEqual(target.read_bytes(), b"created by other actor\n")
                elif case == "deleted":
                    self.assertFalse(target.exists())
                else:
                    self.assertEqual(target.read_bytes(), b"modified by other actor\n")
                self.assertEqual(self.temp_residue(target), [])
                self.assertEqual(store.current_path, source.resolve())

    def test_modified_save_preserves_bom_and_file_level_crlf(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.copy_fixture(tmp, "utf8_bom_crlf.md.bin")
            store = DocumentStore()
            store.load(path)
            store.save("# Changed\n\nline\n")
            self.assertEqual(
                path.read_bytes(),
                b"\xef\xbb\xbf" + "# Changed\r\n\r\nline\r\n".encode("utf-8"),
            )
            self.assertEqual(store.eol_kind, "CRLF")

    def test_modified_save_preserves_lf_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.copy_fixture(tmp, "utf8_lf.md.bin")
            store = DocumentStore()
            store.load(path)
            store.save("# Changed\nline\n")
            self.assertEqual(path.read_bytes(), b"# Changed\nline\n")
            self.assertEqual(store.eol_kind, "LF")

    def test_final_and_no_final_newline_noop_fidelity(self):
        for fixture in ("utf8_lf.md.bin", "utf8_no_final_newline.md.bin"):
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as tmp:
                path = self.copy_fixture(tmp, fixture)
                store = DocumentStore()
                content = store.load(path)["content"]
                before = path.read_bytes()
                store.save(content)
                self.assertEqual(path.read_bytes(), before)

    def test_unicode_and_emoji_noop_fidelity(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.copy_fixture(tmp, "unicode_emoji.md.bin")
            store = DocumentStore()
            content = store.load(path)["content"]
            before = path.read_bytes()
            store.save(content)
            self.assertEqual(path.read_bytes(), before)

    def test_read_only_fact_is_upfront_and_unchanged_save_is_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.copy_fixture(tmp, "utf8_lf.md.bin")
            store = DocumentStore()
            state = store.load(path)
            path.chmod(0o444)
            try:
                state = store.state(state["content"])
                self.assertTrue(state["read_only"])
                with patch.object(store, "_safe_write", wraps=store._safe_write) as safe_write:
                    store.save(state["content"])
                self.assertEqual(safe_write.call_count, 0)
                with self.assertRaises(EditorError):
                    store.save(state["content"] + "changed\n")
            finally:
                path.chmod(0o644)

    def test_file_facts_and_eol_kind(self):
        expected = {
            "no_eol.md.bin": "NONE",
            "utf8_lf.md.bin": "LF",
            "utf8_bom_crlf.md.bin": "CRLF",
            "cr_only.md.bin": "CR",
            "mixed_eol.md.bin": "MIXED",
        }
        for fixture, eol_kind in expected.items():
            with self.subTest(fixture=fixture), tempfile.TemporaryDirectory() as tmp:
                path = self.copy_fixture(tmp, fixture)
                state = DocumentStore().load(path)
                self.assertEqual(state["eol_kind"], eol_kind)
                self.assertEqual(state["encoding"], "UTF-8 BOM" if state["has_bom"] else "UTF-8")
                self.assertIn("read_only", state)


if __name__ == "__main__":
    unittest.main()
