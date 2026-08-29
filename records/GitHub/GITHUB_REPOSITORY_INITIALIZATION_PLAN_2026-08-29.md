# GitHub Repository Initialization Plan — Publication Preflight

Date: 2026-08-29  
Project: Markdown Reader & Editor  
Accepted source baseline: V2.1  
Preflight result: **READY_FOR_HUMAN_REVIEW**  
Baton: **HUMAN**  
Repository created: **NO**  
Git initialized: **NO**  
Commit/push performed: **NO**  
Packaging/release performed: **NO**

## 1. Purpose and historical truth

This plan prepares the accepted pre-Git V2.1 source baseline for an honest public GitHub initial import. It does not reconstruct or manufacture Git history.

The first Git commit should state the truth directly, for example:

`Initial repository import: accepted V2.1 source baseline and pre-Git project records`

Do not create fake V1/V2/P0 commits, backdated commits, or reconstructed fictional history. Pre-Git engineering history remains represented by curated `records/` evidence. Git history begins at the first accepted import.

## 2. Recommended public repository boundary

### INCLUDE — runtime/source and tests

- `app.py`
- `core.py`
- `assets/**`
- `tests/**`, including the seven small fidelity byte fixtures
- `requirements.txt`
- `requirements-build.txt`
- `build_windows.ps1`

### INCLUDE — durable project governance

- `README.md` **after public-readiness rewrite**
- `AGENTS.md` **after canonical-transition wording is adjusted for GitHub**
- `PROJECT_CHARTER.md`
- `MILESTONES.md`
- `CODE_CLEANLINESS_CONTRACT.md`
- `PROJECT_STATE.md` **after canonical-transition wording is adjusted for GitHub**

### INCLUDE — curated pre-Git engineering evidence

Recommended V2 records:

- `records/V2/notes/DEVELOPMENT_NOTES.md`
- `records/V2/tests/PACKAGING_TEST_RECORD_2026-08-29.md` **after one machine-path generalization noted below**
- `records/V2/acceptance/OWNER_ACCEPTANCE_2026-08-29.md`

Recommended V2.1 records:

- `records/V2.1/V2_1_MINIMAL_IMPLEMENTATION_DESIGN_2026-08-29.md`
- `records/V2.1/V2_1_IMPLEMENTATION_RECORD_2026-08-29.md`
- `records/V2.1/V2_1_UNIT_TEST_RESULT_2026-08-29.txt`
- `records/V2.1/V2_1_P0_COLD_START_FIX_2026-08-29.md`
- `records/V2.1/V2_1_P0_UNIT_TEST_RESULT_2026-08-29.txt`
- `records/V2.1/V2_1_HUMAN_WINDOWS_ACCEPTANCE_2026-08-29.md`

GitHub preflight evidence:

- `records/GitHub/GITHUB_REPOSITORY_INITIALIZATION_PLAN_2026-08-29.md`

### INCLUDE — historical release metadata only

- `releases/V2/accepted/SHA256.txt`

Do **not** include the accepted V2 EXE in Git history.

## 3. Files/folders recommended for exclusion

### Exclude from the public repository initial import

- `SESSION_STATE.md` — keep as Drive-side Relay/session coordination state rather than durable public source history.
- `records/V2/handoffs/STARTUP_FIX_HANDOFF.md` — useful during the original execution, but now stale/redundant and contains obsolete artifact-location guidance.
- `records/V2/handoffs/CODEX_HANDOFF.md` — execution handoff, not durable public evidence; contains obsolete pre-acceptance workflow instructions.
- `records/V2/notes/build_mac.sh` — historical/unsupported side path, not part of the current Windows public product boundary.
- `releases/V2/accepted/Markdown_Reader_Editor.exe` — historical accepted artifact remains in Drive only.
- `.venv/`, `venv/`
- `__pycache__/`, `*.pyc`, `*.pyo`
- `build/`, `build_*/`
- `dist/`, `dist_*/`
- generated PyInstaller `*.spec` unless a future Human decision explicitly promotes a specific spec to source input
- temporary files such as `*.tmp`
- other ephemeral build/cache/log spam not intentionally promoted into `records/`

