# V2.1 — Minimal Implementation Design & Change Boundary Review

Date: 2026-08-29  
Project: Markdown Reader & Editor  
Baseline: V2 accepted Windows build  
Milestone: V2.1 — Content Fidelity Contract  
Review status: APPROVED_WITH_AMENDMENTS / READY_FOR_IMPLEMENTATION_AUTHORIZATION  
Implementation authorization: NOT_GRANTED  
Baton: HUMAN

## 1. Review conclusion

V2.1 can be implemented without architecture expansion, without new runtime dependencies, without a new bridge API, and without changing the accepted `app.py` lifecycle / pywebview event flow.

Recommended runtime change surface:

- `core.py`: implement save invariants and authoritative file snapshot checks.
- `assets/index.html`: passively render file facts and enforce obvious read-only state from the existing document payload.
- `app.py`: no source change expected or approved in this boundary.
- Existing baseline tests remain; add a separate fidelity test suite and byte fixtures.

The implementation should preserve the current single-window product surface and existing `Open -> Review -> Fix -> Save -> Close` workflow.

### Human Design Review Decision

Human review result: **APPROVED_WITH_AMENDMENTS**.

The amendments below are authoritative for implementation and supersede any conflicting wording elsewhere in this document:

1. add one minimal persisted EOL fact, `eol_kind`, with allowed values only `NONE / LF / CRLF / CR / MIXED`; `line_ending` remains solely the file-level write-back policy;
2. fix the Normal Save decision order so read-only is checked only after content is proven changed and a disk write is required;
3. protect Save As targets with a local target snapshot rechecked before replacement, without adding long-lived fingerprint state for unrelated targets;
4. fix File Facts ownership: Python owns encoding/BOM/EOL/read-only facts, JS owns Clean/Modified;
5. require explicit tests proving `_safe_write` zero calls on No-op and temp cleanup on second-fingerprint conflict / `os.replace` failure.

All other design boundaries remain approved unchanged. Source implementation, test execution, build-script modification, packaging, and release are still **NOT AUTHORIZED**. Baton remains `HUMAN`.

## 2. Baseline review findings

### `core.py`

Current `DocumentStore` owns the correct filesystem responsibilities: current path, UTF-8 BOM policy, file-level EOL policy, load/save/save-as, and Markdown rendering base directory.

Current gaps relevant to V2.1:

- normal save always writes, even when editor content is unchanged;
- there is no authoritative fingerprint for the opened disk bytes;
- external modification is not checked before save;
- `_write()` uses `Path.write_bytes()`, which truncates the destination before the full write succeeds;
- obvious read-only state is not surfaced at open time;
- status payload contains BOM/EOL primitives but does not expose a complete, accurate V2.1 file-facts view.

### `app.py`

`EditorAPI` already maps `EditorError` to user-facing save/open failures and already resets Python-side dirty state only after successful open/save/save-as.

The Python-side `dirty` flag exists for the native close path. It must not become the authority for No-op Save or external-change correctness because it is asynchronously synchronized from JS.

No V2.1 behavior requires a new API method or a change to the pywebview startup / close lifecycle.

### `assets/index.html`

The UI currently keeps transient editor state in JS: path/name, `lastSavedContent`, dirty state, and preview render token.

The previous accepted startup fix established a critical invariant: generic UI refresh paths such as `updateChrome()` must not call back into the pywebview bridge while another bridge request is completing.

V2.1 file facts must therefore arrive in existing document responses (`initial_state`, `open_file`, `save`, `save_as`) and be rendered locally with no extra bridge request.

### Tests

The current suite covers UTF-8, BOM preservation, CRLF preservation, non-UTF-8 rejection, Save As extension, HTML escaping, harmful links, and relative images.

It does not yet prove No-op Save, external-change rejection, safe-write failure semantics, read-only upfront behavior, or the V2.1 byte-level fidelity corpus.

`tests/__pycache__/` is currently present in the canonical Drive tree and is repository pollution. It should be deleted as an allowed hygiene cleanup; no compatibility code should be added for it.

### Build and dependencies

