# Document navigation — local implementation

Human authorized document search, a draggable editor/preview divider, and a collapsible heading outline. Scope: existing front-end only; no new runtime dependency, persistence, file tree, replacement search, or Python API.

Implemented in `assets/index.html`. Outline derives from rendered h1–h6 elements. Search is case-insensitive and mode-specific (source in edit mode, rendered text nodes in reading mode). Split width is transient and clamped to 20–80%.

Verification: headless Microsoft Edge browser smoke PASS for search counts, previous/next wrap, editor selection and scrolling, reading highlights and clearing, divider pointer drag, heading navigation, narrow-window reading transition, no dirty-state change, and no JavaScript errors. Bridge is stubbed; packaged Windows acceptance remains unverified.

JavaScript syntax and Git diff whitespace checks PASS. Existing Python suite could not import: available Python interpreters lack `mistune`. Python application and save/render APIs were not changed.

No new EXE built and no GitHub publication performed. Existing v2.7 remains the published release.
