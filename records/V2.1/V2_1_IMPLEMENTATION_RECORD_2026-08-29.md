# V2.1 Source Implementation Record — 2026-08-29

Project: Markdown Reader & Editor  
Milestone: V2.1 — Content Fidelity Contract  
Design: `APPROVED_WITH_AMENDMENTS / READY_FOR_IMPLEMENTATION_AUTHORIZATION`  
Human implementation authorization: `GRANTED`  
Implementation Baton: `SOL`  
Implementation result: `READY_FOR_HUMAN_REVIEW`  
Packaging: **NOT PERFORMED**

## 1. Scope executed

Implemented only the approved V2.1 Change Boundary:

- `core.py`
- `assets/index.html`
- new `tests/test_fidelity.py`
- new `tests/fixtures/fidelity/*`
- deleted canonical `tests/__pycache__/`
- governance/evidence updates under `PROJECT_STATE.md`, `SESSION_STATE.md`, and `records/V2.1/*`

No protected business/build/release file was modified.

## 2. Runtime implementation

### DocumentStore state budget

Existing state retained:
- `current_path`
- `had_utf8_bom`
- `line_ending`

New stored state is exactly:
- `source_fingerprint`
- `editor_fingerprint`
- `eol_kind`

`eol_kind` values produced by implementation are limited to `NONE / LF / CRLF / CR / MIXED`.

No mtime, size version, generation counter, watcher, polling state, ACL snapshot, EOL profile, per-line EOL map, or Python clean/modified correctness state was added.

### Normal Save

Implemented fixed decision order:
1. current target readable;
2. raw-byte SHA-256 external fingerprint check;
3. editor-canonical SHA-256 check;
4. unchanged => success / no `_safe_write`;
5. changed => obvious read-only check;
6. encode with existing BOM + `line_ending` policy;
7. same-directory temp write;
8. second raw-byte fingerprint check;
9. `os.replace`;
10. update fingerprints and EOL facts.

The old direct target `Path.write_bytes()` writer was removed. `core.py` now has zero `.write_bytes(` calls and one `os.replace(` call for persistence.

### Save As

- resolved target equal to current path delegates to normal `save()`;
- different target uses only a local `(exists, raw SHA-256)` snapshot;
- snapshot is rechecked after temp write and before replace;
- target creation/deletion/byte modification detected by the snapshot check blocks overwrite;
- no Save-As target fingerprint/version state is retained on `DocumentStore`.

### Read-only / File Facts

- read-only is derived on demand from standard-library-visible facts;
- unchanged read-only content succeeds as backend No-op;
- changed read-only content is rejected only when a write is required;
- Python payload is authoritative for `encoding`, BOM, `eol_kind`, and `read_only`;
- JS remains authoritative for Clean / Modified;
- `assets/index.html` only renders those facts and readonly UI state from existing API responses.

### Bridge safety

Baseline bridge API names: `initial_state`, `open_external`, `open_file`, `render`, `save`, `save_as`, `set_dirty`.  
Post-implementation bridge API names: identical.  
New bridge API count: **0**.

`app.py` was not modified.

## 3. Fidelity corpus and tests

New test file:
- `tests/test_fidelity.py` — 231 lines

New raw-byte fixtures (7):
- `utf8_lf.md.bin`
- `utf8_no_final_newline.md.bin`
- `utf8_bom_crlf.md.bin`
- `unicode_emoji.md.bin`
- `mixed_eol.md.bin`
- `cr_only.md.bin`
- `no_eol.md.bin`

Direct test command:

`PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v`

Result:
- existing V2 baseline tests: **8/8 PASS**
- new V2.1 fidelity tests: **13/13 PASS**
- total: **21/21 PASS**
- failures/errors: **0**

Raw test evidence:
- `records/V2.1/V2_1_UNIT_TEST_RESULT_2026-08-29.txt`

## 4. Fidelity acceptance mapping

| Acceptance item | Result | Evidence |
|---|---|---|
| No-op SHA-256 identical | PASS | corpus No-op tests |
| No-op `_safe_write` 0 calls | PASS | explicit mock assertion |
| mixed-EOL No-op byte-identical | PASS | mixed fixture test |
| external modification blocked | PASS | preflight conflict test |
| second fingerprint conflict preserves target + cleans temp | PASS | explicit race test |
| `os.replace` failure preserves target + cleans temp | PASS | injected failure test |
| Save As same-path guard | PASS | delegation + external conflict test |
| Save As target race | PASS | created / deleted / modified subcases |
| BOM / LF / CRLF regression | PASS | old tests + new modified-save tests |
| final / no-final newline | PASS | byte-identical corpus tests |
| Unicode / emoji | PASS | raw-byte fixture test |
| read-only upfront / No-op semantics | PASS | chmod-derived fact + changed-write rejection |
| File Facts / `eol_kind` | PASS | NONE/LF/CRLF/CR/MIXED assertions |

## 5. Code-change scale