Runtime dependencies remain only `pywebview` and `mistune`; build adds `pyinstaller`.

`build_windows.ps1` is not a test-only entrypoint: it creates `.venv`, installs dependencies, runs tests, then packages with PyInstaller into `dist/`. It remains protected in V2.1 and must not be invoked while packaging is unauthorized.

The known build-hygiene debt remains deferred to its separately authorized pass.

## 3. V2.1 state model and sources of truth

### Existing state retained

`DocumentStore`:
- `current_path`
- `had_utf8_bom`
- `line_ending`

JS:
- `lastSavedContent` / `dirty` for editor UX
- `renderToken` for preview ordering

Python `EditorAPI.dirty`:
- retained only for native close confirmation
- explicitly not used to decide whether saving is safe or necessary

### New stored state — two backend fingerprints plus one minimal EOL fact

1. `source_fingerprint: bytes | None`
   - SHA-256 digest of the exact raw disk bytes at the last accepted load or successful save.
   - Sole authoritative source for V2.1 external byte-change detection of the current document.
   - Never copied into JS.

2. `editor_fingerprint: bytes | None`
   - SHA-256 digest of the editor-canonical text at the same accepted snapshot.
   - Canonicalization only converts CRLF / CR to LF before hashing, matching the existing editor/write normalization boundary.
   - Used only for No-op Save detection.
   - Never copied into JS.

3. `eol_kind: str`
   - Allowed values are exactly: `NONE`, `LF`, `CRLF`, `CR`, `MIXED`.
   - Represents the actual observed EOL fact of the accepted file content.
   - `line_ending` remains separate and continues to mean only the file-level EOL policy used when an edited document is actually written.
   - This is a single minimal fact, not an EOL profile or preservation map.

### State explicitly forbidden

Do not add:
- mtime + size + hash parallel version state;
- JS copies of source/editor fingerprints;
- JS `externalConflict` or Python/JS conflict synchronization;
- background file-version state;
- watcher state, polling timers, daemon state;
- save generation counters;
- retry counters / watchdog flags;
- ACL / ADS / metadata snapshots;
- `EOLProfile`, per-line EOL maps, or another EOL abstraction layer;
- any additional EOL state beyond `line_ending` policy plus `eol_kind` fact;
- a second dirty authority for save correctness;
- Python `clean`, `modified`, or new `dirty` state used for save correctness.

### Fact ownership and derived, non-stored facts

Python authoritative file facts:
- encoding / UTF-8 BOM fact;
- EOL fact via `eol_kind`;
- `read_only`, computed from the current path when returning/opening a document and checked again only when an actual write is required. Use standard-library checks only; this is an obvious-read-only signal, not an ACL guarantee.

JS authoritative editor fact:
- Clean / Modified, derived from `editor.value !== lastSavedContent`.

Python must not add a new Clean / Modified / dirty authority for save correctness. Existing `EditorAPI.dirty` remains solely for native close confirmation.

## 4. Save invariants

### Normal save algorithm

The decision order is fixed and must not be reordered:

1. Require `current_path`; read the current target successfully. If the current target is missing or unreadable, fail closed.
2. Compute the current raw-byte SHA-256 and compare it with `source_fingerprint`. Any mismatch is an external-change conflict; do not write.
3. Canonicalize incoming editor content to LF and compute its editor fingerprint.
4. Compare it with the stored accepted `editor_fingerprint`.
5. If unchanged, return success as a No-op with **zero write-path calls**, even if the current file is read-only.
6. If changed, check obvious read-only / writability. Reject only now, because a disk write is actually required.
7. Encode content using the existing V2 BOM + `line_ending` file-level write-back policy.
8. Write encoded bytes to a uniquely named temporary file in the same directory.
9. Immediately before replacement, re-read the current target and perform the second raw-byte fingerprint check against the accepted `source_fingerprint`.
10. If the second check conflicts, remove the temp file and fail without touching the target.
11. Replace the destination with the temp file using standard-library `os.replace()`.
12. On success, update `source_fingerprint`, `editor_fingerprint`, and accepted EOL facts (`eol_kind`; `line_ending` remains the write policy) from the newly accepted content, then return the existing document response plus file facts.

