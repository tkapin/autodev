# AutoDev v0.2.0 validation

## v0.2.0 source improvements, 2026-09-29

The source now adds opt-in `focus` reads and UTF-8 CLI output, with guidance for
pre-audit feedback ordering, mechanism-based repair diagnosis, and reuse of
authorized project preflight recipes. This section describes the independently
evaluated v0.2.0 source change. It is not a new live delivery trial.

Separate GPT-6 Astra Reviewer and GPT-5.4 Tester contexts assessed the exact
10-file implementation manifest, checking its SHA-256 hashes before and after.
Both returned PASS with no unresolved blockers. Independent unittest runs
reported 55 tests: 54 passed and the existing Windows symlink-privilege test
skipped. Junction rejection ran and passed. This documentation section was
added afterward and was not part of that implementation manifest.

Independent synthetic checks covered transitive dependencies, pagination and
retained failed attempts, invalid/stale cursors, interleaved writes, multiple
runs, active guidance, all audit findings/dispositions, Unicode output/errors
under redirected cp1252 settings, and unchanged database/source bytes on reads.
An unresolved finding from an earlier audit still blocked continuation after
a later empty audit. Late GM feedback still invalidated completed audits.

In one synthetic history, full context output was 61,019 bytes and the first
task-focus page was 31,637 bytes. Paging recovered all 58 current-run events
and 34 sprint feedback records exactly. Full artifact contents and past runs
remain available through context/global journal. This measures payload size,
not total retrieval cost, delivery speed, or model decision quality.

The Reviewer compared old/new guidance on synthetic stale-binary, lockfile
drift, AOT-overload, retained-handle race, and audit-order cases. New guidance
makes provenance checks, diagnostic steps and GM feedback timing more explicit;
several correct decisions were already required by the baseline. No native
PIM scenarios were rerun, and no time/cost or live productivity benefit is
claimed. The Tester's first large-inline-JSON probe exceeded Windows command
length; using the documented request-file interface resolved that harness issue.

PIM was not modified. The evaluated source was released as v0.2.0 in commit
`aabd395` and pushed to `origin/main`. The installer produced immutable content
hash `c2b41026c3afa77bedd73fc09f150a665c0ff157085b07a546bb2de4c9c3418a`.
The Copilot CLI registration reports enabled v0.2.0; the Agency Copilot engine
and personal `autodev` skill link point to that same immutable release.
The complete 55-test suite passed independently against both installed copies,
with only the existing Windows symlink-privilege skip. The installed helper's
`help` output advertises `focus`. Existing sessions were not restarted; open a
new session in another repository to load the release.

## Result

The local v0.1 plugin was implemented, installed, and exercised with the real
Copilot CLI and a fresh Copilot app session. Two disposable delivery projects
completed their delivery/audit/learning/closure cycle. This establishes a
working bounded PoC, not general effectiveness on large software projects.
Independent final code review then identified three edge-case defects. The
corrected 0.1.1 release was installed and its expanded regression suite passed
against the development source and both actual installed copies.

Tested environment: Windows, Python 3.14.6, Copilot CLI 1.0.87-0, and the
Copilot app available during implementation. The implementation targets
Python 3.11+ using only the
standard library; Linux/macOS execution has not been tested in this session.

## Offline checks

```powershell
python -m unittest discover -s .\tests -v
```

46 tests ran: 45 passed and one was skipped. The skipped file-symlink test
requires a Windows privilege that this account does not hold. A real Windows
directory-junction rejection test did run and pass.

Coverage includes:

- State/journal atomicity, including a forced journal-write failure and rollback.
- Append-only journal enforcement, restart, and retained run history.
- Exact package approval, two-model independent challenge, unresolved findings,
  explicit model policy, and stable context-role bindings.
- Concurrent/stale claims, conflicting write scopes, dependencies, bounded
  retries, and path traversal/metadata-path rejection.
- Independent task review/testing, combined integration, and stale file evidence.
- Pause, reconciliation, cancellation, and renewed Client authorization.
- Incomplete versus limited-coverage completed audits, specific Client
  exceptions, finding dispositions, late evidence, and non-recursive audit work.
- Acceptance versus closure, final audit obligations, and correction/reopening.
- Independent candidate evaluation, stale candidate/baseline rejection,
  project-local adoption/revert, immutable materialization, and shared approval.
- Cumulative audit findings across follow-ups, including incomplete-audit
  exceptions and run closure; safe learning after a failed historical
  submission; chronological overlapping edits and explicit legacy ambiguity.
- Manifest/skill/agent packaging, explicit model pins, and LF agent definitions.

Markdown was formatted and linted. Local documentation links and whitespace
were checked. App plugin metadata validation also passed.

## Independent final review

An isolated GPT-6 Astra code review reproduced three defects in the initial
implementation. They were not dismissed because the ordinary live flow passed:

1. A later empty/incomplete audit could hide an earlier unresolved blocker.
   Findings now remain obligations across audit versions, and GM can disposition
   their originating reports. Continuation/closure check all of them.
2. A submitted item in a finished failed sprint could indefinitely block later
   improvement adoption or rollback. Only unfinished assignments now impose
   that boundary; historical evidence stays intact.
