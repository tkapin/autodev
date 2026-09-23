# AutoDev workflow and coordination contract

## Draft status and terms

This is a design draft for AutoDev's initial default development workflow. It
inherits the accepted requirements from `principles.md` and `roles.md`: the Client
commissions work; the General Manager (GM) is the single business contact and
accountable internal lead; the GM manages all internal roles including the PM;
the GM delegates requirement detail to the BA and tactical planning to the PM;
the Client is not sent to Developer, Tester, or Reviewer sessions; the GM may
authorize BA clarification with the Client; specialists may communicate through
auditable shared records; and every finished delivery/workflow run, including
failure or cancellation, requires a retrospective Auditor review.

The Client accepted the shared-record triad as C12 (formerly P13): current work
state, an append-only journal, and versioned artifacts. It applies both to
developing AutoDev and to the software work it coordinates. The detailed
transition, routing, and recovery rules below remain proposals.

The Client's 2026-09-21 workflow draft adds targeted BA-led discovery, iterative
specification/architecture/planning, Client approval before implementation,
PM-led sprints, agent feedback, sprint audits, and a final improvement report.
The sections below capture that direction; unresolved execution policies are
not silently treated as approved.

Independent rubber-duck reviews by GPT-6 Astra, Claude Opus 5, and Grok 4.6
informed the proposed control rules below. These are design critiques, not
execution evidence. The Client specifically selected pause-by-default when a
sprint audit cannot finish, with a Client-authorized exception available.
Other proposed defaults still require adoption before autonomous execution.

The workflow below is proposed. The governing charter was accepted on
2026-09-21: C07 adopts bounded autonomy, C08 defines criteria responsibilities,
and C17 adopts controlled, reversible improvement. Their detailed mechanisms
and numeric limits remain open. This draft does not approve H3, any trial,
runtime, or storage format. In particular, a
manager-first demo is marked as proposed H3, not adopted policy. This document
also does not guarantee delivery quality by policy alone: quality claims require
accepted criteria, technical verification, and visible evidence.

Terms used here:

- An **engagement** or **project** is the Client-commissioned scope managed by
  the GM.
- A **delivery run** is one attempt to take a defined specification through
  delivery outcome, whether successful, failed, or cancelled.
- A **sprint** is a bounded delivery increment with an objective, planned work,
  evidence, and a recorded outcome. Its duration and resource limits are agreed,
  not assumed. A project can contain multiple sprints.
- A **work item** is an assignable unit of work with one active owner, inputs,
  outputs, and completion evidence. Unclaimed items have no active owner.
- A **role** is a responsibility contract; an **agent** is an execution instance
  acting under a role.
- An **artifact version** is a named version of a specification, design, plan,
  review, test result, or role definition.
- A **decision** is an auditable choice that affects scope, criteria, authority,
  design, assignment, or workflow.
- An **event** is an append-only record that something material happened.

Proposed boundary mapping: an engagement contains delivery runs, and a delivery
run can contain multiple sprints. Each authorized run records its objective,
scope, start, and completion conditions before execution. Finishing a sprint
does not itself finish the parent run. An agent session or retry is not a new
run. Failed or abandoned discovery is a finished workflow attempt and requires
an audit; it cannot disappear because no implementation was approved.
Separately commissioned improvement implementation is its own delivery run.
Rework normally stays within the current authorized run.

Technical verification means evidence that the delivered change behaves as
specified. Client acceptance means the Client accepts the deliverable against
their intent and authority. A finished delivery means the GM records a delivery
outcome, successful or not. Pending audit means the mandatory retrospective has
not yet completed; it must remain visible and cannot be treated as success by
fallback.

## GM operating loop

The initial workflow has two kinds of work: Client delivery and improvement of
AutoDev itself. Both use the lifecycle below. Self-improvement is a required
capability, not merely advice to revise prompts after a retrospective. The
mechanisms in this section are proposed defaults, not an approved runtime.

The GM starts or resumes from the current work state, applicable specification
and plan versions, outstanding decisions, verification evidence, and audit
obligations. It relies on the BA's business view, the Architect's technical
view, and the PM's delivery view, following evidence links where needed instead
of rereading every agent conversation. The GM needs a coherent system-level
understanding of scope, architecture, dependencies, and risks; it is not
expected to retain every technical detail or replace its specialists.

At intake, and whenever a result, blocker, change request, or Client decision
arrives, the GM applies this decision cycle:

1. **Understand the outcome.** Ask the BA to make the next useful increment
   precise, including business criteria and material unknowns. Engage the
   Architect on feasibility, technical obligations, and system impact, and the
   PM on dependencies and deliverable slices. Review specifications through the
   multi-model collegium below. Resolve decisions through the authorized party
   rather than asking the Client to manage implementation.
2. **Authorize bounded work.** Establish the scope, delivery boundary, available
   resources, permitted effects, stop conditions, and escalation triggers.
   Ask the PM for a practical plan and the Architect for design where needed.
   Assign only responsibilities useful to that increment.
