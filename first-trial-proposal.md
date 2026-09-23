# First AutoDev trial proposal

Status: draft proposal for owner review. This document does not approve a
runtime, install dependencies, implement agents, or authorize execution.
The governing charter was separately accepted on 2026-09-21; trial choices and
budgets below remain proposals.

Current priority is the operating-model design in the project README. This
proposal is supporting material, not the next implementation step. Any eventual
trial must preserve C05's accountable General Manager: the parent coordinator
may fill that responsibility without adding a new worker agent. Record shared
coordination effort in both arms rather than treating it as invisible work.

This historical design proposal requires an evaluator-supplied sample project,
not another project from this repository. The completed Python delivery trials
are a separate exercise described in [VALIDATION.md](VALIDATION.md).

## Basis

### Existing approved principles

The [governing charter](principles.md) applies in full. In particular, use
explicit intent (C02), simplicity (C04), accountable management (C05), focused
contracts (C06), bounded autonomy (C07), and appropriate verification (C08-C11).
Preserve traceable records (C12), recovery (C14), mandatory audits (C16), and
controlled improvement (C17).

The former P6 collaboration policy remains separate: the parent coordinator
recommends work placement and obtains the Client's choice before new work
packages unless already selected.

### Source-backed findings from the research subagents

The three clean-context GPT-5.5 research subagents support these findings:

- Spec Kit-style artifacts are relevant for specification readiness,
  clarification markers, task plans, checklists, and verification notes.
- The inspected systems provide examples of durable state, external checks,
  visible incomplete states, and stop or retry behavior. Some Ralph variants
  bound total iterations; others and AutoResearch allow indefinite repetition.
  They do not collectively establish bounded execution as a universal practice.
- Agent organization evidence supports structured handoffs, focused contexts,
  and independent verification when they produce distinct artifacts or checks.
  It does not prove that a professional org chart should be copied directly.
- Simpler structured baselines can be competitive with complex agentic systems
  for localized coding tasks, so the first trial should compare against a
  cheaper baseline.
- Coding benchmarks and narrow optimization loops are not evidence of
  full-lifecycle product delivery.

### Proposed design choices, not yet approved facts

This trial proposal makes the following choices for owner review:

- Use an evaluator-supplied offline C# console sample as the target application.
- Exercise an existing-code enhancement with deterministic tests.
- Compare a single structured baseline against a smallest-useful specialized
  workflow.
- Use a deliberately ambiguous initial brief to test business analysis.
- Keep setup artifacts, owner clarification answers, and participant inputs
  separate to prevent evaluation leakage.

H1's execution mapping and H3's additional demo gate remain open. C08 defines
criteria responsibilities, while C07/C17 adopt the former R1/R4 governing
commitments. Their concrete procedures do not follow automatically from this
trial proposal.

## Recommended local application task

Target application: a small offline .NET console application using
`System.CommandLine`, supplied separately by the evaluator.

Recommended enhancement: add a `greet` command that prints a greeting with
predictable output and test coverage.

This target is intentionally small, local, credential-free, and deterministic.
It is large enough to exercise requirements clarification, CLI behavior,
implementation, review, tests, and rework without becoming a benchmark suite or
runtime-selection exercise.

This is a workflow-mechanics pilot, not a statistically meaningful benchmark or
evidence that one architecture scales better. A simple greeting task can expose
handoff and clarification failures but cannot validate the full professional
development lifecycle.

## Setup artifact: deliberately ambiguous initial brief

Do not give the clarified candidate specification below to the business analyst
or baseline participant. Their input should be only this brief plus the current
repository files they are allowed to inspect.

> Add a greeting command to the command-line sample. It should greet users by
> name, support quiet mode, and behave nicely when the name is missing. Keep it
> simple and add tests so we know it works.

Known ambiguities intentionally left in the brief:

- Whether `greet` should be a root command mode or a subcommand.
- Whether the name is an option, argument, or both.
- What "quiet mode" suppresses: all output, only diagnostic output, or the
  greeting itself.
- What "behave nicely" means for a missing name: default value, validation
  error, prompt, or usage text.
- What exact output format is acceptable.
- Which exit codes count as success or failure.

## Setup artifact: clarified candidate specification

This section is a proposed owner-answer script, not a hidden acceptance oracle.
It must not be included in the business analyst's initial participant input.
Candidate answers and numerical thresholds are proposals, not owner-approved
facts. Score clarification separately, then give both implementation arms the
same owner-approved specification. Never fail delivered software for violating
a candidate answer that was not communicated and approved.

### Candidate behavior

