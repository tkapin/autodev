# Agent organization evidence

Access date: 2026-09-20. Status: bounded research synthesis for AutoDev
framework design, not an approved architecture or recommendation.

## Research question

When does specialized or multi-agent organization improve software-development
outcomes, and when do coordination, handoff loss, role-playing, correlated
mistakes, or overhead make it worse? The evidence below treats the owner's
preference for specialization and clean focused contexts as a design intent to
test, while keeping H1-H3 open.

## Sourced findings

The strongest cautionary evidence is Agentless (Xia et al., published
2024-07-01; v2 2024-10-29), evaluated on SWE-bench Lite repository repair tasks.
The authors explicitly ask whether complex autonomous software agents are
necessary, then compare a controlled localization/repair/patch-validation
pipeline against agent-based approaches. Their demonstrated result is not "no
agents ever"; it is that, for SWE-bench Lite bug-fix issues, a simple
non-autonomous process that withholds open-ended action planning from the model
was competitive or better than contemporary open-source software agents at much
lower cost. The relevant failure analysis is also architectural: complex tool
interfaces can be misused, long action chains are hard to debug, and a wrong
step can propagate through later turns. Implication: AutoDev should treat
multi-agent organization as a hypothesis that must beat a simpler structured
pipeline baseline, especially for localized repair tasks.

MetaGPT (Hong et al., published 2023-08-01; v7 2024-11-01) is the best primary
source supporting specialization with structured handoffs. It uses software-team
analogies such as product manager, architect, project manager, engineer, and QA
engineer, but its core mechanism is not the analogy itself. The authors argue
that Standard Operating Procedures, typed intermediate artifacts, and executable
feedback reduce ambiguity and idle role-playing chatter. Their experiments
include HumanEval, MBPP, and a SoftwareDev-style benchmark, with ablations for
roles and executable feedback. The transferable claim is narrower than "copy a
human org chart": structured intermediate outputs and verification checkpoints
can improve collaboration; professional labels are a prompt scaffold whose value
depends on the artifacts and checks they produce.

ChatDev (Qian et al., published 2023-07-16; accepted ACL 2024, v5 2024-06-05)
also supports bounded specialization, but with important limits. It organizes
design, coding, and testing through a chat chain and communicative
dehallucination, where agents request more detail instead of answering
prematurely. The demonstrated scope is generated software from requirement
descriptions and analyses of completeness, executability, and consistency. This
supports AutoDev principles P2, P7, and P9: ask clarifying questions, separate
work phases, and test artifacts rather than trust claims. It does not settle
whether AutoDev needs distinct BA, manager, PM, architect, reviewer, tester, and
auditor agents; it shows that communication protocols can matter.

The Microsoft AutoDev paper by Tufano et al. (published 2024-03-13) is relevant
mainly as a same-name adjacent system. It describes autonomous agents with
repository tools, build/test execution, a conversation manager, scheduler, and
Docker evaluation environment, and evaluates HumanEval code generation and test
generation. It demonstrates that tool-using autonomous development loops can be
made concrete, guarded, and test-driven. It does not provide a clean ablation of
multi-agent specialization versus one agent, nor a full-lifecycle BA-to-owner
acceptance study, so it should not be used as proof for H1-H3.

Lost in the Middle (Liu et al., published 2023-07-06; TACL 2023, v3
2023-11-20) is not a software-agent study, but it is directly relevant to fresh
versus retained context. Across multi-document QA and key-value retrieval, the
authors found that models often use information less reliably when the relevant
content is buried in the middle of long contexts. This supports the owner's
preference for clean, focused contexts and explicit handoffs, but only as an
indirect mechanism: shorter focused contexts may reduce retrieval burden, while
critical decisions and evidence still need to be retained in durable artifacts.

AI Agents That Matter (Kapoor et al., published 2024-07-01) is a useful
evaluation warning rather than software-lifecycle evidence. It argues that agent
evaluations should control cost and compare Pareto frontiers, because extra
inference-time computation can make an agent appear better while merely spending
more. AutoDev comparisons should therefore count tokens, wall time, tool calls,
human interventions, and successful acceptance evidence, not only solved tasks.

## Evidence limits

Direct comparative evidence for a complete professional software lifecycle is
thin. Available studies mostly cover coding benchmarks, generated toy projects,
or issue repair. They rarely isolate BA versus manager ownership, manager-before
owner review, retained versus clean contexts, independent reviewer/tester
effects, or hierarchy depth. Role-playing risks are better evidenced by the
systems' own mitigations than by head-to-head role-title ablations. Correlated
mistakes remain under-measured: if all agents share the same model family,
prompt style, retrieval errors, or flawed specification, "independent" review
may simply repeat the same false assumption.

## Implications for AutoDev principles and hypotheses

P8 should be read as an empirical constraint: use the smallest role structure
that creates distinct artifacts, checks, or authority boundaries. P9 is
supported when handoffs carry explicit specification slices, assumptions,
decisions, required evidence, and failure criteria; unsupported handoff chatter
is a known risk. Clean contexts are plausible for reducing distraction, but they
must be paired with durable handoff artifacts so important decisions are not
lost. Independent review and testing are likely valuable when they run different
checks against observable artifacts, not when they merely ask another similar
agent to agree.

H1 remains unproven as an exact roster. H2 remains open because none of the
sources validates BA/manager joint ownership of delivery criteria. H3 remains
open because the evidence supports verification gates generally, not a specific
manager-then-owner demo sequence.

## Bounded falsification experiments

1. Compare a single structured agent, a three-role loop (spec/design,
   implement, verify), and the proposed fuller roster on the same small issue
   set. Hold model, tools, budget, and acceptance criteria constant. Falsify
   extra roles if they add cost or handoff defects without improving accepted
   outcomes.

2. Compare retained long-context execution against clean-context specialists
   receiving only a written handoff plus artifacts. Score missed requirements,
   hallucinated decisions, duplicate work, and verification pass rate.

3. Compare verification modes: implementer self-check only, independent reviewer
   only, independent tester with executable tests, and reviewer plus tester.
   Falsify role separation if independent checks do not catch distinct defects
   beyond a cheaper baseline.

## References

- Agentless: <https://arxiv.org/abs/2407.01489> and HTML
  <https://arxiv.org/html/2407.01489>
- MetaGPT: <https://arxiv.org/abs/2308.00352> and HTML
  <https://arxiv.org/html/2308.00352>
- ChatDev: <https://arxiv.org/abs/2307.07924> and HTML
  <https://arxiv.org/html/2307.07924>
- AutoDev: <https://arxiv.org/abs/2403.08299> and HTML
  <https://arxiv.org/html/2403.08299>
- Lost in the Middle: <https://arxiv.org/abs/2307.03172> and HTML
  <https://arxiv.org/html/2307.03172>
- AI Agents That Matter: <https://arxiv.org/abs/2407.01502> and HTML
  <https://arxiv.org/html/2407.01502>