3. **Let the team execute.** The PM routes work and specialists exchange
   auditable handoffs within the plan. The GM handles material exceptions and
   cross-cutting decisions, not every message or routine defect fix.
4. **Assess evidence and progress.** Continue useful work, route justified
   rework, narrow scope with authorization, or pause/stop. Repeated failures,
   exhausted limits, missing authority, or lack of meaningful progress require
   a recorded decision, not another automatic attempt at unchanged work.
5. **Deliver and learn.** Present the integrated result for Client acceptance,
   record the actual outcome, commission the mandatory audit when the run
   finishes, and disposition improvement findings.

A pause records why work cannot proceed, who owns the next decision, and what
would permit resumption. It is not a completed delivery or an excuse to keep
agents running. A finished run records its outcome even when unsuccessful.

The GM gives the Client concise updates at meaningful milestones, material
changes, and decision points, with any additional cadence agreed per engagement.
An update states the outcome sought, verified progress, remaining work,
material risks or blockers, and any decision needed with a recommendation.
Estimates and unverified claims remain distinguishable from observed results.
The BA, Architect, or PM can assemble the relevant information; the GM owns the
Client-facing answer.

### Autonomy and Client involvement

At intake, record how much involvement the Client wants during discovery,
whether autonomous refinement is authorized, and whether it wants a summary
after every sprint or only at agreed milestones and exceptions. Reporting
frequency and approval authority are separate settings.

In the Client's proposed full-auto mode, the GM can repeatedly commission BA,
Architect, PM, and advisor work without asking permission for each round.
It still obtains required business inputs and presents the resulting
specification, architecture, and plan for Client approval before implementation.
Full-auto does not silently waive that approval gate, invent material Client
preferences, grant new access, or authorize unlimited iterations.

Each refinement round identifies unresolved findings, expected outputs, and
what evidence would establish readiness. The GM continues while rounds make
useful progress within agreed limits. If findings persist, advice conflicts, or
limits are reached, it asks for a decision, proposes a narrower scope, or pauses.
The target is a sound, implementable baseline, not an unverifiable promise of
perfection.

### Readiness and refinement stopping rules

The GM can present a baseline for Client approval when named specification,
architecture, and plan versions are consistent; the next increment has clear
behavior, quality obligations, and observable acceptance evidence; interfaces
and dependencies are sufficiently understood; and integration responsibilities
and an operating envelope are defined. The required collegium review must cover
those versions, with all findings dispositioned and no remaining blocker.

A blocking finding identifies an unmet obligation or uncertainty that prevents
authorized implementation or reliable verification of the next increment.
Non-blocking findings may be deferred with a reason, impact, owner, and revisit
trigger. Dissent is not automatically a blocker, but voting or management
preference cannot dismiss evidence of an unmet obligation.

Readiness requires resolving existing blockers, not merely finding no new ones.
Each further round must address a named blocker or decision using new evidence
or a changed approach. Repeated findings without such progress require a GM
decision, authorized narrowing, or pause, not another identical review round.
Once readiness holds, present the package instead of soliciting endless polish.
Re-review focuses on changed content and affected dependencies; reopen settled
findings only when new evidence or changes invalidate their resolution.

The approval summary explicitly lists unresolved and excluded matters. For
each, distinguish a deliberate non-goal from an exclusion proposed because
refinement failed or reached its limits; explain the consequence and risk.
Such an exclusion requires the appropriate scope decision. Do not disguise
convergence-driven omissions as a complete understanding of Client intent.

When a required Client decision is outstanding, record the question, GM
recommendation, affected work, and resumption condition. Continue only
independent authorized work; silence is neither approval nor permission to
adopt the GM's preferred answer. Re-notification follows the agreed cadence,
not repeated polling or continued agent deliberation over the same question.

### Specification review collegium

Specifications are critical delivery inputs and require review by a collegium
of agents using different permitted models. This includes revised
specifications; review can focus on the changes and their affected assumptions
and dependencies. The BA, Architect, and PM are the primary supporting roles,
not a requirement for three permanent agents or a fixed three-model topology.
The GM may add focused advisors, such as a Tester for testability or a security
specialist for a relevant risk.

Proposed review procedure:

1. The BA prepares the versioned specification with the Architect and PM,
   including business intent, technical obligations, acceptance evidence,
   constraints, dependencies, assumptions, and unresolved questions.
2. Reviewers in separate contexts examine the same version and relevant
   evidence from business, architecture, and delivery perspectives. They
   produce initial findings before seeing each other's conclusions to reduce
   anchoring. Record the actual model and artifact versions; author self-review
   does not substitute for independent challenge.
3. The BA consolidates business findings, the Architect addresses technical
   findings, and the PM addresses delivery implications. Preserve disagreements
   and evidence, not just a merged consensus. Revised artifacts link to the
   findings they address and receive appropriate re-review.
4. The GM records a readiness decision based on evidence and resolves conflicts
   through the appropriate authority. Material unknowns that block the next
   increment must be resolved or explicitly excluded through an authorized
   scope decision. Client business decisions still go to the Client; a majority
   vote cannot establish correctness or waive an unmet obligation.

