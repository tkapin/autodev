# Principles review: consolidated recommendation

**Adoption note, 2026-09-21:** The Client accepted the 17-principle set as an
initial charter, with a preference for future consolidation into fewer,
stronger principles. The authoritative version is now
[principles.md](../principles.md). The review narrative below preserves the
pre-adoption assessment and proposal status; it does not override that charter.

## Status and method

Four models independently reviewed the same AutoDev principles, roles, and
workflow draft on 2026-09-20:

- [GPT-6 Astra](principles-gpt-6-astra.md)
- [GPT-5.5](principles-gpt-5.5.md)
- [Grok 4.6](principles-grok-4.6.md)
- [Claude Opus 5](principles-claude-opus-5.md), explicitly authorized by the
  owner for this review only.

The parent coordinator reviewed their findings and assembled the proposed
17-principle charter below. This is not a vote, independent empirical
validation, or a claim that these are objectively the best models. Shared
training and sources can produce correlated agreement.

Existing approved P principles remain authoritative. The C identifiers below are
proposed replacement-charter identifiers, not adopted renumbering. H1-H3 and
R1/R4 are not approved by this review.

Three reviewers reported limited primary-source checks; Opus explicitly used
general knowledge without fetching sources. No factory, benchmark, or software
trial was run.

## Verdict

The foundation is coherent and broadly aligned with established engineering
practice. Its distinctive strengths are explicit intent, evidence over
self-assessment, one accountable GM without a communication bottleneck,
specialized handoffs, durable project records, and mandatory run-level audits.

The main imbalance is that organizational coordination is better specified than
the actual engineering and delivery guarantees. The reviews repeatedly identify:

- Autonomy without approved stopping and permission rules.
- Specifications without an explicit small-increment feedback rule.
- Completion evidence without sufficiently explicit reproducibility,
  integration, and regression requirements.
- Quality and acceptance without settled decision rights or quality attributes.
- Process self-modification without sufficiently explicit evaluation and
  rollback rules.
- Delivery without a clear boundary for packaging, release, handover, and
  operational responsibility.

These are mostly missing commitments or consciously open decisions, not proof
that accepted principles contradict one another. In particular, P8/P9 can
coexist: specialization is required, but unnecessary agent instances are not. GM
accountability can coexist with auditable peer communication and independent
findings.

## Relationship to established practice

**Agile:** living specifications, short feedback loops, changing requirements,
technical excellence, and simplicity are compatible. Exhaustive upfront
specification or document production as the measure of progress is not.
AutoDev's GM-mediated communication differs from direct business/developer
interaction; it must preserve timely, accurate feedback rather than claim to
copy agile ceremonies.

**SOLID and separation of concerns:** use cohesive responsibilities, narrow
interfaces, clear contracts, and appropriate dependency boundaries in software.
SOLID is not evidence for a fixed organization chart or one agent per
responsibility. Follow target-project engineering standards and apply these
ideas where they improve the design.

**KISS, YAGNI, and DRY:** prefer the simplest adequate design and defer
speculative capability. Consolidate authoritative knowledge, but do not create
premature abstractions merely to remove small duplication. Independent
verification is not wasteful duplication just because another agent wrote tests.

**Continuous integration and delivery:** verify the assembled result, not just
individual agent outputs. Builds, tests, and relevant regression evidence must
be reproducible and tied to the delivered versions. No particular vendor,
branching strategy, or deployment platform follows from that principle.

**Inspect and adapt:** audits only help when findings lead to considered action.
Evaluate changes by client outcomes and engineering quality alongside cost and
speed. Do not substitute an activity counter or a mandatory ceremony for
improvement.

Primary references linked and discussed in the reviewer reports:

