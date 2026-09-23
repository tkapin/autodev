# AutoDev roles and terminology

## Status and terminology

This records the initial role list accepted by the owner during the design
discussion. It is a short glossary, not a set of executable agent prompts.
The General Manager's overall accountability, authority to task internal
agents, and responsibility for their workflow reflect the owner's stated
requirements. Agent instantiation and detailed authority contracts remain open
under the [accepted charter](principles.md); accepting the roles does not require
one persistent agent per role. H1/H3 and detailed authority procedures remain
open; C08 establishes differentiated criteria responsibilities.

The first detailed [GM role contract](role-contracts/general-manager.md) defines
proposed inputs, decision rights, supporting-role handoffs, outputs, recovery,
and evaluation scenarios. It is a draft contract, not an installed agent.
The [packaged role agents](tkapin-autodev/agents) provide concise executable
instructions for the core roles. Their operating baseline is documented in
[the v0.1 implementation spec](implementation-spec.md).

**General Manager (GM)** is the working name for the role previously
called Delivery Manager or Manager. It covers business understanding, technical
delivery, and team coordination without creating another management layer.

**Client** is the term for the requesting party: normally the human
user, occasionally an authorized external agent. Earlier documents use
"owner" or "user" for this party. "User" remains an informal synonym for Client,
especially when the requester is human. The Client is outside AutoDev's internal
reporting hierarchy; an external agent's authority must be explicitly defined.

A **role** is a responsibility contract. An **agent** is an execution instance
assigned a role. Role separation does not automatically require persistent
agent instances or a particular runtime.

## Short role definitions

- **Client:** Commissions the work, supplies desired outcomes and constraints,
  resolves business decisions, and accepts or rejects delivery within its
  authority. Does not have to coordinate AutoDev's internal agents.
- **General Manager:** Manages all internal agents and is accountable to the
  Client for the overall result. Defines the project workflow, assigns and
  redirects work, coordinates dependencies and escalations, and presents
  integrated results and answers to Client information requests. Relies
  extensively on the BA, Architect, and PM as its primary supporting roles for
  business clarity, technical coherence, and tactical execution management.
  Maintains enough system-level understanding to judge recommendations,
  dependencies, risks, and tradeoffs, not every implementation detail. Maintains
  the overall project picture and actively improves the workflow to deliver the
  best-quality outcomes for the Client, not merely the lowest execution cost.
  Reviews and updates individual agent definitions and introduces new roles
  when justified by delivery needs. Is accountable for adherence to AutoDev's
  governing principles across its own decisions, all subordinate agents, and
  the overall workflow.
- **Business Analyst (BA):** Investigates needs, identifies ambiguity, prepares
  clarification questions, and develops requirements and proposed acceptance
  criteria. Uses targeted questions, examples, and corner cases to discover
  actual Client needs without an exhaustive questionnaire. Maintains the input
  specification and its evolution alongside the Architect and PM.
  Supplies the GM with the detail and options needed to obtain sound
  Client decisions. When tasked by the GM, discusses concrete requirements
  directly with the Client and reports the conclusions back to the GM.
- **Project Manager (PM):** Turns delivery goals into work items, dependencies,
  assignments, and a practical execution plan. Maintains progress and blocker
  records, follows up on handoffs, and performs tactical coordination within
  authority delegated by the GM. Develops the project structure, milestones,
  and incremental sprint plan. After Client plan approval and GM sprint
  authorization, drives sprints, spawns or assigns execution agents, coordinates
  safe parallel work and integration, and reports progress periodically to the
  GM. Optimizes speed without sacrificing quality.
- **Architect:** Owns the coherent technical view of the system and advises the
  GM from specification discovery onward, not only after requirements are
  written. Reviews feasibility, quality attributes, interfaces, dependencies,
  and technical risks. Designs the simplest adequate solution, records
  significant tradeoffs, and maintains the architecture as implementation
  evolves. Does not unilaterally redefine business intent or acceptance criteria.
- **Developer:** Implements assigned changes and implementation-level tests,
  produces supporting artifacts, and addresses defects and review findings.
- **Reviewer:** Independently examines changes for correctness, maintainability,
  specification alignment, and agreed engineering standards. Returns actionable
  findings supported by evidence.
- **Tester:** Verifies observable behavior through acceptance, regression, and
  failure-path checks. Produces reproducible defect reports and pass/fail
  evidence.
- **Process Auditor (Auditor):** Can be commissioned by the GM or directly by
  the Client to examine the effectiveness of the whole development framework:
  processes, communication, role design, handoffs, and resource use. Identifies
  bottlenecks and quality problems, and returns evidence-backed findings and
  recommendations to the GM for workflow improvement. Does not automatically
  change the rules it audits. Must audit every completed delivery/workflow run
  using the records of all participating agents. Audits each finished sprint
  using agent feedback and objective evidence, then consolidates project-wide
  learning with the GM at closure.

## Reporting and delegation