Review depth is proportionate to risk and change size. The panel composition,
model selection, and review limits remain policy decisions; only authorized
models may be used. If the required diversity or review cannot be provided,
record the blocker and seek a policy decision rather than silently treating
single-model review as equivalent. Model diversity broadens challenge but
does not prove correctness or replace implementation review and testing.

## Default lifecycle

These are responsibilities and decision points, not a requirement to launch
every role for every task or run them in a strictly sequential chain. Within its
authority, the GM records a proportionate plan: related analysis can be
combined, independent work can proceed concurrently, and unnecessary artifacts
need not be invented. This does not waive required verification, Client
acceptance authority, or the mandatory run-level audit.

### 1. GM intake and high-level alignment

The Client gives the GM an outcome, constraint, defect, or change request. The
GM records the engagement, initial intent, constraints, known authority, and any
obvious non-goals. The GM decides whether the request is ready for BA analysis
or must be rejected as outside authority. The output is an initial engagement
record and one or more draft work items for analysis, not an implementation
order. The GM first clarifies the high-level problem, desired value, constraints,
and engagement preferences with the Client. Detailed discovery then goes to the
BA rather than turning the GM into the requirements interviewer.

### 2. BA-led discovery and input specification

The GM tasks the BA to identify ambiguity, missing requirements, assumptions,
risks, and proposed acceptance evidence. The BA may prepare questions for the GM
to ask the Client, or the GM may authorize a bounded BA conversation in the same
engagement. The Architect contributes feasibility, system constraints, and
quality requirements during discovery; the PM checks dependencies and useful
delivery slices. The BA records answers and unresolved issues. After collegium
review, the GM decides whether the specification is ready enough to proceed,
needs more Client input, or should be narrowed.

For this workflow, the GM explicitly tasks the BA to work with the Client on
the details in the same engagement. The BA specializes in asking useful,
targeted questions: actual usage, examples, corner cases, failure behavior,
priorities, and constraints. It uses existing answers and progressively asks
about material gaps instead of administering an exhaustive questionnaire.
The output is an input specification that distinguishes confirmed needs,
assumptions, non-goals, and unresolved decisions.

Readiness does not require a frozen waterfall. It requires enough accepted
intent, constraints, and evidence expectations to avoid turning material
unknowns into silent implementation choices. Later changes go through an
explicit change decision that records the revised specification version and
affected work items.

### 3. Iterative specification, architecture, and planning

The GM tasks the Architect, and where useful the BA, to propose the simplest
adequate solution. The Architect records interfaces, constraints, tradeoffs,
risks, and technical assumptions. The GM uses this evidence to decide whether
design is sufficient for planning or whether more analysis is needed. The output
is a design artifact version linked to the specification version it satisfies.
Discovery and design can iterate together. If design changes a requirement or
invalidates an assumption, revise the specification and return the affected
scope to collegium review before treating it as implementation-ready.

The BA, Architect, and PM iterate together under the GM. The BA maintains
business meaning and acceptance criteria, the Architect owns technical
coherence, and the PM checks decomposition, dependencies, and incremental
delivery. The GM returns specific findings for revision and may use additional
rubber-duck advisors to challenge the combined proposal. The specification
collegium remains required; extra advice is not a substitute for its review.

Specifications are the durable source of product intent, not disposable
preparation for code. The intended standard is that another team can recreate
the specified system from the versioned specification package and its declared
dependencies, without relying on the original conversations or undocumented
knowledge in the existing implementation. This means equivalent required
behavior and constraints, not identical generated source code.

The package includes relevant behavior, examples and corner cases, interfaces,
data rules, quality attributes, acceptance evidence, architecture decisions,
and environment/dependency requirements. It records required external assets
and how they are obtained, not secrets. Reviewers identify facts that remain
available only in conversations or code and route them back into the package.
Recreation is a design goal until demonstrated; a clean-context reconstruction
exercise is a candidate validation method, not something already performed.

Preserve incremental learning: describe the overall system and milestones,
detail the next sprint sufficiently for execution, and make later uncertainty
visible. Before implementing newly discovered behavior, update the affected
specifications and obtain the required decision. Do not manufacture exhaustive
upfront detail for requirements the Client has not yet decided.

### 4. Project plan and Client approval

The GM tasks the PM to produce a practical plan: work items, dependencies,
owners or required roles, expected outputs, acceptance evidence, and known
blockers. The plan identifies the main project parts, milestones, sprint goals,
incremental Client value, integration responsibilities, and PM-to-GM reporting
cadence. The PM coordinates tactical sequencing under the GM's authority.

The GM assembles a coherent summary of the specification, architecture, and
plan, including material tradeoffs, assumptions, risks, and deferred questions.
The Client approves the named artifact versions, requests revisions, or declines.
PM-led implementation begins only after that approval and within the agreed
authority and resources. Approval of the plan is neither acceptance of future
software nor authorization for deployment.