- Add a `greet` subcommand to the existing console application.
- Accept the person to greet through `--name <value>` or `-n <value>`.
- When `--name` is provided with a non-empty value, print exactly:
  `Hello, <name>!`
- Preserve the existing root command and `sub1` behavior unless the trial owner
  explicitly approves changing it.
- Treat a missing or whitespace-only name as a validation failure.
- For missing or whitespace-only name, exit nonzero and include the phrase
  `Name is required` in the user-visible output.
- `--quiet` on `greet` suppresses the greeting on successful execution but does
  not suppress validation errors.
- Successful `greet` execution exits with code `0`.

### Candidate deterministic acceptance evidence

- A test proves `greet --name Ada` exits `0` and prints exactly
  `Hello, Ada!`.
- A test proves `greet -n Ada --quiet` exits `0` and does not print the
  greeting.
- A test proves `greet` exits nonzero and includes `Name is required`.
- Tests cover whitespace-only names and validation failures with `--quiet`.
- A test proves the existing `sub1 --name Ada` behavior remains unchanged.
- The implementation builds without warnings introduced by the change.

### Candidate revision or failed-verification scenario

Include a separate, controlled recovery scenario, even if both initial
implementations pass. Use an evaluator-prepared faulty patch or fixture on an
isolated copy after the first-pass result is recorded, not a deliberately bad
instruction to one participant. Apply the same fault category and recovery
budget to each arm and report recovery separately from natural defects:

- If an implementation treats a missing name as `Hello, World!`, verification
  should fail because the clarified candidate behavior requires an explicit
  validation failure.
- If an implementation changes existing `sub1` output or exit code while adding
  `greet`, verification should fail as a regression.

The exact fault and method of applying it remain to be approved before execution.

## Smallest useful specialized workflow

The proposed workflow has three participant roles plus the owner. Role labels
describe responsibilities, not permanent architecture.

### Business analyst

Input:

- Ambiguous initial brief.
- Current relevant repository files.
- Applicable AutoDev principles, especially C02, C04, C06, and C08.
- Instruction not to implement.

Output artifact: `spec-readiness.md`.

Required contents:

- Restated user outcome.
- Ambiguities and assumptions.
- Clarifying questions.
- Candidate acceptance criteria, clearly marked as proposed.
- Readiness verdict: ready, ready with assumptions, or blocked.

Handoff to owner:

- Return the minimum questions needed to the parent coordinator, who presents
  them to the owner here and relays the answers. No participant contacts the
  owner in a delegated session.
- Do not see the hidden clarified candidate specification.

### Implementer

Input:

- Owner-approved specification produced after business analysis.
- Relevant repository files.
- Explicit non-goals and preserved behavior.
- Required acceptance evidence.

Output artifacts:

- Code changes.
- Test changes.
- `implementation-notes.md` summarizing changed files, assumptions followed,
  commands intended for validation, and any known gaps.

Handoff to verifier:

- Specification.
- Diff summary.
- Claimed acceptance evidence.
- Known risks or skipped checks.

### Verifier

Input:

- Owner-approved specification.
- Implementer handoff.
- Changed repository files.

Output artifact: `verification-report.md`.

Required contents:

- Commands run and exact outcomes.
- Acceptance criteria pass/fail table or compact list.
- Regression checks for preserved behavior.
- Any failed-verification scenario found.
- Verdict: accept, request rework, or blocked.

### Delivery and acceptance path

1. Business analyst converts the ambiguous brief into questions and proposed
   criteria.
2. Owner answers or accepts candidate assumptions.
3. Implementer receives only the approved spec and relevant files.
4. Verifier receives the approved spec, implementation handoff, and diff.
5. If verification fails, the implementer gets a rework handoff containing only
   failed criteria, observed evidence, and constraints.
6. Owner receives the final specification, diff summary, verification report,
   known limitations, and unresolved questions.

This tests a minimal version of H3's manager/review concern without adding a
separate manager role. A manager-first demonstration remains unapproved.

## Simpler structured baseline

Baseline participant: one agent/session with a structured prompt, no specialized
handoffs, and the same budget ceiling.

Baseline input:

- Ambiguous initial brief.
- Relevant repository files.
- Instruction to ask clarifying questions if needed.
- Requirement to produce code, tests, and a validation summary.

Baseline output:

- Code and test changes.
- A single delivery note with assumptions, validation commands, and evidence.

The baseline should be allowed to ask questions, because the comparison is not
"good process versus deliberately careless process." The tested difference is
whether specialized clean handoffs catch more issues or reduce ambiguity enough
to justify their cost.

