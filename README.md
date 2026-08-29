# Markdown Reader & Editor

**A Markdown editor that changes only what you changed.**

*A file-faithful Markdown reader & quick editor for Windows.*

`faithful-markdown` is a small local tool for reviewing Markdown and making focused corrections without creating unrelated file churn.

Core workflow: `Open -> Review -> Fix -> Save -> Close`

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

V2.1 is an accepted **source** baseline. It does not yet have an accepted packaged artifact, and packaging is not claimed to be reproducible.

## Known boundaries

V2.1 does not claim complete preservation or guarantees for ACL/DACL, Alternate Data Streams, filesystem timestamps/metadata, compression/encryption metadata, symlink/junction semantics, network/sync-drive replacement semantics, edited mixed-EOL per-position preservation, every possible system-level TOCTOU race, or reproducible packaging.

## Non-goals

No multi-tab feature race, workspace/file tree, Git client, AI, cloud sync, plugins, knowledge base, WYSIWYG, or similar feature-bloat competition.

## Engineering records

Development reached accepted V2.1 before this Git repository existed. Selected design decisions, incidents, failed approaches, regression evidence, and Human acceptance records are preserved under `records/`.

No fictional or backdated Git history is reconstructed.

## License

MIT. See `LICENSE`.