The approval record also names the delegated refinement envelope and milestone
acceptance points. Client update cadence does not determine acceptance points.
Proposed default: on multi-sprint work, include an early useful Client feedback
or acceptance milestone rather than discovering product misalignment only at
final delivery. The Client chooses these checkpoints in the plan.

Individual technical handoffs inside the approved plan need not return to the
GM unless they change scope, criteria, authority, or risk materially. Changes
beyond delegated authority return through the GM to the Client.

#### Change authority within the approved plan

The following is the proposed refinement envelope to include in approval:

- The PM sequences and assigns work, routes defect correction, and coordinates
  safe parallel execution within the sprint goal and delegated resources. It
  cannot change that goal, waive verification, or add unapproved behavior.
- The BA develops business requirements and records authorized Client answers.
  The Architect develops technical detail and engineering obligations. Neither
  independently changes Client commitments or accepts delivery.
- The GM can authorize technical elaboration and internal replanning that
  preserve approved behavior, acceptance criteria, quality obligations,
  constraints, delivery boundary, and resource/access limits. It records the
  rationale and affected artifact versions and reports material decisions.
- New, removed, or weakened business behavior or criteria, changed commitments,
  expanded permissions, and changes outside the approved envelope require the
  appropriate Client decision before affected work proceeds. Governing
  principles and acceptance authority cannot be changed as internal tuning.

An unmet existing criterion is a defect, not a reason to weaken that criterion.
Classify a clarification by its effect, not its label: if it introduces a
previously undecided material business choice, obtain Client authorization.
When the BA and Architect disagree on classification, the GM records the
evidence and rationale; ambiguous authority goes to the Client. Unaffected
authorized work can continue.

New versions inside the approved envelope retain a traceable relationship to
the original approval; they do not require repetitive whole-package approval.
Outside-envelope changes require approval of the revised affected scope.
In either case, identify invalidated evidence and reissue affected assignments
before treating the new version as executable.

### 5. PM-led sprint execution

The GM authorizes the sprint objective and plan; the PM drives execution and
spawns or assigns Developers, Reviewers, Testers, and other justified agents
within delegated authority. All roles still report to the GM; tactical
assignment by the PM does not create a second overall delivery authority.
A Developer claims a work item only when it has the required inputs or records
a blocker.
The Developer produces code changes, implementation notes, tests where
appropriate, and evidence links. If the Developer discovers missing requirements
or design conflicts, the work item returns to clarification, design, or planning
through a recorded blocker or change request rather than silent invention.

The PM can run independent work in parallel when dependencies, resource limits,
workspace isolation or serialized writes, and integration ownership are clear.
Parallel task completion is not proof that the integrated increment works.
The PM optimizes delivery speed without reducing quality or verification.
It reports progress, evidence, blockers, remaining work, and forecast changes to
the GM at the agreed cadence and promptly escalates material exceptions.

The sprint plan names an integration owner and an integrated-verification
assignment with a designated verifier, exact combined artifact version, and
required evidence. Existing roles perform these responsibilities. A sprint
cannot be recorded as technically successful until integrated verification
passes; individually verified items do not satisfy this gate.

### 6. Independent review and test

Reviewer and Tester assess the implementation against the agreed criteria,
rather than accepting the implementer's self-assessment. Where an independent
agent/context is used, record that fact; one instance changing personas is not
evidence of independent review. The exact execution separation remains a design
choice under H1, subject to C11's default separate verification context for
software changes and explicit proportionate exceptions. The Reviewer checks
correctness, maintainability, specification
alignment, and agreed standards. The Tester verifies observable behavior and
failure paths against the accepted criteria. Findings are actionable records
with evidence. Passing review or test is technical verification evidence, not
Client acceptance.

Reviewers also identify behavior or verification expectations supported only by
conversation or undocumented code. Route these specification gaps to the BA
and Architect for authorized resolution and affected re-review. A checklist
review improves specification completeness but does not demonstrate that a
system has actually been reconstructed from its specification.

Failed review or test sends work back to the relevant owner through PM
coordination. The GM is informed when failure affects scope, commitment,
criteria, or repeated progress, but the GM does not need to approve every
defect-fix handoff that stays within the approved plan.

### 7. Sprint audit, GM adjustment, and continuation

At the end of their assignments, agents leave concise process feedback as
defined below. The Auditor combines those reports with work records, handoffs,
and verification evidence at every finished sprint, including failed or
cancelled sprints. Findings cover successful practices, bottlenecks, tooling,
roles, coordination, and improvement opportunities, and go to the GM.

The GM consults the PM and relevant specialists, records a disposition for each
finding, and decides whether to adjust the workflow, commission a controlled
agent/tool change, defer work to the improvement backlog, or seek Client input.
It then records go, replan, pause, or stop for the next sprint. This is a GM
decision, not an automatic Client approval request after every sprint.
Immediate changes still require appropriate evaluation and versioning.

If the Client requested sprint updates, the GM presents delivered and verified
value, outstanding work or limitations, main improvement findings, actions
taken or deferred, and the next sprint's goal. It may delegate preparation but
owns the report. Notification does not imply Client acceptance.

