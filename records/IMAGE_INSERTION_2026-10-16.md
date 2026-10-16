# Image insertion

V2.10 packaged from `7e4e27433e37bfd07d70c247b9ddcadb3aaa731f` using existing isolated build; 31 tests PASS. EXE `releases/v2.10/FaithfulMarkdown.exe`, 13,264,246 bytes. SHA-256 `71ACF99666AD3F8DA0E1F5429E8B161D6A0723EB22644C3EFC5F3E27CB6AED0D`. GitHub v2.10 publication authorized by Human; packaged acceptance remains pending.

Authorized: local image selection, Explorer image-file copy/paste and screenshot paste; PNG/JPEG/GIF/WebP/BMP. Copy to document-name.assets; screenshot PNG; relative URL-encoded references; save unnamed document first; no automatic deletion on undo.

Implementation uses existing pythonnet WinForms clipboard in an STA worker; no new runtime dependency. File assets are created immediately while Markdown remains unsaved until explicit Save. Existing 12 MB preview limit applies. Save As asset relocation is outside scope.

Verification: 31 Python tests PASS; existing Edge UI smoke PASS. Actual current Windows image clipboard was imported into a disposable document folder and previewed as an inline image successfully; clipboard content was not changed. Image import tests cover relative paths, Unicode/spaces, distinct names, unsaved/unsupported/oversized rejection. Packaged UI and Explorer CF_HDROP end-to-end remain unverified.