### Save As algorithm

- If the selected resolved target equals `current_path`, it **must delegate to normal `save()`**. It must not use a separate overwrite policy or bypass current-document conflict checks.
- A different target path must not create or retain any long-lived target fingerprint/version state in `DocumentStore`.
- Before temp writing begins, capture a **local target snapshot** for that Save As operation only:
  - target absent => local `ABSENT` snapshot;
  - target present => local raw-byte fingerprint snapshot.
- After the same-directory temp write and immediately before `os.replace()`, re-check that local snapshot:
  - if an absent target was created, stop;
  - if an existing target was deleted, stop;
  - if an existing target's bytes changed, stop.
- On any such target-snapshot conflict, clean up the temp file and do not overwrite the changed target.
- The Save As snapshot is strictly a `_safe_write` / Save As local variable and must never become a field, cache, JS state, or cross-call version source.
- Different target paths otherwise retain the V2 Save As content policy: UTF-8 without BOM and LF file-level baseline for the newly accepted document.

### Failure semantics

- External byte change: fail, preserve external file bytes, keep editor contents and dirty state, show a clear message; no auto-reload, merge, or force-overwrite path.
- Read-only / not writable: unchanged content may still return a successful No-op. Reject only changed content that actually requires a write; do not silently fall back to another path.
- Temp write failure: fail; original target must remain untouched.
- Second fingerprint / Save As target-snapshot conflict after temp creation: fail; original/changed target remains untouched and temp must be cleaned.
- Replacement failure: fail; original target must remain untouched and temp must be cleaned; cleanup failure must be reported rather than silently ignored.
- Fingerprint read failure / missing current file: fail closed and do not recreate the original path as part of normal Save.
- No retry / timeout / backoff / watchdog.

## 5. Minimal design by approved V2.1 scope

### 5.1 No-op Save

**Existing files modified**
- `core.py`

**New files**
- test-only corpus / fidelity tests; no runtime file.

**New state**
- `editor_fingerprint` in `DocumentStore`.

**Forbidden state**
- no JS save fingerprint;
- no second dirty flag for save correctness.

**Source of truth**
- backend SHA-256 of editor-canonical content at the last accepted snapshot.

**Failure semantics**
- No-op is a successful Save response with zero disk write.
- External-change check still occurs first so the UI cannot claim a stale external file was "saved".

**Tests**
- `Open -> Save` on each fidelity fixture: SHA-256 unchanged.
- Patch / spy `_safe_write` and assert **0 calls** for No-op Save.
- Include mixed-EOL fixture where editor-canonical text is LF but source bytes remain mixed; no-op must remain byte-identical.
- Read-only + unchanged content: backend Save succeeds as No-op and `_safe_write` remains at 0 calls.

**Compatibility**
- Existing Save UI/message remains.
- New unsaved documents still invoke Save As.

### 5.2 External Change Guard

**Existing files modified**
- `core.py`

**New files**
- fidelity tests only.

**New state**
- `source_fingerprint` in `DocumentStore`.

**Forbidden state**
- no mtime/size/hash tuple;
- no watcher;
- no conflict state mirrored to JS.

**Source of truth**
- raw SHA-256 of the last accepted disk bytes.

**Failure semantics**
- mismatch => `EditorError`; target bytes remain untouched.
- missing/unreadable current target => fail closed; no silent recreation.

**Tests**
- load -> external byte modification -> save edited content => error and external bytes unchanged.
- same test with otherwise-clean editor content.
- Save As to same resolved current path must not bypass the guard.
- second fingerprint conflict after temp creation => changed/original target remains intact and temp is cleaned.

**Compatibility**
- detection is byte-based; metadata-only changes do not conflict.
- V2.1 does not create a merge/force-save UI.

### 5.3 Minimal Safe Save

**Existing files modified**
- `core.py`

**New files**
- fidelity tests only.

**New state**
- none beyond `source_fingerprint`, `editor_fingerprint`, and the minimal `eol_kind` fact; Save As target snapshots are local variables only.

