# AutoDev principles review -- independent GPT-5.5 reviewer

## Verdict and strengths

The current principles are strong for this design stage. They correctly treat
AutoDev as a software delivery organization, not a single coding prompt. The
best parts are P1/P2 specification readiness, P7 evidence over assertion, P8/P9
specialized but minimal roles, P12 single accountable GM, and P13 recoverable
state. Those are practical governing ideas a GM can use when deciding whether to
ask for clarification, split work, accept a result, reroute a blocker, or change
the process.

The main weakness is not excess ceremony; it is that several delivery-critical
values are still implicit. Tests, CI, release/operability responsibility,
bounded autonomy, criteria ownership, and process-change rollback are present as
hints or open decisions, but not yet first-class governing principles. That
creates avoidable room for a future GM to optimize for visible progress, agent
activity, or elegant workflow artifacts instead of valuable, maintainable,
shippable software.

## Prioritized gaps and tensions

1. **P7 lacks a full definition of done.** Failure scenario: a Developer
   supplies tests and a Reviewer passes maintainability, but no one confirms the
   build, regression risk, deployment note, or user-facing acceptance evidence.
   Minimal remedy: make "done" require agreed acceptance evidence, relevant
   automated checks, regression consideration, known limitations, and release or
   handoff readiness.

2. **H2 criteria ownership is still unresolved.** Failure scenario: BA writes
   business criteria, Architect adds quality constraints, Tester verifies only
   visible behavior, and the GM presents a package that satisfies none of them
   coherently. Minimal remedy: make the GM accountable for criteria coherence,
   the BA responsible for business intent, technical specialists responsible for
   technical sufficiency, and the Client the acceptance authority.

3. **R1 should become a runtime principle, not remain optional.** Failure
   scenario: the loop keeps spawning rework, audits, and clarification tasks
   because each step is locally justified. Minimal remedy: require explicit
   authority, budgets, stop conditions, escalation triggers, and permission
   boundaries for every run.

4. **P5/R4 process improvement needs rollback governance.** Failure scenario:
   the GM changes prompts or role contracts after one bad run and silently
   worsens the next three. Minimal remedy: version process changes, state the
   expected improvement, compare with a relevant baseline when material, and
   keep a rollback path.

5. **P4/P8 tension needs an operating test.** Failure scenario: "specialized
   agents" becomes a default role parade, or "simplicity" collapses independent
   review into implementer self-approval. Minimal remedy: require each role or
   handoff to preserve a distinct decision right, independence need, or context
   benefit; otherwise merge it.

6. **Production and operability are missing values.** Failure scenario: a run
   delivers code that passes local tests but lacks migration notes,
   configuration, observability, rollback, or operational ownership. Minimal
   remedy: add a principle that delivery includes safe release/operation
   considerations proportionate to the task.

7. **Client value can be obscured by proxy metrics.** Failure scenario:
   throughput, fewer agents, token cost, or audit closure is reported as success
   while the Client's problem remains partly unsolved. Minimal remedy: make
   Client value and accepted outcomes the primary progress measure, with proxy
   metrics explicitly secondary.

8. **H3 manager-first demo should remain conditional.** Failure scenario: the GM
   demo becomes an approval theater that duplicates Reviewer/Tester work.
   Minimal remedy: adopt it only as an integration-readiness gate for material
   deliveries, and evaluate whether it catches packaging, evidence, or
   expectation gaps.

These are omissions or open decisions, not flaws in the accepted roles. Storage
technology, exact topology, and concrete budgets were consciously left open and
should stay open until the first executable loop needs them.

## Alignment with established practices and caveats/sources

