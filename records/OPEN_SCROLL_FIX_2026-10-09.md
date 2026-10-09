# V2.9.1 — document-load position

Human reported editor at bottom while reading starts at top. applyDocument replaced text without resetting caret or scroll. Added three initialization lines to reset caret and both pane scroll axes; ordinary render/save paths unchanged.

Edge regression PASS: switch from scrolled document, focus editor, both panes and caret at zero; ordinary preview refresh preserves scroll. Existing UI checks and build Python suite PASS. Packaged Human acceptance pending.

Source `bbdcf30788af0ddaece8a9921317c000de967769`; artifact `releases/v2.9.1/FaithfulMarkdown.exe`, 13,261,988 bytes, SHA-256 `FA9DDF2EEAE27AB0A9665C83F76765109571DF1CFCC15CC64C03F9EF6C10C2A2`.

Build dependency resolver selected pycparser 3.11; PyInstaller warned that pycparser.lextab/yacctab hidden imports were absent. Build succeeded; no packaged runtime acceptance claimed. Dependency download retried once after a read timeout and succeeded.
