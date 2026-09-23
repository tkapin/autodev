# Independent principles review: GPT-6 Astra

## 1. Verdict and strongest existing commitments

AutoDev has a credible accountability charter, but not yet a complete delivery
charter. Its strongest decisions are explicit intent and uncertainty (P1/P2),
evidence rather than self-certified success (P7), specialization without a fixed
organization chart (P8/P9), accountable but non-bottleneck management (P12), and
traceable state rather than conversational memory (P13). Mandatory run-level
audits, including failed and cancelled runs, make P5 unusually actionable.

The main imbalance is that coordination and organizational evolution are more
developed than delivering, integrating, releasing, and sustaining useful
software. The GM needs stronger rules for choosing **what not to optimize**,
terminating work honestly, and distinguishing technical completion from
operational readiness.

I found no fundamental contradiction among the accepted commitments. Single
business contact versus BA clarification is an explicit exception; P8 versus P9
is a deliberate optimization constraint; managerial accountability versus
visible independent findings is compatible. H1/H2/H3 and R1/R4 are unresolved
decisions, not violated requirements. P6 governs our collaboration, not runtime
delegation.

This review proposes changes only. It does not approve hypotheses,
recommendations, workflow details, or an executable architecture.

## 2. Prioritized concrete gaps and tensions

### First: make autonomous execution governable

- **P3/P12 and pending R1: accountability without a complete operating
  envelope.** A GM can repeatedly request better work, spawn justified-looking
  roles, or stall awaiting unavailable approval. Existing authority restrictions
  are valuable but do not establish stopping behavior. Smallest fix: approve an
  engagement-level envelope covering permitted actions, resources, material-risk
  escalation, progress checks, cancellation, and truthful unsuccessful
  termination. Bound rework without quietly lowering acceptance criteria.
- **P7 and pending H2: quality ownership remains underspecified.** BA and GM
  could agree on a feature demo while omitting compatibility or recovery
  requirements. Smallest fix: Client controls business intent and acceptance; BA
  proposes observable criteria; technical specialists identify engineering
  obligations; GM integrates them and obtains authorized resolution of
  conflicts. Distinguish acceptance criteria from a reusable, proportionate
  definition of done. A change to either must invalidate affected evidence
  rather than merely update a label.

### Next: close the software-delivery loop

- **P1/P2/P3: specification readiness can become an analysis queue.** “Every
  requirement” and completeness checking can encourage exhaustive upfront
  specification despite the workflow's explicit rejection of waterfall. Smallest
  fix: specify the next valuable slice sufficiently; expose assumptions;
  authorize bounded discovery where uncertainty blocks specification; seek early
  working feedback. Record material changes without requiring a change board.
- **P7/P9: local success can conceal integration failure.** Separate specialists
  may pass checks on different revisions while the assembled product regresses.
  Smallest fix: verify the integrated deliverable and record exact artifact,
  environment, and test versions. Automate repeatable build, acceptance, and
  regression checks where useful; cover important failure paths and preserve
  missing or flaky evidence visibly. More test output is not automatically more
  confidence.
- **P7/P12: delivery stops too close to the demo.** An accepted result may lack
  installation instructions, migration handling, support ownership, or safe
  recovery. Smallest fix: explicitly state the delivery boundary and assign
  release/operational responsibility when applicable, including authorization,
  rollout verification, rollback or compensation, and handover. For a library or
  PoC, this may be a reproducible package and documented limitations, not a
  service or an SRE team. Production deployment remains outside default
  authority.

### Then: preserve trust while adapting

- **P5/P12/P13 and pending R4: recorded improvement is not demonstrated
  improvement.** The GM can change agents mid-project and subsequently report
  faster completion on easier work. Versioning preserves provenance but not a
  valid comparison. Smallest fix: propose a benefit, compare representative
  outcomes and costs against a baseline, preserve quality guardrails, and retain
  a rollback path. Prompt/version changes must not silently rewrite active
  obligations. Do not require a large statistical program for a tiny prompt fix.
- **P12 and H1: independence needs practical protection, not another boss.** A
  manager under delivery pressure could repeatedly change the reviewer until a
  favorable verdict appears. Visible findings already forbid suppression;
  strengthen this with recorded reassignment reasons, unresolved-dissent
  visibility, and escalation for material disputes. Distinct contexts help but
  do not prove uncorrelated judgment. Reserve stronger separation for
  consequential claims; every role need not be a separate permanent agent.