**Forbidden state / mechanisms**
- no persistence manager/framework;
- no fsync durability protocol;
- no `ReplaceFileW` wrapper;
- no file-lock subsystem;
- no metadata/ACL copy layer.

**Source of truth**
- encoded bytes generated by the existing BOM/EOL policy plus the accepted raw fingerprint for pre-replace guard.

**Failure semantics**
- same-directory temp + `os.replace`;
- original survives temp-write / replace failures;
- cleanup failure is surfaced.

**Tests**
- successful small edit preserves UTF-8/BOM/file-level EOL guarantees.
- second fingerprint conflict after temp creation leaves the target intact and cleans the temp file.
- injected `os.replace` failure leaves original bytes intact, cleans the temp file, and never reports success.
- external modification between initial preflight and pre-replace verification is rejected in a deterministic mocked test if a minimal hook/test seam is available without adding runtime abstraction.

**Compatibility**
- no promise for ACL, ADS, timestamps, file identity, sync-drive semantics, or power-loss durability.

### 5.4 Read-only Upfront

**Existing files modified**
- `core.py`
- `assets/index.html`

**New files**
- fidelity tests only.

**New stored state**
- none; `read_only` is derived.

**Forbidden state**
- no permission watcher;
- no cached ACL model.

**Source of truth**
- standard-library filesystem facts at open/state time; on Windows include the obvious read-only attribute and a normal writability check.

**Failure semantics**
- obvious read-only document opens in read-only editor mode;
- backend normal Save is not a blanket failure: unchanged content succeeds as No-op; changed content is rejected when it reaches the read-only check;
- Save As remains available;
- permission changes after open are not watched; an actual required write still fails clearly.

**Tests**
- Windows-focused read-only fixture/test proves returned document fact and write rejection.
- cross-platform helper tests may mock the standard-library check rather than introducing platform libraries.

**Compatibility**
- no ACL fidelity guarantee.
- no background permission refresh.

### 5.5 File Facts

**Existing files modified**
- `core.py`
- `assets/index.html`

**New files**
- no runtime file.

**New stored state**
- `eol_kind` is the only additional file-fact state; no additional File Facts state is introduced.

**Forbidden state**
- no JS shadow copy of backend fingerprints or permission model;
- no Python Clean / Modified / new dirty authority for save correctness;
- no `EOLProfile` or per-line EOL map.

**Source of truth / ownership**
- Python authoritative: encoding / BOM / EOL (`eol_kind`) / read-only.
- JS authoritative: Clean / Modified.
- Existing `EditorAPI.dirty` remains solely for native close confirmation.
- File facts travel in the document payload already returned through existing bridge calls.

**Displayed facts**
- `UTF-8` / `UTF-8 BOM`
- `NONE` / `LF` / `CRLF` / `CR` / `MIXED` mapped from Python `eol_kind`
- existing Saved / Unsaved (Clean / Modified) indicator from JS only
- `Read Only` only when true

**Failure semantics**
- no extra bridge request to refresh facts.
- facts update only when a document is opened or a save/save-as succeeds.

**Tests**
- core payload assertions for BOM/EOL/read-only facts.
- no new JS test framework; thin UI mapping is reviewed manually / by code review in the implementation acceptance pass.

**Compatibility**
- current status bar remains small; no panel, toolbar, dialog, or feature UI is added.

### 5.6 Fidelity Test Corpus

**Existing files modified**
- preferably none in the accepted baseline suite `tests/test_core.py`.

**New files**
- `tests/test_fidelity.py`
- `tests/fixtures/fidelity/utf8_lf.md.bin`
- `tests/fixtures/fidelity/utf8_no_final_newline.md.bin`
- `tests/fixtures/fidelity/utf8_bom_crlf.md.bin`
- `tests/fixtures/fidelity/unicode_emoji.md.bin`
- `tests/fixtures/fidelity/mixed_eol.md.bin`

Using `.bin` fixture suffixes prevents text tooling / checkout normalization from silently rewriting the byte corpus. Tests copy them to temporary `.md` targets.

**New runtime state**
- none.