The baseline's self-check is not independent verification. Before execution,
obtain an explicit C11 exception for this controlled comparison; do not treat
the experimental baseline as the default production verification policy.

## Evaluation plan

### Trial arms

- Arm A: single structured baseline.
- Arm B: smallest useful specialized workflow with business analyst,
  implementer, and verifier.

Both arms use the same ambiguous brief, starting commit, allowed repository
context, exact model/version and settings, tool permissions, owner-answer
policy, maximum elapsed time, and final acceptance criteria. After the
clarification phase, both receive the same owner-approved specification.
Record any unavoidable differences instead of claiming a controlled comparison.
If later delegation is authorized, use only explicitly selected non-Anthropic
models.

### Observable acceptance evidence

- Build command succeeds.
- Deterministic tests covering the candidate behavior pass.
- Existing `sub1` behavior is preserved.
- Missing-name behavior fails visibly rather than silently defaulting.
- The final delivery note distinguishes completed criteria, failed criteria,
  assumptions, and evidence.

### Quality measures

- Requirements quality: number of significant ambiguities surfaced before
  implementation.
- Delivery correctness: acceptance criteria passed on first verification.
- Regression safety: preserved behavior checked and unchanged.
- Handoff quality: verifier can reproduce claimed evidence without prior chat
  context.
- Rework quality: failed verification produces targeted correction rather than
  broad redesign.
- Simplicity: no unnecessary runtime, plugin host, external service, or broad
  architecture introduced.

### Accounting to capture

For each arm, record:

- Wall-clock time.
- Number of participant turns.
- Number of owner questions.
- Tool calls.
- Files changed.
- Tests added or changed.
- Build/test command outcomes.
- Approximate input, output, and cache tokens where available.
- Any budget overrun, stop, or escalation.

### Proposed budgets

These numbers are proposals for owner approval, not current policy:

- Maximum wall-clock time per arm: 45 minutes.
- Maximum implementation attempts per arm: 2.
- Maximum verification attempts per arm: 2.
- Maximum owner clarification questions before implementation: 5.
- Maximum total participant turns per arm: 8.
- Token budget target per arm: 60k input tokens and 12k output tokens, excluding
  tool result compression or unavailable accounting fields.
- Stop after the first unresolved dependency/tooling problem that is unrelated
  to the task and cannot be resolved with existing repository tooling.

Before execution, define how participant turns and attempts are counted across
roles and confirm that the caps permit clarification plus a full rework cycle.
The token target is observational unless exact accounting and enforcement are
available; do not claim an unenforceable hard cap or treat missing usage as zero.
Budget feasibility has not been validated.

### Failure and stop conditions

Stop and mark the arm incomplete if:

- The participant tries to use credentials, external services, or unrelated
  integrations.
- The participant changes the task scope instead of clarifying it.
- The participant weakens acceptance criteria to claim success.
- The participant cannot produce deterministic tests.
- The participant exceeds an approved, enforceable time, turn, attempt, or token
  limit. Separately report observed token-target overruns where no hard token
  cap is available.
- Verification finds the same failed criterion twice after rework.

Escalate through the parent coordinator to the owner if:

- The ambiguity affects product intent rather than implementation detail.
- Existing code behavior appears intentionally inconsistent with the candidate
  spec.
- Test tooling is absent or would require adding a new test project/package.

## Mandatory post-run feedback

Each finished trial arm is a delivery/workflow run and therefore requires the
Auditor retrospective specified in C16. Record what worked, gaps,
bottlenecks, recommendations, and the GM's response. Account for audit effort
separately from participant execution. Do not feed one arm's findings or
workflow changes into the other arm before the comparison is complete.
Audit-only activity does not trigger another mandatory audit.

## Leakage controls

- Store the ambiguous brief and clarified candidate specification in separate
  setup artifacts before execution. This combined proposal is for planning
  only and must not be exposed to participants.
- Give the business analyst and baseline only the ambiguous brief.
- Give the implementer only the owner-approved specification, not the hidden
  candidate specification.
- Give the verifier the owner-approved specification and implementation handoff.
- Evaluate final outcomes against the communicated owner-approved specification.
  Keep test implementations private if appropriate, but not product
  requirements. Use the owner-answer script to assess clarification coverage,
  not to impose undisclosed correctness criteria.
- Do not let an evaluator who knows the hidden candidate spec act as business
  analyst, baseline participant, implementer, or verifier in the same arm.

## Recommended next decision

Approve, revise, or reject this trial charter before any execution. The next
work package should finalize the exact trial charter and setup artifacts only;
it should still not implement or run the trial.