### Runtime
- `core.py`: +98 / -14 lines; net **+84**
- `assets/index.html`: +17 / -1 lines; net **+16**
- total runtime net: **+100 lines**
- `app.py`: **0 lines changed**
- new runtime modules: **0**

The total runtime net is exactly the reviewed ~100-line re-review trigger. A cleanliness review was performed: the growth maps directly to the three approved state facts, two save fingerprints, one safe-write path, read-only/file-fact derivation, and passive UI mapping. No Manager/Strategy/Provider/Repository layer was introduced, so no boundary expansion was required.

### Tests
- `tests/test_fidelity.py`: **+231 lines**
- raw fixtures: **7 small files**
- `tests/test_core.py`: **0 lines changed**

Test-code growth is materially larger than runtime growth, as required by the design direction.

## 6. Dependency / abstraction / error-handling audit

- new runtime dependencies: **0**
- new test dependencies: **0**
- `requirements.txt`: unchanged
- `requirements-build.txt`: unchanged
- standard-library additions only: `hashlib`, `os`, `stat`, `tempfile`
- new runtime module: **0**
- new bridge API: **0**
- retry / timeout / watchdog / fallback writer: **0**
- SaveManager / FileVersionManager / Strategy / Provider / Repository abstractions: **0**
- old direct destination writer retained: **NO**

## 7. Protected-file / repository-hygiene verification

Drive readback after implementation shows these protected files retain their pre-implementation modification times:

- `app.py` — 2026-08-29T10:12:16.695Z
- `tests/test_core.py` — 2026-08-29T09:03:12.764Z
- `build_windows.ps1` — 2026-08-29T09:56:03.800Z
- `requirements.txt` — 2026-08-29T07:07:53.576Z
- `requirements-build.txt` — 2026-08-29T07:07:57.557Z
- `README.md` — 2026-08-29T07:52:05.878Z
- `AGENTS.md` — 2026-08-29T10:52:11.607Z
- `PROJECT_CHARTER.md` — 2026-08-29T10:52:16.445Z
- `MILESTONES.md` — 2026-08-29T10:52:20.901Z

No write action was issued against `records/V2/**` or `releases/V2/accepted/**`. The accepted V2 EXE remains 14,508,178 bytes with Drive modified time 2026-08-29T10:13:37.744Z.

Canonical `tests/` readback contains only `test_core.py`, `test_fidelity.py`, and `fixtures/`; `tests/__pycache__/` is absent. No build/package command was run and no `.venv`, build/dist output, generated `.spec`, or package artifact was created by this implementation.

Available local baseline SHA-256 facts used during audit:
- `app.py`: `B32778BBA7FC8FC519EEC45C45E94BE4671DA2B4DBFC9F4E5BFD6B048A41C3E7`
- `tests/test_core.py`: `AF1538F88E7A5CD59503F5BABC94420DDD8A82D0CC2617EE8D03C6C5C67B5417`
- `build_windows.ps1`: `5667F6C3D5A830F07AAB9C35FEC34B467C19DECFD7C3B2F0959F7D8D92D6474E`

## 8. Known remaining risks / honest boundaries

1. **Residual TOCTOU:** a small race remains between the second fingerprint check and `os.replace`; closing it requires locking / OS primitive research outside V2.1.
2. **Filesystem metadata:** `os.replace` does not claim ACL / ADS / timestamp / file-identity fidelity.
3. **Save As identical-byte delete/recreate:** the approved local snapshot is existence + raw-byte fingerprint; a target deleted and recreated with byte-identical content is not distinguishable without adding file-identity metadata, which is outside V2.1.
4. **Read-only model:** detection is intentionally obvious/standard-library-level, not a full Windows ACL model.
5. **Sync/network filesystems:** not guaranteed by V2.1.
6. **Mixed EOL after edits:** only No-op byte identity is guaranteed; edited mixed-EOL content continues to follow file-level `line_ending` policy.
7. **Windows facts remain unverified here:** unit tests were run in the current execution environment, not on the owner's Windows machine. Native read-only attributes, NTFS replacement behavior, pywebview UI behavior, and real GUI workflow still need Windows acceptance.
8. **Protected milestone status:** `MILESTONES.md` remains intentionally untouched and still contains its pre-implementation V2.1 Execution line. Current execution truth is the Human instruction plus `PROJECT_STATE.md` / `SESSION_STATE.md`; milestone-file alignment requires a separate Human authorization because it is protected.

## 9. Recommendation

**Recommend entering Codex Windows real-machine acceptance next, but do not package yet.**

Recommended Windows acceptance scope:
- run the existing direct unit-test suite without invoking `build_windows.ps1`;
- manually open LF / CRLF / BOM / mixed-EOL fixtures and verify status facts;
- verify read-only file opens non-editable and Save As remains available;
- verify No-op Save does not change file hash/timestamp-by-write behavior as observable;
- verify external modification blocks save with a clear error;
- verify normal edited save succeeds on Windows local NTFS;
- smoke-check startup/close flow for no bridge re-entry regression.

Packaging remains a separate Human gate.