**Tests prove**
- no-op byte identity and `_safe_write` **0 calls**;
- BOM and file-level EOL regression safety plus correct `eol_kind`;
- final newline / no-final-newline behavior;
- Unicode and emoji bytes;
- mixed-EOL no-op byte identity only;
- external-change rejection;
- second fingerprint conflict after temp creation leaves target intact and temp cleaned;
- `os.replace` failure leaves target intact and temp cleaned;
- Save As local target-snapshot conflict protection for target created/deleted/modified during the operation;
- read-only upfront behavior, including unchanged read-only No-op success.

**Compatibility**
- existing `unittest` runner remains; no pytest or new test dependency.

## 6. CODE_CLEANLINESS_CONTRACT review

### Dependency Budget

Approved: standard library only (`hashlib`, `os`, `tempfile`, `stat` as needed).

Not approved: any new runtime or test dependency.

`requirements.txt` and `requirements-build.txt` stay unchanged.

### State Budget

Approved new stored runtime state is limited to:
- two private backend digests: `source_fingerprint`, `editor_fingerprint`;
- one minimal EOL fact: `eol_kind` with exactly `NONE / LF / CRLF / CR / MIXED`.

Existing `line_ending` remains solely the file-level EOL write-back policy and is not replaced by `eol_kind`.

No new persistent JS state is required. Read-only remains derived. External-change authority for the current document remains exactly one raw-byte fingerprint. Save As target snapshots are local variables only.

Explicitly forbidden: `EOLProfile`, per-line EOL maps, parallel mtime/size/hash state, Python Clean/Modified state, or any new dirty authority for save correctness.

### Abstraction Budget

Approved shape:
- small private helper functions/methods for canonical text hashing, raw file hashing, `eol_kind` detection, obvious read-only check, and safe temp replacement;
- keep `DocumentStore` as the owner;
- keep Save As target snapshot logic local to `_safe_write` / the Save As call.

Do not create `EOLProfile` or any new EOL abstraction layer.

Not approved:
- `SaveManager`, `FileVersionManager`, Strategy/Provider/Repository layers;
- new runtime module solely to hold one implementation.

### Error-handling Budget

Approved:
- explicit `EditorError` for conflict, read-only, and I/O failure;
- preserve original exceptions via chaining where useful.

Not approved:
- broad silent exception handling;
- retries, delay, timeout, watchdog, fallback save paths;
- pretending a failed cleanup/save succeeded.

### Repository Hygiene

- Delete `tests/__pycache__/`.
- Do not run `build_windows.ps1` during source/test-only authorization because it creates ephemeral build state and packages automatically.
- Build-hygiene redesign remains a separate debt item and protected scope.
- No temp files, generated `.spec`, build output, or test bytecode belong in canonical Drive content.

### Delete instead of add

Required deletion/replacement opportunities:

1. Remove the direct destination `Path.write_bytes()` truncation path from `_write()` and replace it with the single safe-write path.
2. Remove the semantic bypass where Save As to the same resolved current path uses a separate overwrite policy; delegate to normal Save.
3. Delete `tests/__pycache__/`.

No unrelated dead-code cleanup is approved in this milestone.

## 7. Bridge / dual-state safety rules

These are hard V2.1 invariants:

1. Add no new `window.pywebview.api.*` method.
2. `updateChrome()`, `applyDocument()`, and any new `applyFileFacts()` function must never call the bridge.
3. File facts are pushed only in responses to existing bridge requests.
4. JS must not store the raw disk fingerprint, editor fingerprint, permission snapshot, or external-conflict state.
5. Python owns encoding / BOM / EOL / read-only file facts; JS owns Clean / Modified.
6. Python `EditorAPI.dirty` remains limited to close confirmation; it is not consulted by `DocumentStore.save()` and no new Python dirty/clean state is added for save correctness.
7. No bridge call is introduced during `initial_state()` response handling.

Any implementation proposal that requires changing `app.py` or adding a bridge method automatically exits this approved boundary and returns to Human review.

## 8. Explicit V2.1 non-goals

Do not implement or research in this phase:

