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
10. **Learn:** Each agent writes `feedback` with sprint and a concise summary.
    GM commissions `audit`, dispositions every finding, and authorizes the next
    increment or hands the exact verified result to the Client.
11. **Deliver:** Relay Client `accept` for the current sprint and integrated
    digest. GM records `finish-run`, commissions the run audit, and `close`s
    with handover evidence once required audits and dispositions are complete.

File snapshots in v0.1 cover regular files supplied by the assignment. There
is no deletion/rename manifest or sandbox-wide write tracking. Include every
changed file and test in the plan and evidence; use the project's normal Git
diff to detect omissions. Treat missing or unexpected changes as a blocker.

## Review, audits, and rework

Read `status` for task revisions and digests. `context` additionally returns full
versioned artifacts and active improvement contents. `journal` returns up to
200 events after an optional `after` sequence number; page until exhausted.

Every audit is against the `scope_digests` entry for its sprint or `run`. Required
examination categories are `journal`, `work`, and `verification`. An `audit`
records `examined`, `outstanding`, `limitations`, `findings`, and evidence.
Each finding has `id`, `summary`, `evidence`, and boolean `blocking`.
Complete means all three categories examined and no outstanding required
examination, not "a report exists." Missing supplemental feedback is a disclosed
limitation. A negative finding is not an incomplete audit.

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
