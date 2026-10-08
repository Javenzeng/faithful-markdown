# Markdown Reader & Editor

**A Markdown editor that changes only what you changed.**

*A file-faithful Markdown reader & quick editor for Windows.*

`faithful-markdown` is a small local tool for reviewing Markdown and making focused corrections without creating unrelated file churn.

Core workflow: `Open -> Review -> Fix -> Save -> Close`

## Document navigation

- `Ctrl+F` opens case-insensitive text search. Enter / Shift+Enter or the arrow buttons move between matches; Escape closes search. Editing mode searches the Markdown source; reading mode searches rendered text within each text node.
- Drag the divider to resize the editor and preview (20–80%), or focus it and use Left / Right. Narrow windows retain the single-pane layout.
- The 目录 button opens a collapsible heading outline. Clicking a heading scrolls the preview to that section; in narrow windows it switches to reading mode.
- These controls affect only the current window and do not change document content or save preferences.

Browser smoke check (requires an existing Playwright installation and Microsoft Edge): `node tests/ui_navigation.cjs`. It checks the UI with a stubbed Python bridge, not the packaged Windows application.

## Content fidelity

V2.1 centers on three rules:

1. **No change means no write.** Unchanged Save performs no disk write.
2. **External changes are never silently overwritten.** If the file changes on disk after opening, Save is blocked.
3. **Saving should not create unrelated content churn.** Normal edits preserve the supported encoding, UTF-8 BOM state, and file-level LF / CRLF policy.

The UI also exposes concise File Facts and detects obvious Windows read-only state up front.

## Current accepted baseline

Current accepted source baseline: **V2.1 — Content Fidelity Contract**.

Pre-Git evidence under `records/` includes:

- source regression after the P0 fix: **24/24 PASS**
- Human Windows real-machine acceptance: **H1-H7 PASS**
- P0 cold-start retest: **5/5 PASS**

These are pre-Git acceptance records, not GitHub CI results.

## Run from source

Target: Windows 10/11 x64, WebView2 Runtime, Python 3.10-3.13 x64.

```powershell
py -3 -m venv .venv
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

The published Windows application is available through GitHub Releases. V2.8 adds document search, a resizable split view, and a collapsible heading outline; its release record distinguishes automated verification from Human acceptance.

## Known boundaries

V2.1 does not claim complete preservation or guarantees for ACL/DACL, Alternate Data Streams, filesystem timestamps/metadata, compression/encryption metadata, symlink/junction semantics, network/sync-drive replacement semantics, edited mixed-EOL per-position preservation, every possible system-level TOCTOU race, or reproducible packaging.

## Non-goals

No multi-tab feature race, workspace/file tree, Git client, AI, cloud sync, plugins, knowledge base, WYSIWYG, or similar feature-bloat competition.

## Engineering records

Development reached accepted V2.1 before this Git repository existed. Selected design decisions, incidents, failed approaches, regression evidence, and Human acceptance records are preserved under `records/`.

No fictional or backdated Git history is reconstructed.

## License

MIT. See `LICENSE`.
