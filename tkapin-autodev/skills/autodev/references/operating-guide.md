# AutoDev operating guide

## Small durable record, not a second agent platform

Copilot executes agents and tools. This plugin supplies responsibilities and a
Python helper for work state, versioned artifacts, evidence, and an append-only
journal. Each project owns `.autodev/state.sqlite3`; keep it local and exclude it
from public source control because it can contain Client intent and feedback.
Do not edit the database directly or make private chat the only source of truth.

The helper never calls an LLM, launches workers, authenticates a person, or
deploys software. Its checks prevent accidental workflow drift through this
interface. An actor with arbitrary filesystem access can bypass it; host
permissions and genuine Client decisions remain essential.

## Calling the helper

Write a UTF-8 JSON request to a local file using the host's file tools, then run:

```text
python "<skill-root>/scripts/autodev.py" <action> --project "<target>" --input "<request.json>"
```

On Windows use backslashes. Keep request files out of deliverable snapshots;
after initialization `.autodev/requests/` is suitable. Calls emit JSON, except
`inspect` emits Markdown. Errors go to stderr with exit code 2. Inspect and fix
the stated cause; do not retry unchanged or fabricate the desired result.

All mutations require an actor:

```json
{
  "actor": {
    "id": "host-context-or-assignment-id",
    "role": "gm",
    "model": "gpt-6-astra"
  }
}
```

An identity is permanently tied to its role/model within the project. GM should
assign a stable tracking ID to each delegated context before dispatch and link
it to the native returned agent ID in recorded evidence. Do not infer a child
identity from inherited process environment variables. Use a genuinely separate
host context for a different role, not an invented persona. A specialist may
return its structured verdict for GM to relay with that source identity; do
not repeat verification merely to change an ID label after it was recorded.
For `client`, omit model and record evidence of the actual Client decision.
The trusted GM host may relay that decision; this does not make an agent the
Client. Context identity is a recorded assertion, not authentication.

Use `help` for required fields, roles, and optional fields. Add
`expected_revision` when a decision relies on a previously read state revision;
if another actor changed it, reload and reconcile before retrying.

## Short path through delivery

1. **Discover:** GM clarifies high-level intent; BA asks targeted questions in
   the same Client engagement. Architect and PM contribute constraints and an
   incremental plan. For a small ask, keep each artifact concise.
2. **Initialize:** `init` takes `intent`, `limits` containing positive
   `max_sprints`, `max_tasks`, `max_attempts`, and optionally explicit `models`.
   Propose limits proportionate to the request and include them in the initial
   Client package. They are not hidden unlimited defaults. The shipped model
   policy permits explicit non-Anthropic models only.
3. **Specify:** BA calls `artifact` with `kind: spec`; Architect uses
   `architecture`; PM uses `plan`. Each supplies `content`. Versions are
   immutable. Include examples, acceptance behavior, quality requirements,
   dependencies, integration responsibility, and unresolved decisions.
4. **Challenge:** Two independent Reviewer contexts using different permitted
   models call `challenge-package` with the exact `versions`, `passed`, and
   evidence. Both must pass, with no outstanding negative verdict. Preserve
   disagreements; an initial negative verdict requires resolution, not voting.
5. **Approve:** Present the named package and limits to the Client. Relay the
   actual decision through `approve` with `versions` and evidence. Version
   changes require renewed challenge and approval in v0.1. This conservative
   boundary is simpler than automatic materiality classification.
6. **Plan sprint:** GM calls `start-sprint` with the approved goal. PM uses
   `add-task` with title, project-relative write scopes (`paths`), and optional
   `depends_on` task IDs. Python requests use `/` or escaped `\\` in JSON paths.
   The helper rejects overlapping claimed/submitted scopes.
7. **Implement:** Developer calls `claim` with task ID and current assignment
   `revision`, edits only its scope, runs checks, then `submit`s with the
   returned revision, a list of all delivered and test `files`, and evidence.
   Submission captures SHA-256 hashes. Tool output, not intention, is evidence.
   Submission order is recorded transactionally. For serialized edits to the
   same file, integration uses the most recently submitted snapshot, not task
   creation order.
8. **Verify:** Separate Reviewer and Tester contexts inspect those exact files,
   run appropriate checks, and call `review` with task/revision, returned
   submission `digest`, `passed`, and evidence. Both roles must pass. Failure
   returns the item to ready; another claim increments revision and attempt.
