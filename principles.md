# AutoDev governing principles

## Status and scope

Accepted by the Client on 2026-09-21 as the initial working charter. These 17
principles govern both AutoDev's own engineering and the software delivery it
coordinates, where applicable. They are requirements, not claims that an
implementation already enforces them.

The Client prefers a smaller, stronger set over time. Consolidate overlapping
principles as experience develops, and move procedural details into policies and
role contracts rather than continually expanding the charter. Preserve useful
safeguards and the decision history when consolidating.

The C01-C17 identifiers preserve the mapping to the
[four-model review synthesis](reviews/principles-synthesis.md). This file is
authoritative; the review reports remain historical evidence.

## Charter

### C01. Deliver Client value, not factory activity

Optimize for useful, accepted outcomes and engineering quality, not agents
launched, documents produced, token savings, or apparent busyness. Make quality,
cost, and time tradeoffs explicit within agreed constraints.

### C02. Make intent, assumptions, and uncertainty explicit

Maintain living, versioned requirements, constraints, non-goals, and acceptance
expectations. Resolve material unknowns with the authorized decision-maker;
record lesser assumptions. Conversation informs the specification rather than
becoming an invisible alternative source of authority.

### C03. Deliver and learn in small, verifiable increments

Specify enough for the next valuable slice, integrate it, obtain feedback, and
adjust. Use proportionate discovery instead of exhaustive prediction. Failed or
cancelled attempts remain honest outcomes, not promises of eventual success.

### C04. Choose the simplest adequate engineering and organization

Prefer maintainable solutions and existing capabilities. Apply separation of
concerns and target-project standards proportionately. Add abstractions,
infrastructure, roles, or handoffs only when their benefit justifies the
complexity. Simplicity does not waive required quality checks.

### C05. Keep one accountable GM and explicit delegated authority

The General Manager owns commitments, principle compliance, coordination, and
the overall result. All internal roles report to it, but auditable peer handoffs
are allowed. Preserve the Client-facing model, authorized BA clarification, and
Client-commissioned audits. Delegation does not transfer accountability.

### C06. Specialize through clear contracts and sufficient focused context

Assignments identify purpose, relevant input and contract versions, authority,
outputs, evidence, and escalation conditions. Use curated context and durable
handoffs, not full-history copying or context-free prompts. A role is a
responsibility contract, not necessarily a persistent agent.

### C07. Bound autonomy by authority, resources, risk, and progress

Establish permitted actions, access, resource limits, stopping conditions, and
escalation before execution. Honor cancellation and stop unproductive loops
without lowering criteria. External or irreversible effects require appropriate
authorization; creating a role does not expand permissions.

### C08. Define done and who can decide it

Separate business acceptance criteria from engineering obligations and an
explicit delivery boundary. The BA develops business clarity, technical
specialists contribute engineering requirements and evidence, the GM ensures
coherence, and the Client retains acceptance authority. Verified, accepted,
released, unsuccessful, and audit-pending are distinct outcomes.

### C09. Treat relevant quality attributes as requirements

Identify applicable maintainability, security, privacy, reliability,
accessibility, performance, and compatibility expectations. Scope evidence to
the actual product and risk; make exclusions and accepted limitations visible.
Avoid both silent omission and indiscriminate checklists.

### C10. Verify the integrated result and protect existing behavior

Use repeatable build, test, regression, and failure-path evidence appropriate to
the change. Record inputs, environment, commands, and delivered versions so
another actor can reproduce the result. Distinguish passing, missing, flaky, and
failed checks. Isolated task success does not establish integration.

### C11. Preserve independent challenge, findings, and uncertainty

Self-approval or a persona switch is not independent verification. Use a
separate verification context by default for software changes, record the actual
separation, and make proportionate exceptions explicit. Preserve findings and
give material unresolved disputes an escalation path; management cannot make
negative evidence disappear.

### C12. Keep current state, an append-only journal, and versioned artifacts

Maintain an authoritative work view, attributable history of material events and
decisions, and exact artifact versions. Keep corrections traceable and state
consistent with history. Retrieve relevant context from these records; protect
sensitive data rather than logging everything.

### C13. Control change without freezing learning

Record authorized scope, criteria, design, and role-contract changes and their
affected work. Reissue assignments and invalidate affected evidence when needed;
do not silently rewrite active obligations. Distinguish defects from new
requests and preserve the versions behind earlier decisions.

### C14. Recover deliberately; retries can have consequences

Preserve ownership and assignment identity, reject stale updates, and resume
from durable evidence. Reconcile uncertain external effects before retrying. Use
idempotency, isolation, rollback, or compensation as appropriate; a journal
alone does not make remote actions transactional.

### C15. Own the delivery and operational boundary

Assign relevant packaging, installation, migration, release, documentation,
handover, support, and recovery obligations. A PoC need not operate a production
service, but still needs a clear handoff and limitations. Client acceptance does
not itself authorize deployment or external publication.

### C16. Audit every finished delivery/workflow run

Include successful, failed, and cancelled runs. Identify successes, gaps,
bottlenecks, and improvements. Keep reports and GM dispositions visible, and
missing audits outstanding. Audit-only activity does not recursively require
another audit.

### C17. Improve through controlled, reversible learning

The GM can refine agents, introduce justified roles, and delegate role design.
Record expected benefit, affected versions and assignments, outcome evidence,
and a revert path; review whether added complexity remains useful. Evaluate
material changes against an appropriate baseline without a large benchmark
program for every small correction. Efficiency proxies alone are not success.

## Separate collaboration policy

The existing P6 collaboration policy remains in the README: recommend execution
placement, obtain the Client's choice at meaningful work boundaries unless
already selected, and keep the parent session responsible for delegated results.
It is not an eighteenth governing principle or a runtime requirement for human
approval before every internal handoff.

## Adoption boundaries and legacy mapping

Adoption does not select infrastructure, approve a runtime or trial, set numeric
budgets, or accept the entire workflow draft. In particular:

- H1: roles remain distinct responsibilities, not a fixed agent-instance
  topology. C11 establishes a separate-context verification default; detailed
  exception policies remain to be defined.
- H2: C08 replaces undifferentiated BA/GM criteria ownership with differentiated
  responsibilities. Detailed conflict and approval procedures remain open.
- H3: a separate manager-first internal demo remains an optional workflow
  hypothesis, not a mandatory charter gate.
- R1: the operating-envelope requirement is adopted in C07; concrete limits
  remain engagement/policy decisions.
- R4: evaluation and reversibility are adopted in C17; concrete metrics and
  methods remain proportionate policy decisions.

For older research and design records:

- P1/P2 map to C02.
- P3 maps to C03, C07, and C10.
- P4/P8 map to C04; specialization is also preserved in C06.
- P5 maps to C16/C17.
- P6 remains the separate collaboration policy.
- P7 maps to C08-C11.
- P9 maps to C06.
- P12 maps to C01, C05, C07, C11, and C17.
- P13 maps to C12.
- Retired P10/P11 became H2/H3; their later disposition is recorded above.