### Why `SESSION_STATE.md` should not live long-term in GitHub

`SESSION_STATE.md` has real multi-session coordination value, but it is intentionally short-lived and changes with Baton/task checkpoints. Committing it would create operational churn that is not source history. After GitHub becomes canonical source, keep `SESSION_STATE.md` in the Drive governance/Relay surface.

Because current `AGENTS.md` says `SESSION_STATE.md` is the short-term authority and assumes the Drive project is canonical, the later Human-approved import preparation should update `AGENTS.md` so public GitHub checkout instructions do not depend on a missing repo-local `SESSION_STATE.md`.

### Why `PROJECT_STATE.md` should remain public

`PROJECT_STATE.md` contains durable engineering facts: accepted baseline, current milestone, major decisions, authorization/release boundaries, and evidence links. That is legitimate public project state. Keep it in GitHub long-term, but after the first import it should identify GitHub commit/release facts as canonical source facts and stop describing the Drive source tree as canonical.

## 4. Debug and incident records that should remain public

Preserve engineering evidence, not cosmetic cleanliness.

Keep public:

- V2 development/design decisions relevant to the architecture reduction.
- V2 packaging/test record, including the pywebview bridge re-entry deadlock, the failed delay workaround, build cache permission failure, and the final root-cause fix.
- V2 Human owner acceptance.
- V2.1 minimal implementation design.
- V2.1 implementation record and unit-test outputs.
- V2.1 P0 `AccessibilityObject...` recursion/API-exposure incident, root-cause analysis, minimal fix, and regression evidence.
- V2.1 Human Windows acceptance H1-H7.
- Fidelity evidence for No-op Save, external-change protection, BOM/EOL behavior, read-only behavior, and race/failure tests.

Do not preserve as public history merely because it once existed:

- repeated `Empty.Empty.Empty...` console spam beyond the concise incident description;
- raw temporary console dumps with no engineering context;
- cache/build directory dumps;
- transient handoff instructions already superseded by durable evidence;
- ephemeral build outputs.

Principle: **Preserve evidence, remove noise.**

## 5. Public-safety audit

Publication scan covered the governance/publication files, runtime source, UI source, tests, build entrypoint, selected V2/V2.1 records, and release metadata. No credential-class secret was found.

### A. PUBLIC-SAFE ENGINEERING CONTEXT

Safe to retain:

- dependency versions and public upstream URLs;
- SHA-256 values and artifact file size;
- `%TEMP%` as an abstract Windows location;
- `.venv`, `build`, `dist`, WebView2, registry/runtime capability references;
- unit-test names/results;
- incident strings such as `AccessibilityObject...` and `maximum recursion depth exceeded` when kept as concise evidence;
- generic statements that the project was previously located on a synced drive;
- the JavaScript identifier `renderToken` / local variable `token`; these are render-order counters, not credentials.

### B. SHOULD GENERALIZE BEFORE PUBLICATION

One explicit machine-specific path was found:

- `records/V2/tests/PACKAGING_TEST_RECORD_2026-08-29.md`
  - contains literal `<Google Drive synced root>` in the section describing garbled console display.
  - recommendation: replace only that literal machine path with an abstract form such as `<Google Drive synced root>` or `D:\<synced-drive-root>` while preserving the incident fact.

README public cleanup is also required for identity/readiness rather than privacy:

- remove the old product reference `Pro Beauty Pro MD Viewer` from the public opening;
- remove or archive the unsupported/stale macOS packaging section unless macOS is deliberately restored as a supported target later.

### C. PRIVATE / MUST REMOVE

- **None found in the scanned publication surface.**

Specifically not found:

- API keys
- OAuth/access/refresh tokens
- passwords
- cookies
- bearer credentials
- credential-bearing private URLs
- personal email addresses
- `<Windows user profile path>`
- Google Drive IDs embedded in repository file content
- account identifiers

Therefore there is **no secret-related publication blocker** at this preflight stage.

## 6. Binary and releases boundary

Historical accepted artifact in Drive:

`releases/V2/accepted/Markdown_Reader_Editor.exe`

Recorded SHA-256:

`E706126BA63F9FD7486430EF1227721FBB58A0725CF53497573CC9FADAECBF1E`

