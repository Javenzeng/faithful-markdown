# Image insertion

Authorized: local image selection, Explorer image-file copy/paste and screenshot paste; PNG/JPEG/GIF/WebP/BMP. Copy to document-name.assets; screenshot PNG; relative URL-encoded references; save unnamed document first; no automatic deletion on undo.

Implementation uses existing pythonnet WinForms clipboard in an STA worker; no new runtime dependency. File assets are created immediately while Markdown remains unsaved until explicit Save. Existing 12 MB preview limit applies. Save As asset relocation is outside scope.

Verification: 31 Python tests PASS; existing Edge UI smoke PASS. Actual current Windows image clipboard was imported into a disposable document folder and previewed as an inline image successfully; clipboard content was not changed. Image import tests cover relative paths, Unicode/spaces, distinct names, unsaved/unsupported/oversized rejection. Packaged UI and Explorer CF_HDROP end-to-end remain unverified.
