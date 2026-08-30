# V2.7 Release Acceptance

- Human decision: V2.7 formally ACCEPTED
- Product: Faithful Markdown
- Scope: Windows App Identity
- Implementation / release-source commit: `5e1644d6a661c3a07f8c49787ae6fd1c1342402c`
- Changed implementation files: `app.py`, `assets/index.html`, `build_windows.ps1`, `tests/test_app_api_surface.py`
- Existing `assets/app.ico` reused unchanged
- Tests: 29/29 PASS
- Packaged Windows evidence: PASS
- EXE: `FaithfulMarkdown.exe`, 14665691 bytes
- SHA-256: `9846C856267D15EB350211BB1B0AE2640322430AE0E61640DAEDB8F0829D044E`
- Register: PASS
- No automatic default takeover: PASS
- Human-set `.md` default + file icon: PASS
- Unregister Guard while default: PASS
- Unregister after switching default away: PASS
- Release: [v2.7](https://github.com/Javenzeng/faithful-markdown/releases/tag/v2.7)
- Remote downloaded artifact hash verification: PASS
- Accepted source baseline remains V2.1 — Content Fidelity Contract
- Baton: HUMAN
- Blocker: None

Blocking fixes: Windows Shell association resolution is used for actual default-handler detection; the final resolved-path comparison bug was fixed before acceptance.