- [Agile principles](https://agilemanifesto.org/principles.html)
- [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)
- [YAGNI](https://martinfowler.com/bliki/Yagni.html)
- [Single Responsibility Principle](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html)
- [Scrum Guide](https://scrumguides.org/scrum-guide.html)
- [SRE: Embracing Risk](https://sre.google/sre-book/embracing-risk/)
- [SRE: Release Engineering](https://sre.google/sre-book/release-engineering/)

These references support engineering concepts, not the efficacy of AutoDev's
proposed multi-agent architecture.

## Recommended charter: 17 principles

### C01. Deliver Client value, not factory activity

The GM optimizes for useful, accepted outcomes and engineering quality, not
agents launched, documents produced, token savings, or apparent busyness. Make
quality, cost, and time tradeoffs explicit within agreed constraints.

Trace: elevates P12's existing outcome focus.

### C02. Make intent, assumptions, and uncertainty explicit

Maintain living, versioned requirements, constraints, non-goals, and acceptance
expectations. Resolve material unknowns with the authorized decision-maker;
record lesser assumptions and their consequences. Conversation is input to the
specification, not an invisible alternative source of authority.

Trace: consolidates P1/P2; materiality guidance is a proposed refinement.

### C03. Deliver and learn in small, verifiable increments

Specify enough for the next valuable slice, integrate it, obtain feedback, and
adjust. Use proportionate discovery for unresolved uncertainty instead of
exhaustive prediction. Failed or cancelled attempts remain honest outcomes; this
is not a guarantee that every run produces working software.

Trace: extends P3 with an explicit incremental-delivery commitment.

### C04. Choose the simplest adequate engineering and organization

Prefer maintainable solutions and existing capabilities. Apply separation of
concerns and target-project standards proportionately. Add abstractions,
infrastructure, roles, or handoffs only when their benefit justifies their
complexity. Simplicity is not permission to omit required quality checks.

Trace: consolidates P4/P8.

### C05. Keep one accountable GM and explicit delegated authority

The GM owns commitments, principle compliance, coordination, and the overall
result. All internal roles report to it, but auditable peer handoffs are
allowed. Preserve the Client-facing model, authorized BA clarification, and
Client-commissioned audits. Delegating execution never transfers accountability.

Trace: retains P12 and the accepted communication exceptions.

### C06. Specialize through clear contracts and sufficient focused context

Every assignment identifies its purpose, relevant input and contract versions,
authority, outputs, evidence, and escalation conditions. Use curated context and
durable handoffs rather than full-history copying or context-free prompts. A
role is a responsibility contract, not necessarily a persistent agent.

Trace: retains P9 and the role/instance distinction.

### C07. Bound autonomy by authority, resources, risk, and progress

Establish permitted actions, access, resource limits, stopping conditions, and
escalation before execution. Honor cancellation and stop unproductive loops
without lowering the criteria. External or irreversible effects require
appropriate authorization; creating a role does not expand permissions.

Trace: proposes R1 adoption, extending existing P12 authority restrictions.

### C08. Define done and who can decide it

Separate business acceptance criteria from proportionate engineering obligations
and an explicit delivery boundary. BA develops business clarity; technical
specialists contribute engineering requirements and evidence; GM ensures
coherence; the Client retains acceptance authority. Verified, accepted,
released, unsuccessful, and audit-pending are distinct outcomes.

Trace: strengthens P7; proposes resolving H2 with differentiated
responsibilities, not undifferentiated BA/GM ownership of all quality decisions.

### C09. Treat relevant quality attributes as requirements

Explicitly identify applicable maintainability, security, privacy, reliability,
accessibility, performance, and compatibility expectations. Scope their evidence
to the actual product and risk, and make exclusions or accepted limitations
visible. Avoid both silent omission and an indiscriminate compliance checklist.

Trace: proposed addition extending P4/P7.

### C10. Verify the integrated result and protect existing behavior

Use repeatable build, test, regression, and failure-path evidence appropriate to
the change. Record inputs, environment, commands, and delivered versions so
another actor can reproduce the result. Separate passing evidence from missing,
flaky, or failed checks. Passing isolated tasks does not establish integration.

Trace: strengthens P7; does not mandate a particular CI service or coverage
score.

### C11. Preserve independent challenge, findings, and uncertainty

Do not call self-approval or a persona switch independent verification. Record
the separation actually used and preserve review, test, and audit findings even
when the GM disagrees. Give material unresolved disputes an escalation path;
management cannot make negative evidence disappear.

Trace: strengthens P7/P12. The recommended default is a separate verification
context for software changes; exact exceptions and stricter risk-based
requirements remain an explicit H1 policy decision.

### C12. Keep current state, an append-only journal, and versioned artifacts

Maintain an authoritative view of work, an attributable history of material
events and decisions, and exact artifact versions. Corrections remain traceable;
state and history must not silently diverge. Supply relevant context from these
records and protect sensitive data rather than logging everything.

Trace: retains P13; data-handling and consistency wording extends its
safeguards.

### C13. Control change without freezing learning

Record authorized scope, criteria, design, or role-contract changes and their
affected work. Reissue assignments and invalidate affected evidence when needed;
do not rewrite active obligations silently. Distinguish defects from new
requests and retain the versions underlying prior decisions.

Trace: proposes elevating change rules from the workflow draft.

### C14. Recover deliberately and treat retries as potentially consequential

Preserve ownership and assignment identity, reject stale updates, and resume
from durable evidence. Reconcile uncertain external effects before retrying; use
idempotency, isolation, rollback, or compensation as appropriate. A journal
alone does not make remote actions transactional.

Trace: proposes elevating workflow recovery rules and extending them to effects.

### C15. Own the delivery and operational boundary

Define who owns relevant packaging, installation, migration, release,
documentation, handover, support, and recovery obligations. A PoC need not
operate a production service; it still needs a clear handoff and limitations.
Client acceptance does not itself authorize deployment or external publication.

Trace: proposed addition consistent with the existing production-access
boundary.

### C16. Audit every finished delivery/workflow run

Include successful, failed, and cancelled runs. Identify what worked, gaps,
bottlenecks, and improvement opportunities. Keep the report and GM dispositions
visible in the shared record, and keep missing audits outstanding. Audit-only
activity does not recursively require another audit.

Trace: retains the accepted mandatory-audit part of P5.

### C17. Improve agents and workflows through controlled, reversible learning

The GM can refine agents, introduce justified roles, or delegate role design.
Record expected benefit, affected versions and assignments, outcome evidence,
and a revert path; review whether added complexity remains useful. Evaluate
material changes against an appropriate baseline without requiring a large
benchmark program for every small correction.

Trace: retains GM evolution authority and proposes R4's evaluation/rollback
discipline. Efficiency proxies alone do not demonstrate improvement.

## Separate collaboration rule

Keep P6 as a development-time collaboration policy, not an eighteenth runtime
principle: recommend placement, obtain the owner's choice at meaningful work
boundaries unless already selected, and keep the parent session responsible for
presenting delegated results. Do not impose a human prompt on every runtime
handoff.

## Disagreements and coordinator judgment

**Review independence:** Grok and Opus favor mandatory different-context
verification. Astra favors stronger separation where risk warrants it.
Recommendation: make independent verification the default for software changes,
record actual separation, and settle proportional exceptions explicitly.
Different contexts reduce shared assumptions but do not prove independent
judgment.

**New-role creation:** Opus proposes requiring a demonstrated failure that
existing roles could not absorb. That is unnecessarily restrictive: an upcoming
known need can justify a specialist before failure occurs. Prefer documented
need, alternatives considered, expected benefit, and subsequent audit of whether
the role helped. Preserve the GM's accepted authority.

**Manager-first demo:** do not add H3 as a mandatory governing principle. GM
accountability already requires integrating results and communicating evidence;
a separate internal demonstration is a workflow option to evaluate. GPT-5.5
includes it conditionally in its candidate charter; this synthesis keeps that
detail outside the governing set.

**Post-acceptance operations:** do not globally declare operations in scope or
out of scope. Require an explicit delivery boundary per engagement and the
necessary authority for whatever is included.

**What not to add:** one principle per acronym; mandatory Scrum ceremonies;
fixed role counts; a broker/database choice; numeric budgets or coverage
thresholds in the charter; exhaustive upfront specs; or unbounded perfection.

## Decisions required before adoption

This document is a review result, not a changed operating charter. The owner
should review the proposed set, especially:

- C07: adopt the existence of an operating envelope while leaving values open.
- C08/C11: settle criteria authority and the independent-verification default.
- C17: establish minimum evaluation and rollback obligations for GM-led changes.

If adopted, update the authoritative principles and dependent role/workflow
documents together, preserve the old-to-new mapping, and identify any approved
exceptions. Do not infer approval from agreement among models.