All internal agent roles report to the **General Manager**, including the BA,
PM, Architect, Developer, Reviewer, Tester, and Process Auditor. The PM is not
a peer manager with separate overall delivery accountability.

The GM can task each subordinate with a bounded objective, relevant inputs,
expected outputs, authority, and completion conditions. It can delegate tactical
assignment and follow-up to the PM without transferring overall responsibility.
The GM also decides how responsibilities and handoffs fit together for the
project, within agreed principles, Client constraints, and granted authority.
That does not imply permission to rewrite AutoDev's governing principles.

Principle compliance is an active GM responsibility, not merely an instruction
for individual specialists. The GM must ensure that assignments, role changes,
workflow adaptations, and delivery decisions remain consistent with the
principles. It addresses deviations, uses Auditor findings to identify gaps,
and escalates unresolved conflicts or requests to change principles rather than
silently making exceptions for speed or convenience.

The BA, Architect, and PM form the GM's primary advisory group: the BA makes
the requested outcome precise; the Architect makes the system technically
coherent; the PM makes delivery organized and trackable. They collaborate on
specifications and plans rather than operating as isolated sequential stages.
Their outputs inform GM decisions without forcing it to perform all analysis,
technical design, and scheduling itself.

The GM can commission additional advisors and independent critiques for a
bounded question. Specification review uses a collegium of agents backed by
different permitted models, covering business, architecture, and delivery
perspectives. A role is not permanently tied to a model. The
[workflow draft](workflow-and-coordination.md) defines the proposed review
procedure; model choices and panel size remain open. Advice does not transfer
GM accountability, Client acceptance authority, or specialist responsibility.

### GM decision quality

The GM is the highest-leverage role because its decisions shape assignments,
workflows, and the whole delivery organization. Developing and evaluating its
judgment is a priority, not a reason to centralize all specialist work in its
context. A strong underlying model helps but is not sufficient on its own.

Evaluate the GM through delivered Client outcomes, technical quality, useful
delegation, handling of uncertainty and disagreements, timely intervention,
and effective use of resources. Persuasive summaries, apparent confidence, or
agreement among advisors are not substitutes for evidence. The GM should
recognize when its understanding is insufficient and obtain focused advice.

The Auditor's remit includes the GM's own decisions and performance. Proposed
changes to GM instructions, advisory practices, or decision procedures require
independent evaluation and a revert path under C11/C17; the GM's own favorable
assessment is not sufficient. Concrete evaluation cases and model selection
remain to be designed within the Client's model policy and operating limits.

## Agent and role evolution

The GM has authority to review how individual agents perform and, where needed,
update their role definitions, instructions, responsibilities, and handoff
contracts within the agreed operating boundaries. It can obtain specialist
help with that work, but remains accountable for the changes.

For v0.1, the Client selected automatic adoption only for independently
evaluated, reversible project-local improvements. Changes to the shared plugin
require a specific Client approval and a separate source-change/installation
workflow. Routine delivery agents do not edit the installed plugin.

This includes delegating organizational design itself. If role analysis or
instruction design exceeds the GM's useful capacity, it can introduce a
specialist to improve the quality of that work and reduce its own context
burden. Illustrative roles, not mandatory additions to the initial roster:

- **Role Designer (Role Definer):** Develops or revises role contracts,
  instructions, responsibilities, and collaboration boundaries for the GM.
- **Agent Behavior Analyst ("Psychologist"):** Investigates observed agent
  behavior, recurring reasoning or communication failures, and the effects of
  instructions and role interactions. Recommends improvements from recorded
  evidence; the metaphor does not imply human psychological diagnosis.

These specialists report to the GM like other agents. They propose
organizational changes; the GM remains responsible for deciding which changes
to adopt within its authority and for their impact on delivery. Delegating role
design does not require the GM to personally author every prompt or contract.

The initial role list is not closed. The GM can introduce a completely new role
when it identifies a genuine need. It defines the purpose, responsibilities,
inputs, outputs, decision rights, communication paths, reporting relationship
to the GM, and completion evidence before assigning work to that role. Under
C04, it must consider whether an existing role can meet the need without
unnecessary organizational complexity.

Agent-definition changes and new-role decisions belong in the shared project
record with their rationale and affected workflows. Revised handoffs must be
communicated to the agents that depend on them; earlier audit findings and
delivery evidence must remain traceable.

This organizational authority is not permission to expand tool access, bypass
model restrictions, change Client requirements or acceptance authority, or
rewrite governing principles. Such changes still require the appropriate
authorization. C17 requires proportionate evaluation and a revert path;
specific methods remain policy decisions.

## Communication and evidence

The GM is the Client's sole business contact and owns the engagement, including
scope, commitments, priorities, delivery status, and acceptance coordination.
The Client should experience dealing with a software development company, not
managing a collection of agents.

The Client does not communicate directly with individual Developers, Testers,
Reviewers, or other execution agents. Requests for technical details, test
results, implementation explanations, or progress go to the GM. The GM obtains
the relevant evidence internally, typically uses the BA or Architect to assemble
an appropriate explanation, and returns a coherent answer to the Client.
Summarization must preserve material limitations, failures, and uncertainty.