Client-selected policy: if the sprint audit cannot finish, pause before starting
the next sprint. The GM may reassign the Auditor and arrange bounded recovery
of missing evidence within existing authority. It cannot waive the audit gate.
Only the Client can authorize a specific provisional-continuation exception.
Record its permitted scope, reason, risks, expiry or stopping condition, and
audit recovery owner. The obligation remains outstanding and no exception
authorizes unmet product criteria or otherwise prohibited actions.

Distinguish an audit not started, an incomplete audit with coverage gaps, and a
completed audit with adverse findings. Negative findings are not an Auditor
failure: disposition them and resolve blockers before continuation. Partial
findings can be acted on without claiming the full audit is complete.

#### Auditor completion handoff

Commission an audit against a named scope and completion policy. Specify the
required examination, mandatory evidence, and permitted alternative evidence,
distinguishing these from supplemental sources such as agent feedback.
The Auditor's handoff records:

- Audit identity, commissioned scope/policy versions, covered sprint/run, and
  the artifact and evidence versions examined.
- Completion assessment: not started, incomplete, or complete, with a rationale
  against the commissioned requirements rather than merely a report timestamp.
- Required examination performed and its evidence; any unfinished examination
  or unmet evidence requirement, with the recovery owner and next action.
- Source coverage limitations, their effect on conclusions, and any permitted
  alternative evidence used.
- Findings and recommendations, separately from examination still outstanding.

A completed examination can report missing supplemental feedback or adverse
findings. Neither automatically makes the audit incomplete. Completion requires
that the commissioned examination and evidence requirements are satisfied;
missing mandatory evidence without a permitted alternative means incomplete.
An unresolved corrective action is not necessarily an unfinished examination,
but a delivery or authority blocker still prevents affected work.

The GM checks that the handoff covers the commissioned scope and current
versions and that the completion assessment is supported. It must not infer
completion from the existence of a report, demand zero missing feedback where
policy does not require it, or override an incomplete assessment to bypass the
sprint gate. Ask the Auditor to clarify or correct an inconsistent assessment.
If the policy does not settle a material evidence gap, obtain the appropriate
policy decision; until resolved, the required audit remains pending. Neither
actor may silently narrow commissioned scope or weaken completion requirements.
The existing Client-only continuation exception remains unchanged.

### 8. Integrated demo and Client acceptance

Present the exact verified delivery version and its product artifacts for
acceptance. Unmet agreed criteria require correction or an explicit Client
decision to revise the obligation; do not present a known failure as compliant.
A pending process audit alone need not prevent presenting verified software,
but it remains disclosed and still blocks the next sprint under the policy
above unless the Client grants an exception.

When verification evidence is sufficient, the GM assembles an integrated
delivery package: what changed, how it satisfies the specification, evidence,
limitations, known risks, and open issues. A manager-first internal demo before
Client presentation is proposed H3. Under that proposed gate, the GM reviews the
integrated package first and either sends it back for rework or presents it to
the Client. This gate should be adopted only if it improves readiness and
evidence rather than adding ceremony.

The Client accepts, rejects, or requests changes. Rejection returns to the
appropriate lifecycle stage. Requested changes are not automatically defects:
the GM records whether they are clarification of existing criteria, correction
of unmet criteria, or a scope change requiring a new decision.

### 9. Final audit, improvement report, and handover

After the delivery run is finished, successful, failed, or cancelled, the GM
commissions the Auditor. The Auditor examines the run records, identifies what
worked, gaps, bottlenecks, and recommended improvements, and returns findings to
the GM. Audit work does not recursively require another mandatory audit. The GM
records disposition of each finding: adopt, defer, reject with reason, or create
improvement work. If the audit cannot finish, the audit obligation remains
pending visibly; it is not converted into a successful retrospective.

Record verification, Client acceptance, run outcome, release authorization, and
audit/handover completion separately. Acceptance precedes the post-run
retrospective and does not imply full administrative closure. If authorized
rework continues after rejection, the run remains active; otherwise record its
unsuccessful outcome and commission the audit.

The GM consults the Auditor again at project closure to consolidate sprint
findings, recurring patterns, the effectiveness of adopted changes, and
remaining opportunities. It delivers the final specifications, architecture,
plan/outcomes, code and other artifacts, verification and handover evidence,
and a process/tooling/agent improvement report to the Client. Separate changes
actually adopted from unimplemented recommendations. Closing the project does
not require implementing every improvement.

If the final audit exposes incorrect evidence or a product defect, preserve the
historical acceptance record, notify the Client with corrected facts and a
recommended remedy, and reopen affected evidence and work through the change
process. Do not silently erase acceptance or conceal the finding.
Full closure requires disposition of mandatory audits and completion of agreed
handover obligations; listing an outstanding audit is disclosure, not closure.
Record packaging, installation, migration, support, and recovery responsibilities
where applicable. Release or external publication requires separate authority.