9. **Integrate:** The independent Tester runs the complete increment, then uses
   `integrate` with sprint, `submission_digest` from `status`, passed, and
   evidence. GM can record `finish-sprint` success only after this passes.
   Failed/cancelled outcomes remain valid outcomes, not fabricated success.
10. **Learn:** Collect available role feedback, including GM's own handoff
    feedback, before commissioning the audit. Once feedback and the sprint
    outcome are recorded, read the current scope digest and dispatch the
    Auditor. Disclose unavailable supplemental feedback as a limitation rather
    than waiting indefinitely. GM dispositions every finding and authorizes
    the next increment or hands the exact verified result to the Client.
11. **Deliver:** Relay Client `accept` for the current sprint and integrated
    digest. Finish planned feedback and learning, record `finish-run`, then
    capture the current run digest and commission the run audit. `close` with
    handover evidence once required audits and dispositions are complete.

File snapshots in v0.1 cover regular files supplied by the assignment. There
is no deletion/rename manifest or sandbox-wide write tracking. Include every
changed file and test in the plan and evidence; use the project's normal Git
diff to detect omissions. Treat missing or unexpected changes as a blocker.

## Review, audits, and rework

Start with `status` for task revisions and digests, then `focus` for the assigned
task or sprint. Use full `context` when the omitted artifact contents, other
sprints, or past runs are needed. It includes all versioned artifacts and
improvements. `journal` returns up to 200 global events after an optional
`after` sequence number; page until exhausted.

`focus` takes exactly one existing `task` or `sprint` ID, plus optional `limit`
(1..200, default 20), `after` (event sequence, default 0), `feedback_after`
(offset in selected-sprint feedback, default 0), and `expected_revision`.
Unknown fields, invalid selectors, out-of-range cursors and invalid types are
errors. Example request:

```json
{"task": "task-3", "limit": 20}
```

The response is explicitly partial. It includes policy/limits, current package
versions and approval baseline, task attempts/revisions/submissions, transitive
dependency tasks, all selected-sprint audits/dispositions, integration, run
audits, scope digests, and active improvement contents. Artifact versions and
digests point to full `context` contents. Task focus names omitted task IDs.
It is not an audit-complete packet or permission to skip approved criteria.

Feedback pages contain all feedback for the selected sprint, including other
tasks and dependency feedback. Event pages deliberately contain all current-run
journal events through the returned revision, not just task-tagged events:
global authority decisions and cross-task failures must not disappear.
Current task reviews are not attempt history; read event pages for failures
that preceded reassignment or resubmission. No evidence strings are truncated.
Other runs remain available through full context and the global journal.

Each page reports `total`, `has_more`, and `next_after` or
`next_feedback_after`. Advance each cursor independently; when one stream
finishes, hold its cursor at the last event sequence or consumed feedback
count while paging the other. Nonzero cursors require the first page's
`expected_revision`. If state changes, restart from zero rather than mixing
pages. All pages retain full current selected work; paging bounds event and
feedback records, not total output bytes. Read-only calls do not record events.
CLI stdout and stderr use UTF-8, including when piped on Windows.

Every audit is against the `scope_digests` entry for its sprint or `run`. Required
examination categories are `journal`, `work`, and `verification`. An `audit`
records `examined`, `outstanding`, `limitations`, `findings`, and evidence.
Each finding has `id`, `summary`, `evidence`, and boolean `blocking`.
Complete means all three categories examined and no outstanding required
examination, not "a report exists." Missing supplemental feedback is a disclosed
limitation. A negative finding is not an incomplete audit.

Do not suppress late feedback to keep an audit current. Non-Auditor feedback
changes its scope and requires fresh examination; a bounded delta examination
may suffice if the Auditor establishes what changed. Auditor-only feedback
does not recursively invalidate its own audit. Ordering known feedback before
dispatch avoids preventable re-audits, not legitimate follow-up work.

GM uses `disposition` with scope, the originating audit ID, finding ID, `decision`
(`resolved`, `deferred`, `rejected`, or `scheduled`), and evidence-bearing
reason. All findings need dispositions; blockers need resolution before
continuation. Resolve defects with real work, not a change of wording.
Follow-up audits do not erase earlier finding obligations. Dispositions may
address an older audit; every recorded finding still needs a disposition and
every blocker must be resolved. An exception for incomplete examination cannot
waive these obligations.

An incomplete audit blocks the next sprint. Only the Client can grant
`audit-exception` naming the finished sprint, reason, exact next goal, and
recovery owner. It is one-use and leaves audit debt outstanding. It never
waives a known blocker or allows full closure with missing audits.

