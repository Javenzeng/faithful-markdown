# Current UI foundation

Released product: local Markdown reading and focused editing. DocumentStore owns document identity, encoding and save lifecycle; the existing Python bridge remains unchanged.

Editor text is the current editable content. Preview, heading outline and search results are projections. Syntax examples are static, read-only help and never replace the current document.

Window order: editor → preview → outline → syntax. Editor and preview are independently toggled, with at least one visible. Outline follows preview visibility. Syntax defaults closed. Adjacent visible panes resize in the current window; no layout persistence. Existing colors, buttons and separator primitives are retained.

List continuation applies only to unmodified Enter at an unselected list-line end outside fenced code. Preserve indentation and bullet style, increment numeric markers, reset new tasks to unchecked; an empty list item removes its marker. Shift+Enter and IME composition keep native behavior. Changes flow through the existing input/dirty/render path and native undo; save semantics remain unchanged.

Decision: native Chromium editing command | direct textarea replacement considered | use insertText to retain undo | existing WebView2 runtime | deprecated browser API, verified against Edge; recheck on runtime change or undo failure.