Sprint reviews supplement C16's finished-run audits under the proposed
engagement/run/sprint mapping above. One report can cover coincident sprint,
run, and project boundaries if it explicitly covers each scope. A project-wide
report can reuse earlier evidence but must still assess the overall engagement.
Audit-only work does not trigger recursive audits.

## Agent feedback for the Auditor

Every agent, including the GM and PM, leaves a short feedback record when its
assignment ends, including failure or cancellation where it can still report.
This is evidence for an audit, not a separate mandatory audit of each agent.
An Auditor's own handoff does not recursively commission another Auditor.

The feedback identifies the assignment and artifact versions, outcome, what
worked, friction or bottlenecks, supporting examples, and suggested changes
with expected benefit. Agents may comment on other agents' work only when
exposed to it, distinguishing observations from hypotheses and stating context
limitations. No forced criticism or invented improvement is needed.

Feedback is attributable and retained alongside delivery evidence. It does not
replace tests or objective records. The Auditor cross-checks claims, preserves
disagreements, and records missing feedback as a coverage gap rather than
treating silence as positive evidence. Interrupted agents may be unable to
submit feedback; existing records remain usable without fabricating their view.

Agents write their own observations before reading peer feedback where feasible;
record prior exposure rather than claiming independence that did not exist.
Multiple accounts of the same event are not independent corroboration. The
Auditor distinguishes observed facts, causal hypotheses, and demonstrated
improvements, investigating contradictory evidence instead of counting votes.
Recommendations that enlarge authority or weaken checks require independently
supported evidence and appropriate approval, not self-report alone.
Findings about the GM and its dispositions remain visible in the Client's
closure report, including findings the GM disputed or deferred.

## Self-improvement through the delivery workflow

The GM can commission changes to AutoDev's prompts, role definitions, workflows,
coordination tools, and supporting infrastructure within granted authority.
Examples include better work tracking, agent communication, GM-to-Client
summaries, and extraction of useful information from session records. Access to
those records must respect privacy, retention rules, and existing permissions.

The initial foundation must support observation, a durable improvement backlog,
implementation of changes, evaluation, versioned adoption, and recovery. It need
not start with sophisticated dashboards, analytics, or a message bus. AutoDev
can develop better tools using that foundation.

The Client's v0.1 authority decision permits independently evaluated, reversible
project-local changes to be adopted automatically. Shared-plugin changes need
Client approval; they are proposed and handed off rather than silently applied
by ordinary project agents. The [implementation spec](implementation-spec.md)
and [usage guide](USAGE.md) describe the executable subset of this design.

Proposed improvement flow:

1. **Capture an opportunity.** Audits, Client feedback, or observed delivery
   friction produce an item with evidence, expected benefit, and affected
   capabilities. Preserve the link to the originating run or finding.
2. **Prioritize deliberately.** The GM weighs Client impact, cost, risk, and
   ongoing commitments. The PM schedules selected items within an authorized
   improvement allowance. A backlog item is not permission to execute, and
   optional improvement must not silently displace committed Client work.
3. **Specify and implement.** Use the same BA, planning, engineering, and
   verification responsibilities as other delivery work. Define the expected
   improvement, baseline, regression obligations, and recovery path before
   evaluating the candidate. Reuse existing roles where adequate.
4. **Evaluate separately from adoption.** Keep a known working version while
   assessing a candidate against agreed outcomes. Preserve independent
   verification and adverse findings. Faster or cheaper execution does not
   justify reduced delivery quality or hidden failures.
5. **Adopt or revert explicitly.** The GM authorizes internal adoption only
   within its delegated remit; decisions reserved to the Client still go to the
   Client. Record the versions, evidence, and affected assignments. Changes to
   active runs require explicit migration or reissue, not silent replacement
   of their operating rules. State migrations need a tested recovery path that
   preserves work and journal history, not merely an older executable.

Proposal, implementation, evaluation, and adoption are distinct permissions.
An internal improvement may proceed autonomously only within an approved
improvement mandate and resource allowance; otherwise the GM seeks approval of
the bounded improvement package. Audit findings do not allocate resources or
permit displacement of Client commitments.

Before evaluating a material candidate, fix its baseline, success criteria,
regression obligations, and independent evaluator. Changes affecting the GM,
Auditor, or verification process cannot be approved by their authors' favorable
self-assessment. Evaluate in a separate context; preserve material disputes
and escalate unresolved authority or quality conflicts.

Prefer adoption at sprint or assignment boundaries. Urgent changes during a
sprint require explicit migration/reissue and re-verification of affected work,
not silent replacement of active contracts. Keep the prior version usable and
provide a tested state recovery method when formats change. If a candidate
degrades agreed outcomes, pause its rollout and revert or remedy it through an
authorized decision. Avoid unrelated simultaneous changes to the same
capability when that would make evaluation or rollback ambiguous.

Compare outcomes with relevant baseline cases and disclose task, environment,
and concurrent-change differences. Weak attribution means the benefit remains
unconfirmed; a cheaper or easier sprint alone does not prove improvement.

