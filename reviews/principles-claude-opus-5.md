# Independent principles review — Claude Opus 5

Scope: `README.md`, `roles.md`, `workflow-and-coordination.md` as of 2026-09-20.
Everything below is a proposal for the owner to accept or reject; nothing here
promotes a recommendation to a decision. No external sources were fetched in
this session; all attributions are paraphrased from general knowledge and are
**unverified in-session**. No scores are given, because no agreed rubric exists.

## Verdict

The set is unusually coherent for its stage. It is strongest exactly where
agentic systems usually fail: intent is durable rather than conversational (P1),
completion needs observable evidence rather than an agent's assertion (P7),
accountability has one named owner (P12), and history is append-only and
versioned (P13). The mandatory run-level audit, including failed and cancelled
runs, is the best idea in the document; it is the analogue of a blameless
postmortem and of Scrum's retrospective, and it converts a demo-ware loop into a
system that can improve.

The weakness is symmetrical: the charter governs _how work is described,
assigned and recorded_ far better than _how software actually gets safely built
and stopped_. Four things a delivery factory cannot run without are absent or
still non-binding: a bounded-autonomy safety core, an increment small enough to
be verified early, a re-runnable regression net, and an authority limit on
irreversible side effects. P3 mandates autonomous iteration while the only stop
rule (R1) remains a recommendation — the set currently obliges the system to run
and does not oblige it to halt.

Keep, unchanged in substance: P1, P7, P12, P13, the mandatory audit half of P5,
and P6's status as a collaboration rule that must never leak into the runtime
charter.

## Prioritized gaps and tensions

**1. P3 without R1 — autonomy with no binding stop.** Failure: an implementation
item repeatedly fails verification; each iteration produces a plausible patch
and a new rationale; the run consumes budget until a human notices, and no rule
was violated. Smallest fix: promote a minimal core of R1 to requirement now —
declared authority scope, a resource ceiling per run, a no-progress detector,
and escalate-rather-than-exceed — leaving all numbers open. Budget _values_ are
a decision; the _existence_ of a limit is not process machinery under P4.

**2. No irreversible-effect boundary.** Scope prose excludes "deploying
production software without explicit authority", but no principle constrains a
Developer or Tester agent's side effects. Failure: a verification step runs a
destructive command, mutates a shared branch, publishes a package, or calls a
paid external service, and the journal records it only afterwards. Smallest fix:
one least-authority principle — agents receive the narrowest tool and data
access their contract needs; effects outside the work item's declared boundary
require recorded authorization. This is an operational-safety rule, not a
security audit.

**3. No thin-increment rule (P1/P2 batch risk).** Failure: BA and GM iterate a
specification to "ready", the run implements it whole, and the first executable
evidence arrives at step 6 — where a wrong assumption invalidates the batch.
This is the classic large-batch failure the Agile Manifesto's "working software"
value and Scrum's Increment were formulated against (_unverified attribution_).
Smallest fix: require each delivery run to produce at least one end-to-end
verifiable slice, and allow specification readiness to be judged per slice.

**4. P7 does not require verification to be repeatable or regression-safe.**
Failure: iteration 3 passes a check that was performed ad hoc; iteration 6
breaks behavior accepted in iteration 2, and nobody can re-run the earlier
evidence. Self-testing code and continuous integration (Fowler/Martin;
_unverified_) exist precisely for this. Smallest fix: extend P7 — evidence must
be reproducible by a different agent from recorded commands and inputs, and
previously accepted behavior must be re-verified before a run is declared
finished.

**5. Independence of review is procedural, not principled.** `workflow` §6 warns
that "one instance changing personas is not evidence of independent review", but
no principle carries it; H1 could later merge Developer and Reviewer for
economy. Failure: an agreeing persona reviews its own output and the audit
records a clean run. Smallest fix: make independence a principle — verification
evidence must come from a context that did not author the change, and the
separation actually used must be recorded on the item.

**6. Improvement loop can be gamed (P5 + R4).** `roles.md` warns that speed or
agent count alone do not prove improvement, but with the Auditor feeding the GM
that also owns efficiency, the measurable proxies (iterations, runtime, tokens)
will dominate. Goodhart's law and DORA's insistence on pairing throughput with
change-failure rate are the standard counterweights (_unverified_). Smallest
fix: adopted process changes must be justified by delivery-outcome evidence,
never by efficiency proxies alone.

**7. No rollback for self-improvement.** P13 versions artifacts; nothing
requires an adopted prompt or role change to be revertible or attributable to
the runs it affected. Failure: an audit-driven instruction change quietly
degrades quality across later runs and cannot be isolated. Smallest fix: every
adopted change records its version, the runs it first applies to, and how to
revert it.

**8. Role proliferation has no gate.** P4/P8 argue for smallness, yet `roles.md`
grants role creation, role design delegation, a Role Designer and an Agent
Behavior Analyst. Nothing requires evidence that an existing role failed first.
Failure: an org chart grows one specialist per observed defect. Smallest fix: a
new role requires a recorded failure existing roles could not absorb, plus
review for retirement at the next audit. This is a tension, not a contradiction.

