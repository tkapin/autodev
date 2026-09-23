# AutoDev principles review (Grok 4.6)

Independent critique of `README.md`, `roles.md`, and
`workflow-and-coordination.md`. Recommendations only; not approved decisions. P6
is treated as parent-session collaboration policy, not a runtime rule.

## Verdict

The charter already separates owner requirements, hypotheses, and
recommendations better than most agent-org sketches. Load-bearing pieces are P12
(single GM, internal handoffs allowed), P13 (state / journal / versions), P7
(evidence over assertion), P4/P8 (simplicity and smallest useful
specialization), and run-level audit rather than per-turn audit. The main risk
is an incomplete _runtime_ charter: P3 still aspires to thorough refinement
without a stop rule, R1/R4 are unadopted, H2 would mix product acceptance with
engineering quality, and the Auditor reports to the same GM who is judged by
speed and completion. Do not freeze the workflow draft's state machine as extra
principles.

**Keep:** P1, P2, P4, P7, P8/P9, P12, P13, and P6 only as design-session
placement policy.

## Prioritized gaps and tensions

### 1. Unbounded iteration (P3 vs P4 vs open R1)

P3 wants autonomous meaningful iteration and a "thoroughly refined solution"
while P4 forbids extra machinery and R1 budgets/stop rules are unapproved.

Failure: the factory retries review-fix loops until context collapses, then
either treats activity as success or never finishes. Cancellation still triggers
audit, which recommends more agents.

Smallest fix: promote slim R1 into the runtime charter (authority, retry budget,
escalate-or-stop _before_ a run). Redefine P3 as iterate on evidenced gaps until
criteria or bound is hit. Drop the perfection slogan.

### 2. Audit usefulness vs independence (P5, P12)

Run-level audit including failure/cancellation is the right grain. Audit-only
runs not recursing is correct. Weakness: Auditor reports to GM, findings go to
GM, GM also owns efficiency. Client-commissioned audits still land on GM.

Failure: GM records "reject with reason" on findings that would slow the next
demo; there is no Client-visible unresolved-audit queue; later runs look better
because criteria were narrowed.

Smallest fix: GM remains action owner. Audit reports and dispositions live in
the Client-visible triad. GM cannot complete an audit by assertion or hide
findings. Do not make the Auditor a second Client or a peer manager.

### 3. Criteria ownership (H2, P2, P7)

H2 is not approved and should not become default. Joint BA+GM ownership of
acceptance criteria _and_ quality metrics conflates product intent with
engineering fitness.

Failure: BA writes demo-able AC that omit regression and maintainability; GM
"owns quality" by accepting a package that matches the written AC and silently
drops NFRs.

Smallest fix: Client (via GM/BA) owns product acceptance; Reviewer/Tester own
engineering checks against agreed standards; GM escalates conflicts rather than
merging them silently. Leave H3 optional.

### 4. Role-play is not independence (P8, P9, H1)

The workflow draft already warns that one instance changing personas is not
independent review. Principles do not require a decision. H1 mapping may still
combine roles.

Failure: one session plays Developer, then Reviewer, then Tester; P7 looks
satisfied; defects ship.

Smallest fix: verification of a work item requires a different execution context
than the implementer. Combining BA+PM in one instance can be allowed; combining
implementer+verifier cannot.

### 5. Process change without rollback (P5, P12, R4)

GM may add roles and rewrite agent definitions. R4 evaluation is unapproved.
Sunset/revert of process changes is missing.

Failure: under pressure GM adds Role Designer and "Psychologist"; contracts
change mid-run; nobody can tell whether quality moved.

Smallest fix: process/role changes are versioned (P13), apply to new assignments
only, and carry a recorded revert path. Do not wait for a full
comparative-evaluation program.

### 6. Delivery treated as production (scope vs P7)

Scope already excludes production deploy without authority, but no principle
states it.

Failure: a "verified" package is treated as released, or the PoC is scored on
production DORA metrics before it has a host.

Smallest fix: finished delivery ≠ deploy/operate authority.

### 7. Activity and metric gaming (P7, P12)

P7 forbids weakening criteria to declare done. P12 also pursues efficiency.

Failure: more verified items, shorter cycles, extra roles, high "findings
adopted" counts — Client ask still unmet.

Smallest fix: Client outcome and verification evidence beat activity counts.

### 8. Spec theater vs evolving intent (P1)

"Every requirement as a specification" can become an SRS waterfall. The workflow
already says readiness is not a freeze.

Failure: implementation blocked on exhaustive docs, or draft questions labeled
as spec and coded.

Smallest fix: capture _material_ intent, constraints, and evidence expectations;
change is a versioned decision.

Not treated as contradictions: open H1 instance mapping, unapproved H3, retired
P10/P11 identifiers, storage/runtime choices.

## Alignment with established practice