3. Integration chose overlapping hashes by task creation order, not submission
   order. Submissions now record the transaction sequence, used consistently
   for the status digest and integrated snapshot.

Six regression tests cover these failures, control cases, and legacy-state
handling. Actor validation also rejects malformed role types and case/space
variants of Auto routing. Existing live receipts were rechecked with the
patched helper; the patch is not claimed as a third new live-model delivery.

## Live delivery and evolution

The opt-in runner is `tests/live_trial.py`. It uses a synthetic, narrowly
preapproved Client mandate for a disposable greeting CLI and invokes the real
installed-capable plugin, not a mocked model. No general Client approval is
inferred from this fixture.

Both completed projects demonstrated:

1. BA/Architect/PM artifacts, two-model package challenge, and version-bound
   approval before implementation.
2. Developer work followed by independent review, testing, and integrated
   verification of the exact submitted files.
3. Actual greeting behavior for default name, a named person, a name with an
   internal space, and rejection of blank/whitespace-only names.
4. Five passing project unittest cases, separately re-run by the outer harness.
5. Agent feedback, sprint audit, finding disposition, conditional fixture
   acceptance, final run audit, and recorded closure.
6. A project-local `work_summary.py` improvement, independently evaluated,
   adopted, materialized, and executed. The outer harness also checked empty
   and nonempty/paused/audit-debt/shared-proposal fixtures.
7. An unapproved shared-plugin proposal retained in the backlog. An attempted
   handoff was rejected; no installed/shared plugin content was changed.

Only GPT-6 Astra and GPT-5.4 appeared in the inspected live-trial model usage.
Recorded agent identities and relays are host assertions, not cryptographic
proof of identity. The successful tool evaluation demonstrates functional
correctness for the tested cases, not measured productivity improvement.

### What the first trial exposed

The first invocation could read the plugin but could not execute a helper
outside its target-project path grant. A narrow `--add-dir` grant corrected
that setup without granting all-filesystem access.

The trial then exposed unnecessary identity-label correction and premature
return after a subagent result. The operator clarified stable assignment
provenance, synchronous dependent calls, and bounded host continuations between
invocations. The same project resumed from its durable state and closed at
state revision 46; earlier failed/partial attempts were preserved.

A fresh second project subsequently completed in a single runner invocation,
without manual resumption, and closed at state revision 43. Its outer
verification again passed the five CLI checks, five project tests, two
summary-tool fixture sets, and shared-approval rejection.

Local receipts and transcripts are under `.trial-output/delivery-1` and
`.trial-output/delivery-2`. They are intentionally ignored by Git; private
session logs and credentials are not part of the release.

## Installation and app discovery

This project was subsequently exported to its standalone public repository
with fresh Git history. Runtime databases, private session logs, installed
caches, and other projects were not exported. Repository metadata and
documentation references changed; runtime behavior did not. The historical
fingerprints below describe the builds tested before that metadata change.

The installer registered immutable local releases through both native plugin
managers. The initial live-tested package content fingerprint was:

```text
ae232d51a85fbc11cf9c88b8ded7b2daf38b96676ac7489bb19be9ceb8e18c58
```

Python source line endings were normalized to LF to match published Git
attributes. Following the independent review fixes, the final immutable 0.1.1
source/app-skill release is:

```text
79cf17d3e37c6e37150279ee10bbcbb37065f11a029035b3e50d7f76d8ff8d2c
```

Standalone CLI discovery found the enabled `autodev` skill, and an actual GM
probe loaded the skill, read its guide, and found its helper.

The first app probe exposed all eight custom agents but not the plugin-bundled
skill. A personal-skill link to the same immutable release resolved this in a
fresh app session. That session successfully invoked the host's `autodev` skill,
read its installed guide, and executed the installed helper's `help` action.
It also received the packaged General Manager instructions under GPT-6 Astra.
The exact selected-agent identifier was not independently exposed in session
metadata, so the evidence is the active GM instructions and available agents,
not an invented metadata value.

Existing sessions retain their startup skill catalog. The installer now
creates the app compatibility link; users do not need to copy prompts or
manage two divergent skill sources.

A redundant native CLI reinstall and uninstall returned Windows access denied
while all 14 expected installed files remained intact. Identical-content
installation became a verified no-op. For the substantive reviewed update,
the explicit recovery option verified the owned registration, frozen source
fingerprint, and cached files, removed only that static cached copy using an
ordinary filesystem operation, and let the native manager rebuild it.
No ACLs, authentication, project data, or unrelated configuration were changed
by recovery. Both registrations now expose 0.1.1, and the complete suite was
also run against the CLI cache and the app's immutable linked release.

No marketplace publication occurred. The current CLI warns that direct local
plugin installation is deprecated for a future release; that future migration
is documented rather than treated as a current failure.

## Limits of the evidence

The tests do not prove unrestricted-shell isolation, authenticated human
approval, comprehensive historical filesystem/network absence, long-running
distributed recovery, or superiority over another development approach.
Snapshots cover supplied regular files, not every possible outside write.
Raw test output and Client decisions remain trusted host inputs.

The prepared GM decision packets are still a separate evaluation asset; these
live delivery trials are not claimed as a blind scoring run of that rubric.
Larger projects, model choices, and efficiency should be assessed through
further explicitly scoped use, with audit findings preserved.