The previously agreed exception is GM-authorized BA clarification: the GM can
task the BA to discuss concrete requirements directly with the Client in the
same engagement. This is not general permission for every specialist to become
client-facing. The Client is not required to visit subordinate sessions or take
over coordination.

The Client can also commission an Auditor review directly. This is an explicit
audit-request exception to the usual GM-led contact model, not a requirement
for the Client to supervise another agent session. Findings go to the GM for
action and remain visible in the shared record.

The BA records the discussion's answers, assumptions, unresolved
questions, and implications in the shared project record and returns them to the
GM. The GM remains accountable for follow-through and consistency with the
specification. Delegating a clarification conversation does not itself authorize
the BA to change business commitments or approve delivery.

Internal agents may communicate directly through explicit, human-auditable
handoffs in the shared coordination system. The GM retains visibility without
relaying every message. Storage and transport choices remain undecided.

Reporting authority does not invalidate independent findings. Reviews, failed
tests, and audit findings remain visible under C10/C11; assigning work is not
authority to suppress evidence or declare unmet criteria satisfied.

## Audit and workflow improvement

Each agent leaves concise, evidence-linked process feedback at assignment
completion for the Auditor, including what worked, bottlenecks, and possible
improvements. Observations about peers are limited to work actually seen;
missing feedback and uncertain interpretations remain explicit. These
handoffs are not separate per-agent audits.

Every finished delivery/workflow run triggers a mandatory Auditor review.
The owner selected this run-level boundary, not an audit after every individual
agent session or conversational turn. Review the whole run, including all
participating agents' records. A run ending in failure or cancellation still
provides audit evidence; a paused run is not a finished run.

The Client's sprint-based workflow also requires an audit at each finished
sprint and a final project-wide synthesis. The GM consults the PM and other
specialists on findings, records changes or deferred improvements, and
authorizes the next sprint, replans, pauses, or stops. A report can cover
coincident boundaries without duplicating the audit. The workflow proposes
multiple sprints within a delivery run. The Client selected pause-by-default
when a sprint audit cannot finish; only the Client may authorize a specific
continuation exception, and the audit obligation stays outstanding.

The Auditor supplies an explicit completion assessment against commissioned
scope and evidence requirements, with unfinished examination separate from
source coverage limitations and findings. Missing supplemental feedback does
not automatically mean incomplete; missing mandatory evidence without an
approved alternative does. The GM checks this handoff rather than inferring
completion from the presence of a report. See the
[Auditor completion handoff](workflow-and-coordination.md#auditor-completion-handoff).

The PM owns arranging integrated verification with a named verifier and
artifact version; individual task success cannot establish sprint success.
The GM uses the workflow's readiness and change-authority rules rather than
requiring unanimous advisors or authorizing endless refinement. Findings about
the GM and their dispositions remain visible in the Client's closure report.

The retrospective must identify what went well, gaps, bottlenecks, and
recommended improvements to agent definitions, communication, coordination,
and other relevant process elements. The GM is responsible for commissioning
the review and addressing its findings. If the audit cannot complete, keep
that obligation visibly outstanding rather than treating it as performed.
The delivery outcome and the audit outcome are separate records.

Audit-only activity does not recursively trigger another mandatory audit.
The GM or Client may still request an additional audit explicitly.

The GM is responsible for both the delivered result and the effectiveness of
the process producing it. It maintains a project-wide view of intent, work
status, dependencies, decisions, quality evidence, and risks without requiring
every specialist transcript in its context.

The GM or Client commissions an audit with a defined scope. The Auditor can
examine the GM's coordination as well as subordinate roles, and reports
bottlenecks, causes, supporting evidence, and proposed improvements to the GM.
The GM records its response, tasks the relevant agents, and updates the project
workflow within its granted authority. It records reasons for deferring or
rejecting findings rather than silently ignoring them.

For each finished run, retain the audit report and the GM's disposition of its
recommendations, including assigned improvement work or reasons for taking no
action. A mandatory audit does not mean every recommendation must be adopted.

The improvement objective is efficient delivery of high-quality Client
outcomes. Faster execution, fewer agents, or lower cost alone do not demonstrate
improvement if correctness, maintainability, or satisfaction of the ask suffers.
Audit findings do not grant authority to change Client requirements, acceptance
criteria, or governing principles without the appropriate approval. C17
requires outcome-based, reversible improvement; specific baseline-comparison
and evaluation procedures remain to be designed.

## Remaining design work

The [workflow and coordination draft](workflow-and-coordination.md) proposes
the common work-item, handoff, routing, and recovery contract for these roles.
The design draft is not itself an implementation or storage selection; the
implementation spec records the selected local v0.1 subset.

Define each role's input/output contract, decision rights, escalation rules,
completion evidence, and allowed state transitions. Detail C08's criteria
authority procedures and evaluate the review/demo sequence in H3. Select a
coordination-record model before choosing its implementation.