For stale or failed work use `reassign` with revision, reason, and a genuine
`reconciled: true` after the previous worker/effects are understood. Stop or
isolate previous writers before replacement mutation. For problems discovered
after finishing a sprint, `reopen` preserves history but clears effective
acceptance/integration and requires fresh verification. A materially changed
approved baseline requires finishing/cancelling the old increment and starting
a new authorized one. Do not silently rewrite active obligations.

`pause` prevents new dispatch through the helper. The host must actually stop
workers; a database flag does not kill processes. `resume` requires explicit
reconciliation. GM recovery uses one restored GM context with unchanged
authority; PM cannot promote itself. After full closure, `new-run` retains past
outcomes and active project learning.

## Self-inspection and self-evolution

Use `inspect`, relevant journal pages, feedback, and audits to find observed
friction. Prefer a small justified improvement over speculative framework work.
Possible improvements include role guidance, a work-summary Python tool,
context extraction, or better communication templates.

`propose-improvement` takes `scope` (`project` or `shared`), `kind` (`guidance`
or `tool`), `target` (internal role or simple `.py` filename), `content`, and
`benefit`. It records its author, content digest, and current project baseline.
It does not execute, install, or adopt the content.

An independent Reviewer or Tester uses `evaluate-improvement` with exact
candidate digest, passed, and observed evidence. For tools, first materialize
the candidate, inspect it, then run bounded tests in the target project.
For guidance, compare representative decisions before/after and check that
governing requirements remain intact. Do not call a synthetic example a live
delivery improvement. If evidence is weak, say so and do not claim benefit.

For a passing project-local candidate, GM calls `adopt-improvement` at an
assignment boundary. Future assignments retrieve active improvements from
context. `materialize` returns the exact immutable content-addressed path under
`.autodev/generated`; tools run from that path only within approved host
permissions. `revert-improvement` restores the previous active version after
reconciling affected work. No shared plugin file changes.

For a shared candidate, GM presents its scope, content, evidence, and impact to
the Client. Only a real Client decision can produce `approve-shared`.
`handoff-shared` then records eligibility for a separately authorized source
change, tests, and installation. It does not mutate the plugin. Do not bypass
this boundary with direct writes or treat initial installation consent as
approval of all future updates.

Project-local overrides cannot change permissions, model policy, Client
commitments, audit gates, acceptance authority, or governing principles.
No improvement automatically starts another improvement run. Keep pending
ideas in the backlog and protect delivery commitments.

Finished sprints' historical submitted items are not active assignments and
do not prevent safe later adoption or rollback. Actual unfinished assignments
still do. Older records without submission-order metadata remain readable; if
different overlapping hashes cannot be ordered, the helper reports a
`submission_blocker` and requires reassignment/resubmission and fresh
verification instead of guessing.

## Diagnosis, preflight, and communication

Before another repair of a failed criterion, record the exact diagnostic or
reproduction, a suspected mechanism grounded in code/environment evidence,
and the smallest check that distinguishes it from plausible alternatives.
Run that check before treating a repair as justified; preserve negative output
even if a later broad suite is green. If the mechanism is still unknown, use a
bounded diagnostic step or escalate, not a sequence of guessed patches.
Report both remaining helper claim attempts and any assignment-local repair
or command retry limit. Several command invocations can occur within one claim;
neither counter replaces the other. Reassignment requires reconciled workers
and effects and never resets the approved attempt ceiling.

Reuse preflight commands documented by the project and authorized by the
assignment, or independently evaluated/adopted project-local tools materialized
through the existing helper. These are guidance-only references: the helper
does not execute them, confer execution authority, or add a new preflight
schema. Proposed tools are not executable merely because they exist.
Name the command/tool digest, relevant environment identity, owned output
roots, expected source/lockfile effects, and artifact provenance checks in the
handoff. Do not copy credentials or private feed details into shared guidance.
Project-specific SDK/feed/native packaging remains project tooling.

Reuse the setup recipe, not an old pass. Rerun relevant freshness checks at the
verification boundary and after environment, source, lockfile or output changes.
Use before/after checks to expose drift and compare tested/published/installed
bytes where applicable. A preflight is not a substitute for independent
Reviewer/Tester checks or exact-submission/integration verification.

Keep feedback to the decision, observed friction, evidence references and next
owner; leave raw output in local evidence rather than repeating transcripts.
Do not truncate or discard failures. Client updates belong at useful milestones,
material exceptions or decisions, not every internal wait or status read.
Less text or fewer calls is not evidence of better delivery.