Recommendation:

- do not copy the EXE into the clean Git working tree;
- do not commit any EXE into Git history;
- keep the accepted historical binary in Drive unchanged;
- import only its SHA-256 and supporting acceptance/provenance records;
- future public binaries belong in **GitHub Releases**, attached to a real source commit/tag, not in repository commits.

V2.1 has no accepted packaged artifact; do not imply otherwise.

## 7. Proposed minimal `.gitignore`

Recommended initial file:

```gitignore
.venv/
venv/
__pycache__/
*.py[cod]

build/
build_*/
dist/
dist_*/
*.spec

*.tmp
*.exe
```

Rationale:

- covers state the project/build script actually creates;
- prevents accidental binary commits;
- does not blanket-ignore logs because intentional evidence may belong under `records/`;
- does not ignore `.vscode/` / `.idea/` because project/editor settings could later become intentional source;
- avoids a giant generic Python template.

If a `.spec` later becomes a Human-approved build input, replace the blanket `*.spec` rule with a narrower generated-spec rule or explicit allow-list exception.

## 8. Public README change plan

Current README is a pre-V2.1 document and should not be the public landing page unchanged.

Recommended public structure:

1. **Name + positioning**
   - `A Markdown editor that changes only what you changed.`
   - optional supporting line: `A file-faithful Markdown reader & quick editor for Windows.`

2. **What it is**
   - lightweight, local/offline Windows Markdown reader + quick editor;
   - designed for small, auditable edits to project Markdown files.

3. **Fidelity contract / core behaviors**
   - No-op Save: no change means no write;
   - External Change Guard: do not silently overwrite external changes;
   - UTF-8 / UTF-8 BOM fidelity;
   - file-level LF / CRLF preservation for supported edited-file cases;
   - Read-only upfront;
   - File Facts;
   - safe local Markdown preview;
   - small auditable implementation.

4. **Run from source**
   - supported Windows environment and minimal dependency install;
   - source launch command.

5. **Tests**
   - how to run the current test suite;
   - reference accepted test/Windows evidence without claiming a new run during publication preflight.

6. **Current release/build truth**
   - accepted source baseline is V2.1;
   - historical accepted V2 binary exists only as pre-Git evidence;
   - V2.1 packaging is not yet authorized/accepted;
   - do not call the build reproducible.

7. **Known fidelity boundaries**
   - no full filesystem metadata guarantee;
   - no ACL/ADS guarantee;
   - no guarantee for sync/network-drive replacement semantics;
   - edited mixed-EOL per-position fidelity is not guaranteed;
   - residual TOCTOU/system-level save semantics remain later work.

8. **Non-goals**
   - no workspace/file tree;
   - no Git client;
   - no AI;
   - no cloud sync;
   - no plugin system;
   - no WYSIWYG feature race;
   - no feature-bloat roadmap.

Do not claim:

- full filesystem metadata preservation;
- full mixed-EOL edited preservation;
- network/sync-drive guarantees;
- ACL/ADS fidelity;
- reproducible release.

## 9. License recommendation

Offer Human only these two choices:

### Recommended: MIT

Best fit for this small public utility because it is simple, permissive, familiar, friendly to adoption/contribution, and explicitly allows commercial use with minimal compliance overhead.

### Alternative: Apache-2.0

Choose this if Human specifically wants an explicit patent license/grant and is comfortable with the longer notice/license obligations.

**Recommendation: MIT.**

Do not create `LICENSE` until Human selects the license.

## 10. Repository-name recommendations

The repository name does not need to force an immediate product display-name change.

Recommended, in order:

1. **`faithful-markdown`** — recommended; short, memorable, aligned with the fidelity principle.
2. **`markdown-fidelity-editor`** — most explicit/descriptive.
3. **`file-faithful-markdown`** — strongly communicates the core file-preservation idea.

The UI/display name may remain `Markdown Reader & Editor` until a separate Human naming decision.

## 11. Canonical source transition

### Before first GitHub import

- Google Drive = canonical source + governance + pre-Git records.
- Accepted historical V2 binary remains in Drive.

### Working-copy rule

**Never initialize `.git` inside the Google Drive synced canonical folder.**

