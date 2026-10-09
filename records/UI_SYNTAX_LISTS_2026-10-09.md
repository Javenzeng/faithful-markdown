# V2.9 — syntax reference, pane controls and list continuation

Human authorized an inline syntax pane after the outline, independent editor/reading/syntax controls and resizable visible panes, plus list continuation. Replaced the prior exclusive edit/read mode and fixed split logic. No new runtime dependency or Python API; layout has no persistence.

Edge smoke PASS: existing navigation/search; right-side outline; syntax placement; hiding reading/outline while retaining syntax; last document-pane guard; content preservation; numbered/bullet/nested/task continuation; empty-item exit; fenced-code exclusion; Shift+Enter; Ctrl+Z restoration; dirty state. Test bridge is stubbed. Human packaged acceptance remains pending.

The first test run targeted a section with inputValue instead of its textarea; corrected the test selector and reran successfully. This was a test harness error, not product evidence.
