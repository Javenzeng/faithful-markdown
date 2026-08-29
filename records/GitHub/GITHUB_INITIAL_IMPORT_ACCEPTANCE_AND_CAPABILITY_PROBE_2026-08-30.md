# GitHub Initial Import Acceptance & Capability Probe — 2026-08-30

## Purpose

本记录关闭 `faithful-markdown` 的 GitHub Initial Import Gate，并记录首次可复现的 ChatGPT fresh-session GitHub Capability Probe。

本记录只涉及 governance / repository facts；未修改 runtime source，未运行新的 implementation tests，未打包，未创建 release。

## 1. Accepted Initial Import

Repository:

`Javenzeng/faithful-markdown`

Visibility:

`public`

Default branch:

`main`

Accepted initial-import anchor:

`fab1072af42f78b758b425a61ce2173df39a79fd`

Commit subject:

`Initial repository import: accepted V2.1 source baseline and pre-Git project records`

Readback verified:
- remote repository exists and is directly readable
- default branch is `main`
- initial public `main` HEAD matched the accepted root commit
- root commit has zero parents
- public V2.1 source baseline and governance are present
- `.gitattributes` contains `tests/fixtures/fidelity/*.bin -text`
- raw fidelity fixtures were imported without Git text normalization
- EXE is excluded from public Git history
- packaging / release remained unauthorized

Decision:

> **GitHub Initial Import: ACCEPTED / CLOSED**

From this accepted public push onward:
- GitHub = canonical source + durable governance + Git history.
- Drive Relay = `SESSION_STATE.md`, Baton / short-lived coordination, archival evidence mirror.
- public binaries belong in GitHub Releases rather than Git history.

## 2. Current-Session Capability Probe

Authenticated GitHub account:

`Javenzeng`

Target repository:

`Javenzeng/faithful-markdown`

Result:

`PASS`

Observed repository permissions included:
- admin
- maintain
- push
- pull
- triage

This proves the current Manager session can directly read the canonical repository and repository metadata.

## 3. Fresh-Session Reproduction

Human opened a separate new ChatGPT session and provided only a cold-start instruction:
- act as Manager / Reviewer
- do not use historical chat
- execute GitHub Capability Probe
- target `Javenzeng/faithful-markdown`
- read `AGENTS.md`, `PROJECT_STATE.md`, `MILESTONES.md`
- remain read-only

Fresh-session result supplied by Human:

`PASS`

The fresh session independently:
- identified authenticated account `Javenzeng`
- accessed the target repository
- identified default branch `main`
- recovered accepted baseline `V2.1`
- recovered Baton `HUMAN`
- recovered packaging `NOT_AUTHORIZED`
- detected that old durable governance still claimed GitHub initialization had not happened
- refused to silently upgrade that stale claim to Human acceptance
- stopped at a Human review gate without modifying files

## 4. Governance Decision

The project now treats GitHub connector availability as a probed capability:

> **GitHub access is a capability to verify, not an assumption.**

Manager / Reviewer cold start:
1. confirm authenticated GitHub account
2. access target repository
3. confirm default branch
4. read canonical governance from GitHub
5. only fall back to Drive Relay when Probe fails
6. never infer Windows real-machine facts from repository access

A successful Probe removes the old need for Human/Codex to manually relay canonical repository content into the Manager session.

## 5. Manager / Reviewer Role

Human authorized a thin Manager / Reviewer governance layer:

- Human: final authority
- Manager / Reviewer: canonical reader, Gate designer, evidence reviewer; no business-source edits by default
- Sol: architecture / implementation within approved Change Boundary
- Codex: local Git / Windows factual execution
- Drive Relay: short-lived coordination and `SESSION_STATE.md`

Default control chain:

`HUMAN -> MANAGER -> SOL -> MANAGER -> CODEX -> MANAGER -> HUMAN`

## 6. Next Gate

V2.1 remains the accepted source baseline.

Next milestone:

`V2.2 — Filesystem Save Integrity`

Current V2.2 state:

- Direction: `PENDING`
- Execution: `NOT_STARTED`
- source implementation authorization: `NOT_GRANTED`

Next Gate:

> **V2.2 Design / Evidence / Change Boundary Review**

No V2.2 source modification is authorized by this governance closeout.
