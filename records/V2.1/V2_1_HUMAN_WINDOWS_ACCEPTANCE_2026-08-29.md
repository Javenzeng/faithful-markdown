# V2.1 Human Windows Real-Machine Acceptance — 2026-08-29

Project: Markdown Reader & Editor  
Milestone: V2.1 — Content Fidelity Contract  
Acceptance authority: Human  
Acceptance result: **PASS**  
Execution: **ACCEPTED**  
P0 Cold Start/API Exposure Fix: **ACCEPTED**  
Baton: **HUMAN**  
Blocker: **None**  
Packaging: **NOT_AUTHORIZED**

## Scope of this record

This record captures Human's final Windows real-machine acceptance facts. No additional tests were requested or run during this governance closeout. No source, test, requirements, build-script, product-scope, or accepted-binary files were modified.

## H1 — Cold Start Retest

**PASS 5/5**

After the P0 fix, the source version was launched and closed successfully five consecutive times:
- normal startup;
- responsive UI;
- normal close;
- no `(未响应)`;
- no `AccessibilityObject...`;
- no `maximum recursion depth exceeded`.

Human conclusion: the P0 cold-start/API-exposure regression is resolved on the accepted Windows machine.

## H2 — File Facts + Edit/Save

**PASS**

On a real Windows NTFS UTF-8/LF file:
- UI correctly displayed `UTF-8 | LF`;
- edit succeeded;
- Ctrl+S succeeded;
- disk readback confirmed the change was actually written.

## H3 — No-op Save

**PASS**

For the same file with no editor changes, Ctrl+S produced:
- identical SHA-256 before and after;
- identical LastWriteTime before and after.

Human acceptance statement:

> **No change means no write.**

## H4 — External Change Guard

**PASS**

In the real GUI workflow:
- the app held an unsaved local edit;
- PowerShell externally modified the disk file;
- Ctrl+S was explicitly blocked;
- UI displayed: `文件已被外部修改，已停止保存以避免覆盖外部更改`;
- external disk bytes remained intact;
- no silent overwrite occurred;
- the app remained responsive.

## H5 — Windows Read-only + Save As

**PASS**

For a real Windows `attrib +R` file:
- open immediately displayed `Read Only`;
- editing was blocked;
- Save As remained available;
- omitting the extension automatically produced `.md`;
- the new copy became a normal writable file;
- the original retained its Windows R attribute.

## H6 — UTF-8 BOM + CRLF

**PASS**

After a real edit/save cycle:
- UI still displayed `UTF-8 BOM | CRLF`;
- raw bytes still began with `EF-BB-BF`;
- EOL raw bytes remained `0D-0A`.

## H7 — Dirty Close / Lifecycle

**PASS**

- dirty state was correct;
- closing showed the native Windows unsaved confirmation;
- Cancel kept the window alive and preserved content;
- a second confirmation to discard exited normally;
- no hang or bridge deadlock occurred.

## Final Human Decision

Human formally records:
- `V2.1 Windows Real-Machine Acceptance: PASS`
- `V2.1 Execution: ACCEPTED`
- `P0 Cold Start/API Exposure Fix: ACCEPTED`
- `Baton: HUMAN`
- `Blocker: None`
- `Packaging: NOT_AUTHORIZED`

V2.1 is now the **accepted source baseline**. This does not create or replace a packaged artifact and does not modify the accepted V2 binary.

## Next Gate

**GitHub Repository Initialization**