- **P13 and pending R1: recovery is broader than restoring work state.** A
  worker can publish externally, crash before journaling, and cause a duplicate
  action on retry. The draft handles stale assignments and internal consistency
  well; it cannot make remote effects atomic by declaration. Smallest fix:
  reconcile uncertain effects before retrying; require idempotency or
  compensation where feasible, isolate concurrent mutation, and surface
  unrecoverable ambiguity. Logs should retain decision evidence, not
  indiscriminately retain secrets or sensitive payloads.

One smaller provenance tension: README delivery phases describe baseline
evaluation imperatively although R4 remains pending. Label that wording as
intended/proposed; do not treat repetition as approval.

## 3. Established practices, with caveats and sources

- **Agile:** explicit specifications are compatible with short feedback loops,
  changing requirements, technical excellence, and simplicity. They cease to be
  agile when readiness means eliminating every uncertainty before learning from
  working software. AutoDev intentionally differs from direct daily
  business/developer interaction; GM mediation should be judged by whether
  clarification remains timely and accurate, not declared equivalent by fiat.
  The [Agile Manifesto principles](https://agilemanifesto.org/principles.html)
  support these observations; their human-team advice is not an agent topology.
- **SOLID and separation of concerns:** use focused responsibilities, narrow
  contracts, substitutability where promised, and isolation of changing
  dependencies as design heuristics. SOLID arose in object-oriented design; its
  class-level prescriptions do not establish the correct number of agents.
  Creating a specialist for every concern can increase coupling through
  handoffs. This is my contextual application, not a verified attribution to a
  particular SOLID author.
- **KISS/YAGNI/DRY:** P4 already captures their useful decision pressure. Avoid
  speculative machinery; consolidate authoritative knowledge, but tolerate small
  code duplication until the abstraction is understood. DRY does not justify
  coupling unrelated workflows or eliminating independent verification. These
  are engineering interpretations, not source-verified quotations.
- **Continuous integration:** frequent integration and reproducible automated
  checks are more valuable than many independently “finished” agent tasks.
  [Fowler's Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html)
  explicitly supports version-controlled build inputs and build automation. Do
  not turn this into a mandatory vendor, branch strategy, or full pipeline for
  every documentation change.
- **Release engineering:** repeatability, intentional release changes, and
  collaboration around deployment and rollback belong in delivery thinking.
  [Google SRE's Release Engineering](https://sre.google/sre-book/release-engineering/)
  supplies concrete examples, not a requirement to copy Google's scale,
  organization, hermetic-build infrastructure, or automatic deployment policy.

The three linked primary sources were fetched directly on 2026-09-20. This is a
bounded design review, not a new literature survey or empirical validation of
AutoDev.

## 4. Proposed coherent charter

**Proposal: 16 governing principles, plus one separate collaboration rule.**
These apply to framework engineering and/or runtime as relevant; they are not
all newly approved requirements. “Retain” describes continuity of intent, not
approval of my revised wording.

1. **Deliver Client value, not factory activity.** Retain P12's outcome focus;
   elevate it into a decision rule. Prefer useful results and reduced
   uncertainty over agents launched, artifacts produced, or apparent busyness.
   Optimize cost and time within agreed quality and scope, not instead of them.
2. **Make intent and material uncertainty explicit.** Merge P1/P2. Maintain
   reviewable requirements, constraints, non-goals, assumptions, and evidence
   expectations. Resolve consequential unknowns with the authorized party;
   distinguish recorded assumptions from accepted requirements.
3. **Learn through small, integrated increments.** Extend P3; new proposal. Plan
   and specify enough for the next useful slice. Use early feedback and bounded
   discovery rather than exhaustive anticipation or endless refinement.
4. **Control change without freezing learning.** Elevate the draft workflow; new
   proposal. Record authorized changes, affected versions and dependencies,
   rework, and evidence invalidation. Separate a defect from a changed request.
5. **Choose the simplest adequate engineering and organization.** Merge P4/P8.
   Reuse existing capabilities, keep responsibilities cohesive, and add
   abstractions or agents only for demonstrated need. Simplicity includes
   understandable maintenance, not merely fewer files or fewer participants.
6. **Keep one accountable GM and explicit delegated authority.** Retain P12. GM
   owns commitments, compliance, outcomes, and Client communication; PM and
   specialists can coordinate internally. Preserve BA clarification and direct
   audit-request exceptions without transferring Client coordination duties.
7. **Specialize through sufficient context and explicit contracts.** Retain P9
   and the role/instance distinction. Every assignment carries relevant inputs,
   authority, expected outputs, and evidence. Choose execution separation under
   H1; do not instantiate the entire glossary automatically.
8. **Bound autonomy by permission, risk, and progress.** Propose R1 adoption.
   Establish limits and escalation before execution; honor cancellation; stop
   unproductive loops. Use least necessary access and proportionate safeguards
   for external, sensitive, costly, or irreversible actions.
9. **Define done before claiming done.** Retain P7; propose resolving H2. Agree
   behavioral acceptance and proportionate engineering obligations. Distinguish
   verified, Client-accepted, released, unsuccessful, and audit-pending
   outcomes. Neither a demo nor a status flag substitutes for evidence.
10. **Verify the integrated product and protect existing behavior.** Extend P7;
    new proposal. Use reproducible build/test evidence, appropriate regression
    and failure-path checks, and independent challenge where risk warrants. Tie
    evidence to the actual delivered version and disclose coverage limits.
11. **Treat maintainability and nonfunctional quality as requirements.** New
    proposal. Identify relevant security, privacy, reliability, accessibility,
    performance, compatibility, and maintainability needs early; explicitly
    scope their verification. Avoid an exhaustive checklist unrelated to the
    product's risks and users.
12. **Preserve independent findings and honest uncertainty.** Consolidate P7/P12
    and the role contract. Findings survive management disagreement; record
    dispositions and escalate unresolved material conflicts. Distinguish missing
    evidence, negative evidence, and accepted residual risk.
13. **Keep durable, consistent, reconstructable work records.** Retain P13.
    Maintain current state, append-only material history, and versioned
    artifacts with attributable decisions. Protect sensitive information;
    preserve correction provenance rather than freezing inaccurate state.
14. **Recover deliberately; never assume a retry is harmless.** Elevate draft
    recovery; new proposal. Detect stale ownership, reject stale mutations,
    reconcile external effects, and resume from durable evidence. Define a next
    responsible actor for blocked work and recovery.
15. **Own the release and operational boundary.** New proposal. Assign the
    applicable packaging, deployment, handover, support, and recovery
    obligations. Deliver reproducibly within explicit authority; Client
    acceptance alone does not authorize production changes.
16. **Audit every finished run; improve through controlled learning.** Retain
    P5; propose R4's evaluation discipline. Include failure/cancellation, keep
    missing audits visible, and avoid recursive audit obligations. Version
    changes, record GM disposition, compare Client outcomes and quality
    alongside cost/latency, and permit rollback. Do not optimize a single easily
    gamed metric.

**Separate collaboration rule C1 — deliberate work placement:** retain P6
unchanged in substance. At meaningful AutoDev development-package boundaries,
recommend placement and obtain the owner's choice unless already explicitly
selected. That approval does not become a runtime requirement before every
delegation.

## 5. Top three owner decisions and what not to add

1. **Approve the operating envelope before execution:** decide R1, including
   authority, resource/progress limits, cancellation, escalation, and release
   boundary. No universal numeric budget is implied.
2. **Set criteria authority and assurance boundaries:** resolve H2; choose
   risk-proportionate independent execution under H1. Evaluate H3 separately: GM
   accountability need not mean an extra theatrical demo gate.
3. **Authorize governed adaptation:** decide R4's minimum comparison and
   rollback expectations, permitted in-flight role changes, and which changes
   require owner approval. Protect audit visibility without requiring adoption
   of every recommendation.

Do not add one principle per famous acronym, a mandatory toolchain, fixed
multi-agent hierarchy, universal production SLOs, percentage-coverage targets,
or approval gates for routine internal handoffs. Do not redefine “best quality”
as limitless polishing: agreed obligations, explicit tradeoffs, and honest
stopping conditions are stronger than an unbounded promise of perfection.