**9. Delivery boundary and ownership after acceptance are undefined.** Roles
stop at Tester and Client acceptance. Nobody owns build/release reproducibility
or post-acceptance defect intake. Smallest fix: define done as a
Client-accepted, reproducibly buildable artifact with handover notes, and state
explicitly that operations is out of scope — rather than leaving it unstated.

**10. Quality attributes are only implied by P4.** Simplicity is not
maintainability; a Reviewer has no charter clause to cite when rejecting code
that passes tests but is unworkable. Smallest fix: acceptance criteria must name
the quality attributes that matter for that work item, and no more (YAGNI
applies to non-functional requirements too).

**11. Materiality threshold for P2 is missing.** P2 says ask rather than
silently decide; P3 says do not require a person per step. Both are right; the
boundary is unset, so the system will either invent silently or spam the Client.
This, plus the open definition of completion, is the highest-value open
decision. Consciously unresolved and correctly flagged, not contradictions: H1
agent mapping, H2 criteria ownership, H3 demo gate, storage and transport
choices.

## Alignment with established practice

Sound and well-mapped: spec-as-memory (P1); retrospective and inspect-and-adapt
(P5, Scrum); traceable history and blameless post-incident review (P13, Google
SRE); single accountable owner with decentralized communication (P12); explicit
handoff contracts (P9) — which is the one genuinely transferable idea from
interface design. All _unverified in-session_.

Caveat on SOLID: it governs code modules, not organizations. Reading SRP as "one
responsibility per agent" would license exactly the sprawl P8 resists. The
defensible transfers are narrow — the handoff is an interface, give an agent
only the context it needs, and depend on a _contract version_ rather than on a
particular agent instance (`workflow` already does this). Do not put SOLID in
the charter; require instead that code-level standards are inherited from the
target project. Caveat on agile: "working software over comprehensive
documentation" sits in tension with a document-heavy charter. The tension is
justified here — specifications are the agents' only durable memory — but the
failure mode is treating specification completeness as progress, which gap 3
addresses.

## Proposed coherent set (16)

Runtime charter. P6 stays deliberately outside it as a collaboration rule.

1. **Intent lives in the specification.** Any requirement acted on must exist in
   a versioned specification; conversation is not a source of truth. _(P1)_
2. **Clarify what is material; record what is assumed.** Escalate unknowns that
   change scope, criteria, or authority; decide the rest and record the
   assumption on the item. _(P2 + new threshold)_
3. **Deliver in thin verifiable increments.** Each run yields at least one
   end-to-end slice that can be demonstrated and verified. _(new)_
4. **Evidence-based completion.** Completion requires observable evidence
   reproducible from recorded commands by another agent. _(P7 + new)_
5. **Independent verification.** Verification comes from a context that did not
   author the change; record the separation used. _(new; split from P7, H1)_
6. **Protect accepted behavior.** Re-verify previously accepted behavior before
   declaring a run finished; regressions block completion. _(new)_
7. **Fit-for-purpose quality.** Simplest design meeting stated criteria; name
   the quality attributes that matter and no others. _(P4 + new)_
8. **Bounded autonomy.** Iterate without step-by-step direction, within declared
   authority, resource ceilings, and no-progress stop rules; escalate rather
   than exceed. _(P3 + R1 core)_
9. **Least authority, explicit for irreversible effects.** Narrowest access per
   contract; effects outside the item's boundary need recorded authorization.
   _(new)_
10. **One accountable General Manager.** Sole Client contact and accountable
    lead; summaries preserve failures, limits, and uncertainty. _(P12)_
11. **Smallest structure preserving specialization.** New roles require recorded
    evidence that existing roles could not absorb the need, and are reviewed for
    retirement. _(P8 + `roles.md` gate)_
12. **Self-sufficient handoffs.** A handoff names spec, design, contract
    versions, inputs, expected outputs, evidence, and stop condition. _(P9)_
13. **State, journal, versioned artifacts.** Current state, append-only history,
    versioned artifacts; corrections never overwrite history. _(P13)_
14. **Consistent and resumable execution.** State change and its journal event
    commit as one logical operation; a restart rediscovers ready work, open
    questions, and pending audits. _(elevated from `workflow`)_
15. **Every finished run is audited.** Including failed and cancelled runs;
    findings stay visible, the GM records disposition, audits do not recurse.
    _(P5 audit half)_
16. **Process changes are versioned, outcome-evaluated, revertible.** Justified
    by delivery outcomes, not efficiency proxies; each change names its revert
    path. _(P5 improvement half + R4)_

## Top three owner decisions

1. Promote the minimal bounded-autonomy core (principle 8) from R1 to a
   requirement now, with values left open. Nothing else should be implemented
   first.
2. Define run completion: the increment, the verification set, and the
   materiality threshold of principle 2. This closes the acknowledged gap in
   P3/P7 and gives H2 something concrete to allocate.
3. Decide the delivery boundary — reproducible artifact plus handover, or an
   explicit out-of-scope declaration for release and operations.

## What not to add

No SOLID clause; no separate principle per maxim (DRY, KISS, YAGNI belong inside
principle 7); no obligation to run every role on every task; no broker,
database, or evaluation platform mandated by a principle; no numeric agent
scoring; no audit of audits; and no runtime rule requiring human approval per
delegation — that is P6's collaboration scope only.