P1/P2 align with specification by example and agile backlog refinement, but they
must not become waterfall freeze. The Agile Manifesto principles explicitly
welcome changing requirements and favor frequent delivery of valuable software,
while also valuing technical excellence and simplicity
(<https://agilemanifesto.org/principles.html>). AutoDev should therefore treat
readiness as "enough shared intent to proceed safely," not "all future learning
forbidden."

P4 and P8 align with KISS/YAGNI and the Agile principle that simplicity is "the
art of maximizing the amount of work not done." Caveat: DRY and reuse are not
always simplicity. In agent workflows, premature abstraction can hide
responsibility and make failures harder to audit. Prefer duplication of small
clear role contracts over a clever generic role when independence matters.

P7/P13 align with CI and traceability. Fowler's CI article emphasizes versioned
mainline, automated builds, and reproducible build/run capability
(<https://martinfowler.com/articles/continuousIntegration.html>). AutoDev's
versioned artifacts and journal are compatible with this, but the principle set
should explicitly require the checks and reproducibility evidence that make
"verified software" credible.

P5 aligns with Scrum's transparency, inspection, and adaptation pillars; the
Scrum Guide also warns that inspection without adaptation is pointless
(<https://scrumguides.org/scrum-guide.html>). Caveat: AutoDev should not import
Scrum ceremonies wholesale. The useful lesson is empirical adaptation with
visible artifacts, not a prescribed sprint process.

SOLID maps only partially. Single responsibility supports role contracts and
separation of concerns; dependency inversion suggests specialists should depend
on stable specs and artifacts rather than private conversation state. But SOLID
is object-design guidance, not an organizational constitution. Use it as a smell
detector, not as a rule generator.

## Proposed coherent set of principles

This set separates the future runtime charter from the current collaboration
policy. P6 should remain a collaboration rule for building AutoDev; it should
not be a runtime permission rule for every future agent action.

### Runtime and framework charter

1. **Explicit Client value first** (new). The GM optimizes for accepted Client
   outcomes and useful software, not agent activity, cost reduction, or process
   neatness as ends in themselves.
2. **Specification is the contract of intent** (retains P1). Requirements,
   constraints, non-goals, and changes live in versioned specs rather than
   private chat memory.
3. **Clarify material ambiguity before implementation** (retains P2). Unknowns
   that affect scope, criteria, authority, or risk become questions,
   assumptions, or change decisions.
4. **Iterate on evidence, not hope** (merges P3/P7). Rework targets observed
   gaps, failed checks, or changed intent; repeated prompting without new
   information is not progress.
5. **Definition of done is explicit and proportionate** (new from P7 gap). Done
   means accepted criteria, relevant tests/checks, regression consideration,
   limitations, and release/handoff evidence appropriate to the work.
6. **Simplicity is a quality attribute** (retains P4). Choose the simplest
   adequate design, workflow, and artifact set; avoid speculative mechanisms
   unless evidence justifies them.
7. **Smallest useful specialization** (merges P8/P9). Use distinct roles or
   agents only when they preserve expertise, independence, context isolation, or
   throughput that a simpler structure cannot.
8. **Explicit auditable handoffs** (retains P9). Every handoff carries the
   relevant spec version, decisions, constraints, expected output, evidence, and
   authority.
9. **Single accountable GM** (retains P12). The GM owns workflow, internal
   coordination, principle compliance, integrated delivery, and Client
   communication while delegating detailed work.
10. **Criteria have accountable ownership** (promotes H2 with modification). BA
    owns business clarity, specialists own technical sufficiency, Tester and
    Reviewer own independent evidence, GM owns coherence, and Client owns
    acceptance.
11. **Independent evidence cannot be suppressed** (strengthens P7/P12). Reviews,
    tests, audits, blockers, and failed evidence remain visible even when
    inconvenient.
12. **Durable recoverable state** (retains P13). Current state, append-only
    journal, and versioned artifacts are the authoritative basis for restart,
    audit, and dispute resolution.
13. **Bounded autonomy and resources** (promotes R1). Each run has authority,
    tool permissions, budgets, stop rules, retry bounds, and escalation triggers
    before autonomous execution.
14. **Safe delivery and operability** (new). Release, deployment, configuration,
    observability, rollback, and operational notes are considered when relevant;
    "works locally" is not automatically deliverable.
15. **Empirical process improvement with rollback** (merges P5/R4). Process
    changes are versioned, justified by evidence, evaluated proportionately, and
    reversible when they fail.
16. **Integrated presentation before acceptance when valuable** (conditional
    H3). The GM packages result, evidence, limitations, and risks for Client
    acceptance; an internal manager-first demo is used only when it improves
    readiness.

### Current collaboration policy

Retain P6 separately: while humans and AI are designing AutoDev, choose main
session, clean-context subagent, or fresh session deliberately at each work
package boundary. This is a collaboration policy for framework design, not a
runtime charter principle.

## Top 3 owner decisions and what not to add

1. Decide whether to promote bounded autonomy/resource limits from R1 into a
   governing principle before any executable loop.
2. Decide H2's criteria ownership model, especially who can resolve conflicts
   among BA, Architect, Reviewer, Tester, GM, and Client acceptance.
3. Decide whether H3 is a default integration-readiness gate, a situational GM
   practice, or rejected ceremony.

Do not add a heavyweight platform principle, a mandatory Scrum/SOLID doctrine,
or a rule for every programming maxim. Do not freeze the agent topology yet. Do
not make every specialist client-facing. Do not let process audit recurse
forever or become a substitute for delivering valuable software.