Use a clean non-synced local working tree selected by Human, for example:

`D:\Projects\<repo-name>`

Process:

1. create the non-Drive working-copy directory;
2. copy only the Human-approved public boundary from the accepted Drive V2.1 baseline;
3. apply the approved publication-only text adjustments in that clean tree (README, one path generalization, governance canonical wording, `.gitignore`, chosen LICENSE);
4. verify import integrity;
5. only then run `git init` in the non-Drive working tree;
6. review staged content before the first commit;
7. create one truthful initial commit;
8. create/connect the GitHub repository and push only after Human approval.

### After the first accepted GitHub import

- **GitHub repository = canonical source + Git history**.
- Google Drive = governance / Relay coordination / archival evidence mirror.
- `SESSION_STATE.md` remains Drive-side short-lived coordination state.
- accepted historical binaries may remain in Drive.
- future public release binaries use GitHub Releases.
- `.git` must never be placed in the synced Drive canonical/archive folder.

## 12. Initial-import integrity procedure

After the clean working tree is assembled but before first commit/push:

1. **Inventory the accepted source baseline**
   - enumerate runtime source, assets, tests, requirements, build entrypoint, selected governance, selected records, release metadata.

2. **Byte/hash comparison for protected source/test content**
   - compute SHA-256 for runtime source and tests in the accepted Drive baseline;
   - compute SHA-256 for the copied working-tree versions;
   - require byte-identical equality for files that are not intentionally publication-edited.

3. **Explicitly account for publication-only text edits**
   - README rewrite;
   - packaging-record path generalization;
   - GitHub canonical-transition wording in governance files approved by Human;
   - new `.gitignore`;
   - Human-selected `LICENSE`;
   - this GitHub preflight record.

4. **Confirm binary exclusion**
   - no `*.exe` in staged repository content;
   - accepted V2 EXE remains only in Drive;
   - `releases/V2/accepted/SHA256.txt` may be present.

5. **Confirm ephemeral-state exclusion**
   - no `.venv/`, `venv/`, `__pycache__/`, build/dist directories, generated spec, cache or temporary output.

6. **Run publication secret/privacy scan**
   - secrets must PASS;
   - if any real credential is found, **BLOCK immediately** and return to Human rather than silently sanitizing and continuing;
   - machine-specific path findings must be explicitly classified/generalized.

7. **Evidence handling**
   - cite accepted unit-test and Human Windows acceptance records from V2.1;
   - do not rerun tests merely for this publication preflight unless Human separately authorizes it;
   - do not imply tests were newly run during import if they were not.

8. **Review first commit contents before commit/push**
   - inspect full staged file list;
   - inspect staged diff for publication-edited text;
   - verify no generated/binary files;
   - verify first commit message truthfully describes a pre-Git accepted baseline import.

9. **First commit wording**

Recommended:

`Initial repository import: accepted V2.1 source baseline and pre-Git project records`

## 13. Blockers and Human Review Gate

### Secret blocker

None found.

### Required Human decisions before mutation/import

1. approve/reject the recommended public repository boundary;
2. approve excluding `SESSION_STATE.md` from GitHub and keeping it Drive-side;
3. approve the single machine-path generalization in the V2 packaging record;
4. approve the public README rewrite plan;
5. select MIT (recommended) or Apache-2.0;
6. select a repository name;
7. select the non-Drive local working-copy path;
8. authorize the later GitHub initialization/import phase.

Until Human approval, do not create a repository, run `git init`, commit, push, package, or release.

## 14. Files changed by this preflight

Allowed preflight writes only:

- created `records/GitHub/GITHUB_REPOSITORY_INITIALIZATION_PLAN_2026-08-29.md`
- updated `PROJECT_STATE.md` only to record `GitHub Publication Preflight: READY_FOR_HUMAN_REVIEW`
- updated `SESSION_STATE.md` only to checkpoint this preflight and return Baton to Human

No business/runtime source, tests, requirements, build script, README, historical V2/V2.1 evidence, accepted binary, or release metadata was modified.

---

Final state: **GITHUB_PUBLICATION_PREFLIGHT_READY_FOR_HUMAN_REVIEW**