- full Filesystem Fidelity;
- ACL / DACL preservation;
- Alternate Data Streams;
- creation / modification timestamp fidelity;
- Windows file-attribute fidelity beyond obvious read-only detection;
- symlink / junction fidelity;
- deep `fsync` / directory flush / power-loss durability semantics;
- custom `ReplaceFileW` / transactional save framework;
- file locking / compare-and-swap kernel primitive research;
- mixed-EOL edited per-line byte preservation;
- watcher / daemon / polling service;
- diff / merge / conflict-resolution UI;
- force-overwrite UI;
- autosave;
- tabs, workspace/file tree, Git, AI, cloud, plugins, themes, export features;
- build-hygiene redesign;
- packaging or release work.

## 9. Expected code-change scale

Current approximate source sizes reviewed:
- `app.py`: 209 lines
- `core.py`: 137 lines
- `assets/index.html`: 285 lines
- `tests/test_core.py`: 72 lines

Expected V2.1 delta:

### Runtime
- `core.py`: approximately +55 to +80 lines added, with roughly 10–20 current writer / duplicate-path lines replaced or deleted; expected net +40 to +65.
- `assets/index.html`: approximately +15 to +25 lines net for passive file-fact rendering and read-only UI state.
- `app.py`: 0 lines expected.
- total runtime net growth target: roughly +55 to +90 lines.

If runtime net growth exceeds ~100 lines, if a new runtime module is proposed, or if `app.py` needs modification, stop and return to boundary review before continuing.

### Tests
- new `tests/test_fidelity.py`: approximately +140 to +190 lines.
- five small raw byte fixtures.
- existing `test_core.py` should remain intact if possible.

Test-code growth should therefore be materially larger than runtime growth.

### Dependencies
- new runtime dependencies: **0**.
- new test dependencies: **0**.

## 10. V2.1 Change Boundary

### Allowed files / paths for a future implementation Baton

Business/runtime:
- `core.py`
- `assets/index.html`

Tests:
- `tests/test_fidelity.py` — new
- `tests/fixtures/fidelity/*` — new corpus files
- `tests/__pycache__/` — delete only

Governance / evidence after actual work:
- `SESSION_STATE.md`
- `PROJECT_STATE.md` only when durable status changes
- `records/V2.1/*`

### Protected files / paths

No modification without a new Human boundary decision:
- `app.py`
- `tests/test_core.py` (accepted baseline regression suite; new V2.1 tests go elsewhere)
- `build_windows.ps1`
- `requirements.txt`
- `requirements-build.txt`
- `README.md`
- `AGENTS.md`
- `PROJECT_CHARTER.md`
- `MILESTONES.md`
- `records/V2/**`
- `releases/V2/accepted/**`
- all accepted binaries

### Approved implementation scope

Only:
1. No-op Save
2. raw-byte External Change Guard
3. same-directory temp + standard-library replace Minimal Safe Save
4. obvious Read-only Upfront
5. passive File Facts
6. Fidelity Test Corpus
7. deletion of canonical `tests/__pycache__/`

### Explicit non-goals

All items in section 8 are outside the boundary.

### Acceptance criteria

A future implementation is not ready for Human acceptance until it proves all of the following:

1. All pre-existing V2 unit tests still pass unchanged.
2. No-op Save preserves SHA-256 for all applicable corpus fixtures, including mixed EOL, and `_safe_write` is called **0 times**.
3. Read-only + unchanged content may return successful No-op; read-only rejects only changed content that actually requires a write.
4. Normal Save follows the fixed decision order in section 4 without moving the read-only check before No-op detection.
5. External byte changes observed at save preflight or the second pre-replace check are rejected and never silently overwritten.
6. Second fingerprint conflict after temp creation leaves the target intact and cleans the temp file.
7. `os.replace` failure leaves the target intact, cleans the temp file, and never reports success.
8. Save As to the same resolved current path delegates to normal Save.
9. Different-target Save As stores no long-lived target fingerprint state and uses only a local target snapshot; target create/delete/modify races before replace stop the overwrite and clean temp state.
10. UTF-8 / UTF-8 BOM and file-level EOL write policy do not regress.
11. `eol_kind` accurately reports only `NONE / LF / CRLF / CR / MIXED`; no EOL profile or per-line map exists.
12. Mixed-EOL guarantee remains exactly: No-op is byte-identical; edited per-line preservation is not claimed.
13. Python is authoritative for encoding / BOM / EOL / read-only; JS is authoritative for Clean / Modified; Python adds no new clean/modified/dirty save-correctness state.
14. Existing `EditorAPI.dirty` remains only for native close confirmation.
15. Obvious read-only files are read-only immediately in the editor; Save As remains available.
16. Status bar shows only verified compact facts; no functional panel/UI expansion.
17. No new bridge API or startup/UI bridge call exists.
18. No new runtime/test dependency exists.
19. No watcher, daemon, polling, retry, timeout, or fallback layer exists.
20. Canonical repo contains no `__pycache__`, temp-save residue, `.venv`, build/dist output, or generated `.spec` from this work.
21. Runtime net growth remains within the reviewed budget or is explicitly re-reviewed.
22. No packaging is performed until separately authorized.

### Known risks / honest boundaries

1. **TOCTOU residual:** two save-time fingerprint checks materially narrow the race window, but without locking or an OS compare-and-swap primitive there remains a tiny race between the final fingerprint check and `os.replace()`. Closing that gap belongs to V2.2/V2.4 research, not V2.1.
2. **Filesystem metadata:** `os.replace()` is chosen for content safety, not ACL/ADS/timestamp/file-identity fidelity. Those properties are explicitly not guaranteed in V2.1.
3. **Read-only detection:** upfront detection is intentionally limited to obvious standard-library-visible writability/read-only facts; it is not an ACL model.
4. **Sync/network filesystems:** semantics may differ from local NTFS and are not guaranteed in V2.1.
5. **Mixed EOL after edits:** existing file-level normalization behavior remains; only untouched no-op byte identity is guaranteed.
6. **Save As target race:** the local target snapshot narrows overwrite races for unrelated targets without creating long-lived state, but it does not claim kernel-level compare-and-swap semantics.

### Recommended implementation order

1. Reconfirm Human source implementation authorization and Baton == `SOL` before any source write.
2. Delete `tests/__pycache__/` and ensure future test execution does not persist bytecode in canonical Drive.
3. Add `tests/test_fidelity.py` and raw byte corpus first, including explicit assertions for No-op `_safe_write` 0 calls and temp cleanup failure paths.
4. Add `source_fingerprint`, `editor_fingerprint`, and minimal `eol_kind` detection/state in `core.py`; keep `line_ending` as the write-back policy.
5. Implement the fixed Normal Save decision order exactly as specified in section 4.
6. Replace direct destination write with same-directory temp + second fingerprint check + `os.replace()`, with deterministic cleanup on conflict/failure.
7. Implement Save As same-path delegation plus local target snapshot protection for different targets; add no long-lived target version state.
8. Add derived read-only and Python-owned file-fact payload in `core.py`.
9. Add passive `applyFileFacts()`-style UI mapping in `assets/index.html`; JS continues to own only Clean / Modified and no bridge call is added.
10. Run authorized unit tests directly (not `build_windows.ps1`), preferably with bytecode writing disabled or in an ephemeral local worktree/copy.
11. Review state count, runtime LOC delta, dependencies, temp residue, ownership rules, and protected-file diff.
12. Return to Human / Codex acceptance. Packaging remains a later explicit gate.

## 11. Current gate

Human Design Review result: **APPROVED_WITH_AMENDMENTS**.

Design status: **APPROVED_WITH_AMENDMENTS / READY_FOR_IMPLEMENTATION_AUTHORIZATION**.

This document remains a design/review artifact only. No business source was modified, no tests were run, and no package was built while recording these amendments.

Current execution state: `NOT_STARTED`.  
Source implementation authorization: `NOT_GRANTED`.  
Baton: `HUMAN`.

Next single action: **Human decides whether to explicitly grant V2.1 source implementation authorization and transfer Baton from HUMAN to SOL. Until both happen, implementation must not start.**
