from __future__ import annotations

import base64
import hashlib
import mimetypes
import os
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse

import mistune

UTF8_BOM = b"\xef\xbb\xbf"
MAX_INLINE_IMAGE_BYTES = 12 * 1024 * 1024

class EditorError(RuntimeError):
    """A user-facing editor error."""

def _fingerprint(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def _canonical_text(content: str) -> str:
    return content.replace("\r\n", "\n").replace("\r", "\n")

def _editor_fingerprint(content: str) -> bytes:
    return _fingerprint(_canonical_text(content).encode("utf-8"))

def _detect_eol_kind(content: str) -> str:
    remainder = content.replace("\r\n", "")
    kinds = [kind for kind, present in (("CRLF", "\r\n" in content), ("LF", "\n" in remainder), ("CR", "\r" in remainder)) if present]
    return "NONE" if not kinds else kinds[0] if len(kinds) == 1 else "MIXED"

@dataclass
class DocumentStore:
    current_path: Path | None = None
    had_utf8_bom: bool = False
    line_ending: str = "\n"
    source_fingerprint: bytes | None = None
    editor_fingerprint: bytes | None = None
    eol_kind: str = "NONE"

    @property
    def base_dir(self) -> Path | None:
        return self.current_path.parent if self.current_path else None

    def load(self, path: str | Path) -> dict:
        target = Path(path).expanduser().resolve()
        if not target.is_file():
            raise EditorError(f"文件不存在：{target}")

        raw = target.read_bytes()
        had_bom = raw.startswith(UTF8_BOM)
        try:
            text = raw.decode("utf-8-sig" if had_bom else "utf-8")
        except UnicodeDecodeError as exc:
            raise EditorError(
                "仅支持 UTF-8 / UTF-8 BOM Markdown 文件。请先将该文件转换为 UTF-8 编码。"
            ) from exc

        self.current_path = target
        self.had_utf8_bom = had_bom
        self.line_ending = "\r\n" if "\r\n" in text else ("\r" if "\r" in text else "\n")
        self.source_fingerprint = _fingerprint(raw)
        self.editor_fingerprint = _editor_fingerprint(text)
        self.eol_kind = _detect_eol_kind(text)
        return self.state(text)

    def save(self, content: str) -> dict:
        if not self.current_path:
            raise EditorError("当前文档还没有保存路径。")
        try:
            current_raw = self.current_path.read_bytes()
        except OSError as exc:
            raise EditorError(f"无法读取当前文件：{self.current_path}\n{exc}") from exc
        if _fingerprint(current_raw) != self.source_fingerprint:
            raise EditorError("文件已被外部修改，已停止保存以避免覆盖外部更改。")

        incoming_fingerprint = _editor_fingerprint(content)
        if incoming_fingerprint == self.editor_fingerprint:
            return self.state(content)
        if self._is_obviously_read_only(self.current_path):
            raise EditorError(f"文件为只读或当前不可写：{self.current_path}")

        data = self._encode(content, preserve_format=True)
        self._safe_write(self.current_path, data, (True, self.source_fingerprint))
        self.source_fingerprint = _fingerprint(data)
        self.editor_fingerprint = incoming_fingerprint
        self.eol_kind = _detect_eol_kind(data[len(UTF8_BOM):].decode("utf-8") if data.startswith(UTF8_BOM) else data.decode("utf-8"))
        return self.state(content)

    def save_as(self, path: str | Path, content: str) -> dict:
        target = Path(path).expanduser()
        if target.suffix == "":
            target = target.with_suffix(".md")
        target = target.resolve()
        if self.current_path and target == self.current_path:
            return self.save(content)

        snapshot = self._snapshot_target(target)
        data = self._encode(content, preserve_format=False)
        self._safe_write(target, data, snapshot)
        self.current_path = target
        self.had_utf8_bom = False
        self.line_ending = "\n"
        self.source_fingerprint = _fingerprint(data)
        self.editor_fingerprint = _editor_fingerprint(content)
        self.eol_kind = _detect_eol_kind(data.decode("utf-8"))
        return self.state(content)

    def state(self, content: str = "") -> dict:
        return {
            "path": str(self.current_path) if self.current_path else None,
            "name": self.current_path.name if self.current_path else "未命名.md",
            "content": content,
            "has_bom": self.had_utf8_bom,
            "encoding": "UTF-8 BOM" if self.had_utf8_bom else "UTF-8",
            "line_ending": self.line_ending,
            "eol_kind": self.eol_kind,
            "read_only": self._is_obviously_read_only(self.current_path),
        }

    def _encode(self, content: str, preserve_format: bool) -> bytes:
        normalized = _canonical_text(content)
        if preserve_format and self.line_ending != "\n":
            normalized = normalized.replace("\n", self.line_ending)
        data = normalized.encode("utf-8")
        if preserve_format and self.had_utf8_bom:
            data = UTF8_BOM + data
        return data

    def _snapshot_target(self, path: Path) -> tuple[bool, bytes | None]:
        try:
            return True, _fingerprint(path.read_bytes())
        except FileNotFoundError:
            return False, None
        except OSError as exc:
            raise EditorError(f"无法核验保存目标：{path}\n{exc}") from exc

    def _safe_write(self, path: Path, data: bytes, expected_snapshot: tuple[bool, bytes | None]) -> None:
        temp_path: Path | None = None
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as temp:
                temp_path = Path(temp.name)
                temp.write(data)
            if self._snapshot_target(path) != expected_snapshot:
                raise EditorError("保存期间目标文件发生变化，已停止覆盖。")
            os.replace(temp_path, path)
            temp_path = None
        except (EditorError, OSError) as exc:
            try:
                if temp_path:
                    temp_path.unlink(missing_ok=True)
            except OSError as cleanup_exc:
                raise EditorError(f"保存失败，且临时文件清理失败：{temp_path}\n{cleanup_exc}") from exc
            if isinstance(exc, EditorError):
                raise
            raise EditorError(f"无法保存文件：{path}\n{exc}") from exc

    @staticmethod
    def _is_obviously_read_only(path: Path | None) -> bool:
        if not path:
            return False
        try:
            info = path.stat()
        except OSError:
            return False
        readonly_attr = getattr(stat, "FILE_ATTRIBUTE_READONLY", 0)
        attrs = getattr(info, "st_file_attributes", 0)
        return bool(readonly_attr and attrs & readonly_attr) or not bool(info.st_mode & stat.S_IWRITE) or not os.access(path, os.W_OK)

class LocalImageRenderer(mistune.HTMLRenderer):
    def __init__(self, base_dir: Path | None):
        super().__init__(escape=True)
        self.base_dir = base_dir

    def image(self, text: str, url: str, title: str | None = None) -> str:
        resolved = self._resolve_local_image(url)
        return super().image(text, resolved or url, title)

    def _resolve_local_image(self, url: str) -> str | None:
        if not self.base_dir:
            return None

        parsed = urlparse(url)
        if parsed.scheme in {"http", "https", "data"}:
            return None
        if parsed.scheme and len(parsed.scheme) > 1:
            return None

        raw_path = unquote(parsed.path)
        if not raw_path:
            return None

        image_path = Path(raw_path)
        if not image_path.is_absolute():
            image_path = self.base_dir / image_path

        try:
            image_path = image_path.resolve()
            if not image_path.is_file():
                return None
            if image_path.stat().st_size > MAX_INLINE_IMAGE_BYTES:
                return None
            mime_type, _ = mimetypes.guess_type(image_path.name)
            if not mime_type or not mime_type.startswith("image/"):
                return None
            encoded = base64.b64encode(image_path.read_bytes()).decode("ascii")
            return f"data:{mime_type};base64,{encoded}"
        except OSError:
            return None

def render_markdown(content: str, base_dir: Path | None) -> str:
    renderer = LocalImageRenderer(base_dir)
    markdown = mistune.create_markdown(
        renderer=renderer,
        plugins=["strikethrough", "table", "task_lists", "url"],
    )
    return markdown(content)
