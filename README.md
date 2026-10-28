# Markdown Reader & Editor

**A Markdown editor that changes only what you changed.**

*A file-faithful Markdown reader & quick editor for Windows.*

`faithful-markdown` is a small local tool for reviewing Markdown and making focused corrections without creating unrelated file churn.

Core workflow: `Open -> Review -> Fix -> Save -> Close`

## Images

Use 插入图片 or copy one image file / a screenshot and press Ctrl+V in the editor. Supported formats: PNG, JPEG, GIF, WebP, BMP, up to 12 MB per image. Screenshots are saved as PNG. Save an unnamed document first (after saving, paste the image again).

Images are copied into `<document name>.assets` beside the Markdown file and referenced with relative paths. Move the Markdown file together with that folder. Undo removes the reference but retains the image file. Save As does not relocate existing image folders; move/copy them with the document when changing directories.

## Sharing and printing

File → 打印／另存为 PDF prints the current rendered document, including unsaved edits. Choose Microsoft Print to PDF / Save as PDF in the system print dialog. Only reading content prints; default pagination, no custom export settings. Packaged native printing acceptance is tracked in PROJECT_STATE.md.

## Document navigation

The toolbar keeps Open and Save visible. File contains Save As, image insertion and Print/PDF; View contains pane toggles, outline, syntax help and Find; Settings contains Windows registration. Menus close on selection, outside click or Escape. Existing keyboard shortcuts remain available.

- `Ctrl+F` opens case-insensitive text search. Enter / Shift+Enter or the arrow buttons move between matches; Escape closes search. Editing mode searches the Markdown source; reading mode searches rendered text within each text node.
- Toggle 编辑, 阅读 and 语法 independently; at least editor or reading remains visible. Drag separators between visible panes to resize, or focus them and use Left / Right. Layout changes apply only to this window.
- View → 目录 opens a heading outline to the right of reading; hiding reading hides the outline. The read-only syntax reference opens at the far right and never replaces the document.
- At the end of a list item, Enter continues bullets, numbers or unchecked tasks while retaining indentation. Enter on an empty item ends it. Shift+Enter inserts a plain newline; fenced code and IME confirmation are not continued. Ctrl+Z undoes the insertion. Indent nested lists with four spaces; each level numbers independently.
- Pane visibility/width and search affect only the current window. List continuation edits the document and can be undone; layout preferences are not persisted.

Browser smoke check (requires an existing Playwright installation and Microsoft Edge): `node tests/ui_navigation.cjs`. It checks the UI with a stubbed Python bridge, not the packaged Windows application.

## Content fidelity

V2.1 centers on three rules:

1. **No change means no write.** Unchanged Save performs no disk write.
2. **External changes are never silently overwritten.** If the file changes on disk after opening, Save is blocked.
3. **Saving should not create unrelated content churn.** Normal edits preserve the supported encoding, UTF-8 BOM state, and file-level LF / CRLF policy.

The UI also exposes concise File Facts and detects obvious Windows read-only state up front.

## Download and current status

Download the portable FaithfulMarkdown.exe from [GitHub Releases](https://github.com/Javenzeng/faithful-markdown/releases). Close the old program before replacing its EXE. Current version and verification limitations: PROJECT_STATE.md; historical acceptance: MILESTONES.md. Test/build success is not Human packaged acceptance.

## Run from source

Target: Windows 10/11 x64, WebView2 Runtime, Python 3.10-3.13 x64.

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open a file directly:

```powershell
.\.venv\Scripts\python.exe app.py README.md
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## Windows packaging

`build_windows.ps1` is the current Windows build entrypoint.

The historical accepted V2 executable is intentionally excluded from Git history; only its SHA-256 metadata and acceptance evidence are retained.

The published Windows application is available through GitHub Releases. Release records distinguish automated verification from Human acceptance.

## Known boundaries

V2.1 does not claim complete preservation or guarantees for ACL/DACL, Alternate Data Streams, filesystem timestamps/metadata, compression/encryption metadata, symlink/junction semantics, network/sync-drive replacement semantics, edited mixed-EOL per-position preservation, every possible system-level TOCTOU race, or reproducible packaging.

## Non-goals

No multi-tab feature race, workspace/file tree, Git client, AI, cloud sync, plugins, knowledge base, WYSIWYG, or similar feature-bloat competition.

## Engineering records

Development reached accepted V2.1 before this Git repository existed. Selected design decisions, incidents, failed approaches, regression evidence, and Human acceptance records are preserved under `records/`.

No fictional or backdated Git history is reconstructed.

## License

MIT. See `LICENSE`.