- **Agile Manifesto** values working software and responding to change over
  comprehensive documentation and following a plan
  ([agilemanifesto.org](https://agilemanifesto.org/)). P1 is compatible if specs
  are living versions, not a freeze. P3's refinement aspiration fights "working
  software is the primary measure of progress"
  ([principles](https://agilemanifesto.org/principles.html)). Those principles
  also welcome late change, treat simplicity as maximizing work not done,
  require technical excellence, and reflect/tune at intervals. P4 and run-level
  P5 map; P1 maps only if change stays first-class.
- **YAGNI** (Fowler, XP simple/incremental design): do not build presumptive
  capability now; it incurs build, delay, and carry cost
  ([Yagni](https://martinfowler.com/bliki/Yagni.html)). Apply to process
  machinery as well as code. Assignment-revision semantics in the workflow draft
  are useful; promoting every transition into a principle is not.
- **SOLID:** Martin's SRP is a _module_ with one reason to change / one
  stakeholder
  ([SRP, 2014](https://blog.cleancoder.com/uncle-bob/2014/05/08/SingleReponsibilityPrinciple.html)).
  Useful analogy for role _contracts_ (BA, Developer, Reviewer answer different
  authorities). OCP/LSP/ISP/DIP are object-design rules. They do not prove a
  human org chart. Do not put SOLID in the factory charter.
- **Separation of concerns:** keep product acceptance, implementation,
  independent check, and process audit distinct even when some roles share an
  instance. DRY the artifacts (one spec version), not the agents (one
  omni-prompt).
- **Google SRE:** reliable enough, not maximally reliable; explicit risk
  tolerance ([Embracing Risk](https://sre.google/sre-book/embracing-risk/)).
  Analog: done means agreed criteria plus bounds, not thorough perfection.
- **DORA:** current guide lists five software-delivery metrics, treats speed and
  stability as compatible, and warns against setting metrics as a goal
  ([DORA metrics](https://dora.dev/guides/dora-metrics/)). Useful later for
  production delivery; premature as AutoDev PoC gates. Unverified here: older
  "four keys" summaries still circulating.

KISS is folk overlap with P4; no separate primary source cited.

## Proposed runtime charter (16)

P6 stays **collaboration policy** for the parent design session: recommend main
vs subagent vs fresh session, ask the human, wait. It does not require human
approval of every internal factory handoff.

1. **Versioned intent** (P1, tightened) — Act on the current specification
   version. Chat is not the contract.
2. **No silent business decisions** (P2) — Material unknowns become questions or
   recorded assumptions with GM/Client authority, not code.
3. **Change is a decision** (new; agile change + P13) — Scope or criteria
   changes produce a new spec version and retarget work.
4. **Iterate on evidenced gaps** (P3 minus perfection) — Rework against findings
   or unmet criteria. Stop at criteria-met or bound.
5. **Simplest adequate** (P4 + YAGNI) — Smallest design _and_ process that meets
   the current spec. No speculative roles, platforms, or gates.
6. **Smallest useful specialization** (P8/P9) — Roles are contracts. Spawn
   instances only for focus or independence. Hand off spec, constraints,
   outputs, and evidence.
7. **One GM, not one bottleneck** (P12) — Sole Client business contact;
   accountable for all internal agents including PM. Specialists may hand off in
   the shared record. GM may not waive principles for speed.
8. **Client accepts product** (H2 proposal, not H2 as written) — Client accepts
   the integrated result. GM presents evidence. BA prepares product criteria. GM
   does not self-declare Client acceptance.
9. **Independent check** (P7 + H1 constraint) — Implementer cannot verify their
   own work item. Reviewer/Tester use a different execution context.
   Persona-switch is not independence.
10. **Evidence of done includes regression** (P7 expanded) — Observable tests,
    failure paths, and prior accepted behavior. Assertions are not evidence. Do
    not weaken criteria to finish.
11. **Nonfunctional fitness is explicit** (new) — Maintainability and agreed
    NFRs are in criteria or an explicit GM/Client deferral. Omission is not a
    skip.
12. **Delivery is not production** (scope → principle) — A finished package does
    not authorize deploy, operate, or unrestricted tool/model expansion.
13. **Bounded authorized operation** (R1 slim) — Before a run: authority,
    permissions, budgets, retry/stop/escalate. Stalls escalate. No indefinite
    loops.
14. **State, journal, versions** (P13) — Current owner/next action; append-only
    why/who; versioned artifacts. Recover from records. No silent history
    replace.
15. **One active owner** (workflow, slim) — One claimed owner per work item.
    Stale results are evidence, not current state. Role-contract changes do not
    silently rewrite active assignments.
16. **Audited, reversible process change** (P5 + slim R4) — Every finished run
    (including fail/cancel) gets a non-recursive audit. Findings are
    Client-visible. GM records disposition. Adopted process/role changes are
    versioned and reversible. Activity metrics cannot substitute for the Client
    ask.

## Top 3 owner decisions

1. Adopt slim R1 (bounds / stop / escalate) into the runtime charter before any
   loop experiment. Without it P3 is not operational.
2. Split H2: Client/GM/BA own product criteria; a separate context verifies; GM
   escalates conflicts. Do not approve joint ownership of "quality metrics" as
   one blob.
3. Audit-record independence: findings and GM dispositions always in the
   Client-visible triad. Keep Auditor reporting to GM for action.

## Do not add

- SOLID, DORA, or SRE metric dashboards as governing principles
- H3 as a required gate (try later only if it improves readiness)
- Per-turn audits, a message bus, or a frozen org chart
- P6 into the runtime charter
- Perfection, "professional structure proves quality," or numeric budgets inside
  the principles themselves
