from __future__ import annotations

import sys
import webbrowser
from pathlib import Path
from threading import Thread
from time import sleep

import webview

from core import DocumentStore, EditorError, render_markdown


APP_TITLE = "Markdown Reader & Editor"
MARKDOWN_TYPES = ("Markdown files (*.md;*.markdown)", "All files (*.*)")


class EditorAPI:
    def __init__(self, store: DocumentStore, initial_content: str = "", startup_error: str | None = None):
        self.store = store
        self.initial_content = initial_content
        self.startup_error = startup_error
        self._window: webview.Window | None = None
        self.dirty = False
        self.close_prompt_pending = False
        self.allow_close = False

    def bind_window(self, window: webview.Window) -> None:
        self._window = window

    def initial_state(self) -> dict:
        state = self.store.state(self.initial_content)
        state["startup_error"] = self.startup_error
        return state

    def set_dirty(self, dirty: bool) -> None:
        self.dirty = bool(dirty)

    def render(self, content: str) -> dict:
        try:
            return {"ok": True, "html": render_markdown(content, self.store.base_dir)}
        except Exception as exc:
            return {"ok": False, "error": f"Markdown 渲染失败：{exc}"}

    def open_file(self) -> dict:
        if not self._window:
            return {"ok": False, "error": "窗口尚未初始化。"}
        result = self._window.create_file_dialog(
            webview.FileDialog.OPEN,
            allow_multiple=False,
            file_types=MARKDOWN_TYPES,
        )
        if not result:
            return {"ok": False, "cancelled": True}
        return self._load_path(result[0])

    def save(self, content: str) -> dict:
        try:
            if not self.store.current_path:
                return self.save_as(content)
            document = self.store.save(content)
            self.dirty = False
            return {"ok": True, "document": document}
        except EditorError as exc:
            return {"ok": False, "error": str(exc)}

    def save_as(self, content: str) -> dict:
        if not self._window:
            return {"ok": False, "error": "窗口尚未初始化。"}

        current_name = self.store.current_path.name if self.store.current_path else "未命名.md"
        directory = str(self.store.base_dir) if self.store.base_dir else ""
        result = self._window.create_file_dialog(
            webview.FileDialog.SAVE,
            directory=directory,
            save_filename=current_name,
            file_types=MARKDOWN_TYPES,
        )
        if not result:
            return {"ok": False, "cancelled": True}

        try:
            document = self.store.save_as(result[0], content)
            self.dirty = False
            return {"ok": True, "document": document}
        except EditorError as exc:
            return {"ok": False, "error": str(exc)}

    def open_external(self, url: str) -> dict:
        if not url.startswith(("https://", "http://", "mailto:")):
            return {"ok": False, "error": "仅允许打开 http(s) 或 mailto 链接。"}
        webbrowser.open(url)
        return {"ok": True}

    def _load_path(self, path: str) -> dict:
        try:
            document = self.store.load(path)
            self.initial_content = document["content"]
            self.dirty = False
            return {"ok": True, "document": document}
        except EditorError as exc:
            return {"ok": False, "error": str(exc)}
        except OSError as exc:
            return {"ok": False, "error": f"无法打开文件：{path}\n{exc}"}


def has_webview2_runtime() -> bool:
    if sys.platform != "win32":
        return True

    import winreg

    client_id = r"{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
    locations = (
        (winreg.HKEY_CURRENT_USER, rf"Software\Microsoft\EdgeUpdate\Clients\{client_id}"),
        (winreg.HKEY_LOCAL_MACHINE, rf"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{client_id}"),
        (winreg.HKEY_LOCAL_MACHINE, rf"SOFTWARE\Microsoft\EdgeUpdate\Clients\{client_id}"),
    )
    for hive, key_path in locations:
        try:
            with winreg.OpenKey(hive, key_path) as key:
                version, _ = winreg.QueryValueEx(key, "pv")
            if version and str(version).strip() not in {"", "0.0.0.0"}:
                return True
        except OSError:
            continue
    return False


def show_windows_error(message: str) -> None:
    if sys.platform != "win32":
        return
    import ctypes
    ctypes.windll.user32.MessageBoxW(None, message, APP_TITLE, 0x10)


def resource_path(relative: str) -> Path:
    root = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return root / relative


def load_startup_document(argv: list[str]) -> tuple[DocumentStore, str, str | None]:
    store = DocumentStore()
    if len(argv) < 2:
        return store, "", None

    try:
        state = store.load(argv[1])
        return store, state["content"], None
    except (EditorError, OSError) as exc:
        return store, "", str(exc)


def main() -> None:
    if sys.platform == "win32" and not has_webview2_runtime():
        show_windows_error(
            "未检测到 Microsoft Edge WebView2 Runtime。\n\n"
            "请先安装 WebView2 Runtime 后再启动 Markdown Reader & Editor。"
        )
        return

    store, initial_content, startup_error = load_startup_document(sys.argv)
    api = EditorAPI(store, initial_content, startup_error)

    index_path = resource_path("assets/index.html")
    window = webview.create_window(
        APP_TITLE,
        url=index_path.as_uri(),
        js_api=api,
        width=1220,
        height=780,
        min_size=(820, 560),
        background_color="#f6f7f9",
        text_select=True,
        confirm_close=False,
    )
    api.bind_window(window)

    def on_closing() -> bool | None:
        if api.allow_close or not api.dirty:
            return None
        if not api.close_prompt_pending:
            api.close_prompt_pending = True

            def confirm_close() -> None:
                import ctypes

                sleep(0.1)
                result = ctypes.windll.user32.MessageBoxW(
                    None,
                    "当前 Markdown 文件还有未保存的修改。确定要关闭并丢弃这些修改吗？",
                    "未保存的修改",
                    0x2031,
                )
                api.close_prompt_pending = False
                if result == 1:
                    api.allow_close = True
                    window.destroy()

            Thread(target=confirm_close, daemon=True).start()
        return False

    window.events.closing += on_closing
    gui = "edgechromium" if sys.platform == "win32" else None
    webview.start(gui=gui, debug=False)


if __name__ == "__main__":
    main()
