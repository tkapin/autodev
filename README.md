# AutoDev

**From intent to verified software.**

AutoDev is a proof of concept for a spec-driven, autonomous, iterative software
development system. It will coordinate specialized AI responsibilities across
the software lifecycle, from clarifying intent to delivering software and
improving the development process itself.

**Status:** v0.1.1 is implemented and has been validated in both target hosts:
an `autodev` skill, GM and supporting role agents, and Python/SQLite coordination
tooling. Offline checks, two live delivery/learning trials, and fresh app skill
discovery completed. Final independent review also produced three corrected
edge cases with regression coverage. See [validation evidence and limits](VALIDATION.md).
The charter remains authoritative; the implemented scope is defined in
[the v0.1 implementation spec](implementation-spec.md).

AutoDev is a working name, not a unique public brand: other development tools
already use it. The intended distribution/plugin identifier is `tkapin-autodev`;
this is a naming convention, not a registered or verified available package.

## Try the implementation

See [installation and use](USAGE.md). In PowerShell 7 from this directory:

```powershell
.\Install-AutoDev.ps1 -HostTarget CLI
```

The standalone project is maintained at
[tkapin/autodev](https://github.com/tkapin/autodev). The repository root contains
the project documentation, installer, and tests; `tkapin-autodev/` is the
self-contained plugin package. The optional app adapter requires its host's
plugin-management command; see the usage guide before installing for both hosts.

In a target-project session, invoke `/autodev` with the desired outcome or select
the packaged GM agent. The [plugin](tkapin-autodev) contains the skill, role
agents, operating guide, and dependency-free coordination helper. Model access
and host permissions still apply; see the host-specific notes in the usage guide.

## Problem statement

AI-assisted development often relies on a person to carry requirements,
coordinate tools and agents, assess completion, and restart work when progress
stalls. Individual coding conversations are not, by themselves, a repeatable
software production process.

The problem this PoC will investigate is how to turn an evolving software idea
into verified working software through an explicit, reusable process that:

- Captures requirements as reviewable specifications rather than leaving them
  implicit in conversation history.
- Identifies ambiguity, missing requirements, assumptions, and unanswered
  questions before treating a specification as ready for implementation.
- Coordinates design, planning, implementation, review, and testing without
  requiring a person to direct every step.
- Iterates meaningfully on defects and unmet requirements rather than merely
  repeating prompts or accepting an agent's claim of success.
- Preserves engineering simplicity instead of producing unnecessary agents,
  abstractions, infrastructure, or speculative optimizations.
- Uses delivery evidence and session audits to improve both the software and
  the process that produces it.

The initial user is the project owner, who will use the resulting system on
their own projects and evaluate whether it is useful enough to reuse more
broadly.

## Intended outcome

Develop a reusable set of Markdown specifications, role definitions, prompts,
and skills, supported by an executable autonomous development loop and
packaged as a plugin usable by Copilot CLI and the Copilot app.

Portability is a goal, not a claim that one plugin format works everywhere.
The first implementation uses one compatible plugin layout for those two
hosts. Other host integrations are not part of v0.1.

## Scope

The intended lifecycle includes understanding the business need, clarifying
requirements, specifying acceptance criteria, designing an appropriately simple
solution, planning work, implementing it, reviewing it, testing it, and
producing a delivery outcome with supporting evidence.

The owner's proposed operating model emulates professional software development
at scale: specialized agents perform clearly assigned work, exchange focused
instructions and evidence, and deliver through manager review to owner
acceptance. The organizational structure is a hypothesis to evaluate, not a
fixed blueprint. The goal is professional accountability and quality, not
organizational ceremony.

It also includes auditing completed and failed development sessions to identify
improvements to prompts, skills, coordination, verification, and resource use.

See [roles and terminology](roles.md) for the short role definitions and
reporting relationships. **General Manager (GM)** is the working
name replacing Delivery Manager; references to "the manager" below mean this
role. **Client** is the term for the requesting human or authorized
external agent, previously called the owner or user.

Specialized agent execution is a design requirement, not merely an optional
optimization. The exact agent roster, role combinations, and degree of
parallelism remain open. Simplifying the agent structure must preserve clear
responsibilities and acceptance against the owner's intent. The exact
manager-to-owner review sequence remains a design hypothesis.

The initial scope excludes a general-purpose agent platform and deployment
without explicit authority. The selected v0.1 helper uses Python's standard
library and SQLite, with Copilot supplying actual agent execution.

## Principles

The Client accepted the [17-principle governing charter](principles.md) on
2026-09-21 as a good starting set. That file is the authoritative source, with
stable C01-C17 identifiers and a mapping from earlier P/H/R references.

The Client prefers a smaller, more powerful set over time. Consolidate overlaps
as the design is exercised, and move procedural detail into policies rather
than adding principles indefinitely. Do not discard safeguards merely to hit
an arbitrary count.

The charter applies both to engineering AutoDev and to the development it
coordinates. Our execution-placement and single-point-of-contact collaboration
policy (formerly P6) remains separate; it does not require human approval before
every autonomous internal handoff.

The [four-model review](reviews/principles-synthesis.md) preserves the reasoning,
alternatives, and disagreements behind adoption. Its original proposal status
is historical, not the current charter status.

### Remaining organizational and policy decisions

- H1: exact agent instantiation and verification-exception policy.
- H2: detailed procedures for the differentiated criteria responsibilities
  adopted in C08, rather than undifferentiated joint BA/GM ownership.
- H3: whether a separate internal manager-first demo is useful. It remains
  optional and unapproved as a mandatory gate.
- R1/R4: their governing commitments are now adopted in C07/C17; concrete
  limits, metrics, and evaluation mechanisms still need design.

No storage technology, runtime, numerical budget, trial execution, or entire
workflow state machine is approved merely by accepting the charter.

## Design sources and implementation

The operating model was developed around these responsibilities:

1. Principles and their scope, distinguishing rules from defaults and hypotheses.
2. Agent responsibilities and the workflow between them, including who owns
   delivery and who can authorize transitions.
3. Per-role contracts: inputs, outputs, decisions, communication, evidence,
   escalation, and completion.
4. A human-auditable shared coordination record. A journal, tickets, and a
   message bus are candidate mechanisms; no storage or transport is selected.
5. Orchestration and governance for progress, rejection, changes, interruption,
   and recovery.

The existing trial proposal is supporting material for later validation, not
the immediate implementation plan.

The [GM role contract](role-contracts/general-manager.md) is the first detailed
role contract. It specifies the GM's inputs, authority, BA/Architect/PM
relationships, decision cycle, outputs, and independent improvement evaluation,
with scenarios for a later dry run. It does not install an agent or select a
runtime by itself. The packaged role agents and helper implement the scoped
baseline in [implementation-spec.md](implementation-spec.md), rather than every
possible policy in the broader design documents.

Concrete [GM decision exercise packets](evaluation/gm-decision-cases.md) and a
separate [evaluator rubric](evaluation/gm-decision-rubric.md) make a subset of
those scenarios assessable from supplied artifacts, not announced diagnoses.
They include both problems requiring intervention and a ready next sprint.
The packets are synthetic, have not been executed, and do not authorize a
delivery trial or runtime.

The [workflow and coordination contract](workflow-and-coordination.md) is the
current draft for this design work. It proposes the GM's operating loop,
lifecycle transitions, assignments, shared records, handoffs, and recovery
examples. Self-improvement is a required capability covering AutoDev's own
tooling as well as its agents and workflows; the draft describes how the GM
commissions and evaluates that work through the same delivery process.
The broader draft contains policies beyond v0.1; its implementation choices and
deliberate limits are identified in the implementation spec and usage guide.
Actual resources and authority still need agreement for each engagement.
The shared-record triad is accepted as C12 (formerly P13).

Three independent workflow critiques (GPT-6 Astra, Claude Opus 5, and Grok 4.6)
informed proposed readiness, change-authority, integration, recovery, and
self-improvement rules in that draft. It distinguishes Client acceptance from
complete audit/handover closure. The Client selected pause-by-default when a
sprint audit cannot finish, with a specific Client-authorized continuation
exception available. Other workflow defaults are proposals, not evidence of an
implemented or validated autonomous runtime.

### General Manager-led workflow outline

C05 establishes the accountability model. The following sequence is a proposed
workflow to elaborate, not a frozen roster or executable state machine:

1. The GM clarifies the high-level ask and engagement preferences with the
   Client, then tasks the BA to discover details through targeted questions,
   examples, and corner cases in the same engagement.
2. The GM iterates with the BA, Architect, and PM to develop the specification,
   sound architecture, and a project plan with main parts, milestones, and
   value-delivering sprints. Multi-model collegium review and additional
   rubber-duck advice challenge the work; consensus is not proof of correctness.
3. The GM presents the combined package for Client approval. Full-auto
   refinement permits autonomous internal rounds within agreed limits, not
   skipping this approval or inventing material Client preferences.
4. The PM drives authorized sprints, spawns or assigns Developers, Reviewers,
   Testers, and other needed agents, and coordinates safe parallel delivery.
   It reports progress and exceptions to the GM without sacrificing quality
   for speed.
5. Agents leave process feedback at assignment completion. The Auditor reviews
   each finished sprint using feedback and objective evidence. The GM
   dispositions findings, commissions controlled improvements or records
   deferred work, and authorizes the next sprint, replans, pauses, or stops.
6. The GM provides sprint summaries when requested, including delivered value
   and improvement findings. Reporting does not itself require Client approval
   after every sprint.
7. At closure, the GM presents the integrated product for acceptance and
   consults the Auditor on overall learning. The final handover includes code,
   specifications, other artifacts, evidence, and an improvement report.

Specifications are the primary durable product definition. The goal is to
recreate the specified system from the versioned specification package and
declared dependencies, without hidden conversational or implementation
knowledge. This means equivalent required behavior, not identical source code.
Specs evolve with authorized learning; overall planning does not require
exhaustive upfront detail for every later sprint.

At any stage, the Client may ask the GM for technical details or other
information. The GM collects the relevant internal evidence and uses the BA or
Architect as appropriate to prepare the answer. This does not transfer the
Client to a Developer, Tester, or another execution agent.

The GM or Client can also initiate an Auditor review of the process,
communication, agent roles, or other framework behavior. The Auditor returns
findings to the GM, who records its response and coordinates workflow
improvements, including agent-definition changes or a new role where justified.
This direct Client audit-request path does not transfer delivery
accountability away from the GM or require a separate user-facing session.

Independently of ad hoc requests, every finished delivery/workflow run must
receive a retrospective audit. The GM uses its feedback to improve agents,
communication, and coordination; unsuccessful finished runs are included.
Unfinished audit work stays visible separately from the delivery outcome.

The owner explicitly accepted the distinction between an accountability point
and a communication bottleneck. Under C05, specialist-to-specialist handoffs are
permitted through the shared coordination record; the manager need not personally
relay every message. Such handoffs remain explicit, human-auditable, and visible
to the manager. They do not grant additional decision or acceptance authority.

The GM replaces the earlier Delivery Manager role; it is not another layer above
it. The Client is the requesting party, not a subordinate. Terminology and
per-role boundaries are maintained in the [role glossary](roles.md).

## Delivery phases

### 1. Research existing approaches

Investigate agentic development frameworks, spec-driven workflows, autonomous
coding loops, Ralph-style loops, and relevant primary-source work by practitioners
such as Andrej Karpathy.

Record sources and dates, distinguish demonstrated behavior from claims, and
identify which ideas are transferable. A technique should be attributed to a
person only when supported by their own published material.

**Expected output:** A focused research synthesis covering useful patterns,
failure modes, tradeoffs, and build-versus-reuse options.

**Progress:** Three bounded, independently researched tracks were completed on
2026-09-20. See the [research reports and fresh-session handoff](research/README.md).
They cover reusable systems, autonomous loop mechanics, and evidence for agent
organization. These reports preserve the initial research snapshot; the later
runtime selection and completed trials are documented in the implementation
spec and validation report. See the
[first AutoDev trial proposal](first-trial-proposal.md) for the current draft
experiment charter.

### 2. Select principles and responsibilities

Use the research to agree on the development principles, human decision points,
specification readiness criteria, completion criteria, autonomy boundaries, and
minimum useful specialized agent structure, delivery-quality ownership, and
demonstration and acceptance flow. Evaluate H1-H3 rather than assuming the
proposed organizational structure is the only valid design.

**Expected output:** Reviewed principles and explicit decisions, with unresolved
questions recorded rather than silently converted into assumptions.

### 3. Design specifications, prompts, and skills

Collaboratively author the Markdown artifacts that define the agents' work.
Specify responsibilities, required context, outputs, handoffs, review criteria,
and escalation behavior. Distinguish role instructions from reusable skills.

**Expected output:** A small, coherent, reviewable artifact set that can be tried
on a representative development task.

### 4. Implement and evaluate the loop

Choose a runtime based on the agreed requirements. Implement the smallest
end-to-end loop that can take a ready specification through implementation,
review, verification, and meaningful rework.

**Expected output:** An executable PoC with observable progress, durable state,
explicit failure reporting, bounded execution, and evidence for its outcomes.
Exact budgets and evaluation thresholds remain to be specified.

### 5. Package for reuse

Package the validated prompts, skills, and execution capabilities as a plugin,
adding tool-specific integration only where needed.

**Expected output:** A documented installation and usage path for the first
chosen host, plus an explicit compatibility scope for other tools.

### 6. Use, audit, and improve

Apply the system to the owner's projects. Review successful, failed, stalled,
and interrupted sessions. Evaluate targeted process changes against a baseline.

**Expected output:** Evidence-backed revisions to the system, including a record
of what changed, why, and whether it improved outcomes.

## Collaboration and context management

The owner prefers short, focused sessions and clean-context subagents to avoid
context pollution. P6 is an active collaboration rule, not merely a future
product feature.

- At each work-package boundary, state the objective and recommend an execution
  approach. Briefly explain the relevant context-isolation benefit, continuity
  needs, delegation overhead, and expected output. Ask the owner to choose and
  wait; a recommendation alone is not approval.
- A work package is a coherent task such as a research question, a principles
  review, or an implementation slice. Do not ask before every file read, edit,
  or validation command within an already agreed package.
- A choice applies to the stated package, not indefinitely to future work.
  Ask again if its scope or execution approach materially changes. If the
  owner explicitly selected the approach in the current request, acknowledge
  that selection without asking the same question again.
- Prefer clean-context subagents for substantial, bounded research or execution
  tasks that benefit from isolation. Independent research questions are good
  candidates for separate agents.
- Keep small edits, immediate decisions, and collaborative principle discussions
  in the main session when delegation would add overhead without useful
  isolation. Do not split a tightly coupled task merely to increase agent count.
- Give each delegated task a bounded objective, relevant requirements and
  decisions, authoritative inputs, expected output, and a stopping condition.
  A clean context must still be a sufficient context.
- Include the approved execution scope in the handoff. Delegated agents should
  execute that bounded assignment, not repeat the placement question or launch
  additional agents outside the approved scope.
- Bring concise findings, evidence references, uncertainties, and decisions back
  to the main session instead of copying full exploration transcripts.
- Clean-context delegation does not transfer user-facing coordination. The
  parent session remains the sole coordinator for presenting delegated results
  and asking the owner for decisions, unless the owner explicitly changes that
  contact model.
- Persist agreed specifications and decisions in project artifacts. Fresh
  sessions should read those artifacts rather than depend on prior chat history.
- Recommend a fresh session when moving into a substantial new phase or when
  accumulated exploratory context is no longer relevant.
- Follow the owner's model policy: explicitly select non-Anthropic models for
  delegated work unless the owner authorizes a specific exception. Do not rely
  on inherited routing that could violate that policy.

For this principles-capture package, the owner selected the main session after
receiving a recommendation. Subsequent work packages require their own
placement decision under P6.

## Open decisions

- Which specific existing-code enhancement should prove the first loop useful?
- What makes a specification ready, and who resolves unanswered questions?
- What distinguishes required human approval from an autonomous decision?
- What measurable evidence defines completion and engineering quality?
- Which limits and escalation rules prevent unproductive or unsafe execution?
- How should specialized responsibilities map to agent instances, and which
  require independent execution or review?
- What must a handoff contain, and when is retained task context preferable to
  a fresh context?
- How do the business analyst and manager resolve disagreements about criteria,
  and how are changes to criteria approved?
- What constitutes a sufficient demo for each kind of deliverable, and how are
  manager review, owner acceptance, and requested rework recorded?
- What is the simplest adequate runtime and durable handoff format?
- Which tool should host the first plugin, and what portability is actually
  required?
- What session evidence should be retained, and how should sensitive data be
  protected?
- How should process changes be evaluated and approved before adoption?

## PoC success

The PoC should demonstrate a traceable path from intent through a reviewed
specification to working software with acceptance evidence. It should
demonstrate specialized agent handoffs, criteria and metrics with explicit
ownership, and a demo and deliverables evaluated against the owner's ask through
the selected acceptance workflow. It should show how the loop responds to failed
verification or unaccepted deliverables and when it stops or asks for help.
It should also support a repeatable trial on another task and an audit that
produces a testable process improvement.

Concrete scenarios, metrics, budgets, and thresholds must be agreed before
claiming success. The bounded v0.1 implementation and its actual evidence are
documented in [VALIDATION.md](VALIDATION.md); broader efficacy remains unproven.

## Earlier experiment decision

For the first AutoDev experiment charter, the owner selected a small
existing-code enhancement with deterministic tests as the representative task
shape. The exact repository area, behavior change, acceptance evidence,
simpler baseline, specialized-agent structure, stop rules, and resource budget
were left open in that earlier proposal. It was not the subsequently executed
Python trial and should not be read as the current implementation status.