An improvement implementation run is delivery work and requires a final audit.
Audit-only work does not recursively require an audit. New recommendations can
remain in the backlog; completing an improvement must not automatically launch
an unlimited chain of further improvement runs.

Neither self-improvement nor GM ownership authorizes expanded permissions,
changed Client commitments, weakened acceptance criteria, or rewritten
governing principles. Specific improvement budgets, evaluation methods, and
adoption authority remain to be agreed before execution.

## Minimal work-item and handoff contract

Every claimed work item should have one active owner at a time. Ownership
transfer uses an atomic claim or equivalent serialized transition so two agents
do not unknowingly perform the same assignment. Each claim or reassignment has a
new assignment revision. Updates must match the current owner and assignment
revision; a late result from a previous assignment is retained as evidence, not
allowed to overwrite current state or automatically become verified. The PM can
route a useful late result for review, but cannot substitute it for required
verification or Client acceptance.

A work item records:

- stable identifier, engagement/run identifier, title, objective, and non-goals;
- assignment: role, agent instance if known, active owner, and assigning
  authority, with the assignment revision;
- specification, applicable design, and role-contract versions used;
- dependencies and readiness conditions;
- completion or check-in expectation and the authority responsible for recovery;
- expected outputs and acceptance evidence for the work item;
- status: proposed, ready, in progress, blocked, ready for review, verified,
  cancelled, or superseded;
- blockers, questions, assumptions, and requested decisions;
- links to decisions, events, artifacts, review findings, tests, and rework.

Use "claimed" for taking responsibility for work; do not call this "accepted." A
review verdict can request rework without making "rejected" a terminal task
state. "Client accepted" is reserved for acceptance of the integrated result.

Proposed transition rules:

- The GM or authorized PM makes an item ready after its dependencies and inputs
  are satisfied. Claiming it atomically assigns the owner and moves it to in
  progress.
- The owner can report a blocker or submit outputs for review, but cannot
  self-declare independent verification. The PM routes blockers and schedules
  separate review/test assignments linked to the implementation item.
- The designated verifier records the required evidence. Only after the
  applicable checks pass can the item become verified. Failed verification
  creates a finding and returns it to ready for a new implementation assignment,
  or blocked if a decision is needed.
- Cancellation, supersession, and resumption require an actor authorized by the
  recorded plan. The PM may coordinate these within that authority; scope or
  criteria decisions still go to the GM and, where required, the Client.
- Downstream work becomes ready only when its declared dependencies are met. No
  work-item status implies Client acceptance or a completed retrospective.

If a specification changes, active work does not silently rewrite itself. The GM
obtains the required decision from the authorized party; the PM may record and
execute that decision but not independently redefine scope or criteria. The
resulting change record names a new artifact version, identifies affected work
items, and either reissues, cancels, or continues them with an explicit
rationale. Completed evidence stays tied to the contract version that produced
it.

## Shared records and routing

C12 establishes three logical parts of the shared record. Current work state
shows the latest owner, status, blocker, dependency, and next action for each
work item. Append-only history records material events and decisions so the run
can be audited. Human-readable artifacts contain specifications, designs, plans,
role definitions, review reports, test evidence, delivery notes, and audit
results.

Every material state change and its journal event must be recorded consistently
as one logical operation, using a transaction or equivalent serialized update.
An event identifies its actor, run/work item, assignment revision where
relevant, time, outcome, and supporting artifact/decision references. Do not
report a transition as successful if its durable record failed. This is a
logical consistency requirement, not a commitment to a database or
event-sourcing system.

No message broker is required by default. Notifications are optional convenience
views that can be reconstructed from durable work state and events: new blocker,
assignment ready, review failed, verification passed, Client decision needed,
audit pending. Routing responsibility follows the current state: the active
owner acts next; if a work item is blocked, the PM routes the blocker unless it
requires GM or Client authority; if ownership is stale, the PM reclaims or
reassigns it and records why. A stale owner is an owner that has missed a
recorded expectation, become unavailable, or no longer matches the current
authorized assignment. The exact timeout/availability policy must be agreed
before execution; silence alone is not proof that a worker has stopped.

The execution mechanism checks durable actionable state at startup/resume and
after results or decisions, and dispatches only work authorized by the plan. The
PM owns tactical routing; the execution mechanism need not be another agent. A
restart must discover ready work, unresolved questions, and pending audits
without relying on an undelivered notification. No broker is needed to define
this behavior.

Agents should retrieve relevant context by artifact links and current state: the
applicable spec version, decisions, constraints, dependency outputs, and
required evidence. They do not need the full journal injected into every task.
The journal remains available for audit, investigation, and resolving disputes.

Role definitions may evolve under the GM's authority, but active work must
identify the role contract used when it was assigned. Updating a role definition
does not silently change existing assignments. The GM or PM must reissue work
when the new contract matters to the outcome.

### Stop, recovery, and management interruption

