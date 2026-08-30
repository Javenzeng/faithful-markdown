from __future__ import annotations

import inspect
import sys
import types
import unittest


# This test verifies EditorAPI's Python surface, not pywebview internals.
# The project runtime dependency may be absent in a non-Windows unit-test environment.
if "webview" not in sys.modules:
    try:
        import webview  # noqa: F401
    except ModuleNotFoundError:
        sys.modules["webview"] = types.SimpleNamespace()

from app import EditorAPI
from core import DocumentStore


EXPECTED_PUBLIC_METHODS = {
    "bind_window",
    "initial_state",
    "set_dirty",
    "render",
    "open_file",
    "save",
    "save_as",
    "open_external",
    "register_with_windows",
    "unregister_from_windows",
}


class EditorAPISurfaceTests(unittest.TestCase):
    def test_window_reference_is_private(self):
        api = EditorAPI(DocumentStore())
        self.assertFalse(hasattr(api, "window"))
        self.assertTrue(hasattr(api, "_window"))
        self.assertIsNone(api._window)

    def test_bind_window_keeps_reference_private(self):
        api = EditorAPI(DocumentStore())
        sentinel = object()
        api.bind_window(sentinel)
        self.assertFalse(hasattr(api, "window"))
        self.assertIs(api._window, sentinel)

    def test_public_method_surface_did_not_expand(self):
        public_methods = {
            name
            for name, value in EditorAPI.__dict__.items()
            if not name.startswith("_") and inspect.isfunction(value)
        }
        self.assertEqual(public_methods, EXPECTED_PUBLIC_METHODS)


if __name__ == "__main__":
    unittest.main()
