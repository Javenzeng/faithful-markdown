# Document navigation — local implementation

V2.8.1 correction: Human requested the outline on the right, adjacent to reading. Moved its DOM position and changed its border to the left; no new runtime logic. Edge position/navigation checks and build Python suite PASS. Source `291a8609633c1e7eb7183eee634a6e1e6e928f99`; EXE `releases/v2.8.1/FaithfulMarkdown.exe`, 13,258,730 bytes, SHA-256 `C5ADB45F68E80B8BB10EE43E06363736D986E42BD041008DB238AD8F238CC8C9`. Human packaged acceptance pending.

Human authorized document search, a draggable editor/preview divider, and a collapsible heading outline. Scope: existing front-end only; no new runtime dependency, persistence, file tree, replacement search, or Python API.

Implemented in `assets/index.html`. Outline derives from rendered h1–h6 elements. Search is case-insensitive and mode-specific (source in edit mode, rendered text nodes in reading mode). Split width is transient and clamped to 20–80%.

Verification: headless Microsoft Edge browser smoke PASS for search counts, previous/next wrap, editor selection and scrolling, reading highlights and clearing, divider pointer drag, heading navigation, narrow-window reading transition, no dirty-state change, and no JavaScript errors. Bridge is stubbed; packaged Windows acceptance remains unverified.

JavaScript syntax and Git diff whitespace checks PASS. Existing Python suite could not import: available Python interpreters lack `mistune`. Python application and save/render APIs were not changed.

## Packaging and publication

Human subsequently authorized packaging and GitHub synchronization. Built with Python 3.13.15 x64, PyInstaller 6.22.2, pywebview 6.2.1, and mistune 3.2.1 in the existing isolated build workflow. Python regression suite PASS, resolving the earlier missing-dependency limitation.

- Release source commit: `00081fa3f34b4cae6ea680ecbd920d5d96bfb43c`.
- Artifact: `releases/v2.8/FaithfulMarkdown.exe`, 13,256,830 bytes.
- SHA-256: `0348339A7854DB0F9A28B8504A599393D1BF83ED7853E0DFA609D9E0D437D288`.
- GitHub Release: https://github.com/Javenzeng/faithful-markdown/releases/tag/v2.8 ; uploaded asset digest and size verified through GitHub API.
- Source push succeeded using single-command Git proxy configuration; no global configuration change.
- Packaged launch created a responding process, but hidden-window launch did not expose a window title. This is not evidence of visual or feature acceptance. Human packaged feature acceptance remains pending.