A stop request prevents new dispatch in the affected scope. Record stop
requested separately from confirmed quiescence: stale assignment rejection
does not stop an old worker from causing external effects. Workers preserve
outputs and effect status where possible. Before retrying an action with an
uncertain result, reconcile its external effects; do not treat the absence of
a successful journal entry as proof that nothing happened.

Before reassignment permits new mutation of shared resources, establish that
the old worker cannot still write them, or isolate the new work. Resume only
after reconciling owners, outstanding effects, applicable versions, evidence,
remaining limits, and audit obligations. Rollback or compensation requires its
own appropriate authority. A Client-cancelled scope needs renewed authorization
before restart.

If the PM is unavailable, the GM can restore tactical coordination or assign a
replacement PM. If the GM is unavailable, a previously authorized recovery
mechanism may restore one GM instance from durable records with exclusive
ownership and unchanged authority. A subordinate cannot promote itself to GM.
Until restoration, the PM may coordinate existing authorized work but cannot
start a new sprint, expand scope, adopt process changes, or assume the
Client-facing role. If no authorized recovery path exists or state is
insufficient, pause affected work and notify the Client through the established
channel. The runtime recovery mechanism remains an implementation decision.

An interrupted approval remains pending for the named candidate versions.
Restore the decision from the durable record or obtain it from the authorized
party; do not infer approval from partial conversation. An interrupted Auditor
leaves the audit pending under the Client-selected continuation rule.

## Walkthroughs

### Normal delivery

The GM clarifies a feature's high-level intent and tasks the BA to discover
details with the Client. The BA, Architect, and PM iterate on a specification,
design, and milestone/sprint plan, with collegium review and focused GM advice.
The GM presents the package and the Client approves its versions.

The PM drives the authorized sprint, assigning parallel work where safe.
Developers produce changes and tests; Reviewer and Tester record evidence for
the integrated increment. Agents leave feedback and the Auditor reports sprint
findings. The GM dispositions them, provides the requested Client update, and
authorizes the next sprint or another appropriate outcome.

At delivery, the GM presents the integrated package for Client acceptance,
optionally using the proposed H3 internal demo gate. Finished runs are audited;
the GM and Auditor consolidate project-wide learning and deliver a final
improvement report alongside the product artifacts.

### Clarification

During BA analysis, a requirement is ambiguous. The BA records the question and
impact. The GM either asks the Client or authorizes the BA to clarify directly.
The durable record is the question, answer, assumption if any, and updated spec
version. The next actor is the BA if more specification work remains, otherwise
the GM deciding readiness.

### Failed verification and rework

The Tester records that an acceptance path fails, with reproduction evidence.
The PM routes the finding to the Developer or Architect depending on cause. The
Developer claims the rework item, fixes it, and links the new evidence. The
Tester verifies again. If failures repeat or expose a criteria conflict, the PM
escalates to the GM for a decision. The failed evidence remains part of history.

### Interrupted worker

A Developer claims work and then stops responding or cannot continue. The PM
checks the recorded expectation or evidence of unavailability, marks ownership
stale, and records the reason. It reconciles uncertain effects and isolates or
stops previous writers before authorizing replacement mutation. The new owner
uses the spec version, current work state, prior outputs,
and history links; they do not need the interrupted agent's full private
conversation. If both old and new owners later produce results, the PM or GM
records the late result but does not accept its stale assignment revision as a
current update. Any useful patch is deliberately routed into current work and
verified; reassigning work does not authorize two workers to mutate shared
artifacts concurrently. Isolation or serialized mutation must be provided by the
eventual execution design.

### Scope change

The Client asks for an extra behavior during acceptance. The GM records a change
decision rather than treating it as hidden rework. If it clarifies an existing
criterion, affected work returns to the relevant stage. If it expands scope, the
GM creates or revises the specification and plan for a new or amended delivery
run. No numeric budget is imposed here; budgets and stop rules are approval
decisions.

## Owner decisions before implementation

1. Adopt this logical contract as the first default workflow baseline.
   Recommended default: yes, because it is auditable and preserves GM
   accountability without forcing a platform architecture.
2. Decide whether to adopt the proposed H3 manager-first demo gate. Recommended
   default: keep it optional; integrated verification is required regardless.
3. Approve the minimal work-item states and one-active-owner rule at the
   specification level. Recommended default: yes, because wakeup, stale
   ownership, and duplicate-result handling need simple shared semantics before
   runtime selection.
4. Decide how strictly changed role definitions apply to active work.
   Recommended default: no silent retroactive changes; reissue affected work
   with a recorded decision.
5. Adopt the proposed readiness rules and refinement envelope; set actual
   operating limits, reporting cadence, milestone acceptance points, and
   improvement allowance per engagement. Full-auto retains initial Client
   specification/architecture/plan approval.
6. Adopt the proposed nested engagement/run/sprint mapping. Audit continuation
   is already decided: pause by default; only the Client may authorize a
   specific exception, without clearing the audit obligation.
7. Choose when to demonstrate reconstruction beyond routine specification-gap
   review. Do not claim reconstruction has been proven by a checklist.
