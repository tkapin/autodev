# Autonomous development loop mechanics

Purpose/status: this documentation-only research track examines autonomous loop
mechanics for AutoDev, not runtime selection or approval of boundaries,
architecture, or metrics. Sources were read on 2026-09-20. I used first-party
articles and repositories where available; GitHub repositories are cited with
the commit read. I did not run benchmarks, agent loops, models, or external
frameworks.

## Findings

The most transferable pattern is not "Ralph" as a single specification, but a
family of deliberately simple loops that repeatedly allocate a bounded task to
an agent, force external feedback, persist selected state on disk, and start
again with a mostly fresh context.

Geoffrey Huntley's primary article presents Ralph first as a technique whose
"purest form" is a Bash loop: `while :; do cat PROMPT.md | claude-code ; done`.
The author claims it can replace much greenfield outsourcing, but also says it
has defects, requires prompt tuning, and is unsuitable for existing codebases.
Observed mechanics in the article include one task per loop, deterministic
reloading of plans/specifications into context, heavy emphasis on tests/builds
as "backpressure", documentation of learnings into `AGENT.md`/plans, and
willingness to reset or re-plan when the codebase is broken. That is an author's
report from a greenfield compiler project, not general production evidence.

The `snarktank/ralph` implementation narrows Ralph into a PRD/story loop. Its
README says each iteration is a fresh instance, with memory through git history,
`progress.txt`, and `prd.json`; the workflow selects the highest-priority story
whose `passes` flag is false, implements one story, runs checks, commits, marks
the story passing, appends learnings, and repeats until all pass or a maximum
iteration count is reached. The script confirms this is a finite `for` loop with
default `MAX_ITERATIONS=10`, tool choice validation, selected agent invocation,
and an explicit `<promise>COMPLETE</promise>` completion signal. On failure to
finish within the bound it exits nonzero and points the user to `progress.txt`.
This implementation therefore adds bounded execution and a visible incomplete
state that Huntley's infinite-loop description does not require.

The `snarktank` prompt also demonstrates durable state as work instructions, not
just logs: read the PRD, read the progress log, use the branch named by the PRD,
work on one story, run project checks, update reusable patterns, append a
progress report, and only emit the completion promise when all stories pass. It
separates story-specific progress from reusable codebase learnings, which is
directly relevant to AutoDev handoffs.

The `iannuttall/ralph` implementation is another interpretation: a global CLI
whose README describes a minimal file-based loop where files and git are memory,
state lives in `.ralph/`, and each build can be one iteration. It introduces
state fields `open`, `in_progress`, and `done`; if a crash leaves a story
`in_progress`, `STALE_SECONDS` can reopen stalled stories. Its durable state set
is richer: `progress.md`, `guardrails.md`, `activity.log`, `errors.log`, and raw
run logs/summaries. That gives AutoDev a concrete source pattern for
distinguishing progress, guardrails, activity timing, errors, and run artifacts
without assuming one monolithic transcript.

Andrej Karpathy's relevant primary-source work is narrower than a general
software-production framework. In `karpathy/autoresearch`, the README describes
an experiment in autonomous AI research: an agent modifies `train.py`, trains
for five minutes, checks whether validation bits-per-byte improved, keeps or
discards, and repeats. The repository intentionally keeps only three core files:
`prepare.py` as fixed data/evaluation, `train.py` as the editable target, and
`program.md` as agent instructions. This is strong primary evidence for an
optimization loop with a tight verifiable metric, a fixed time budget, one
editable file, and git-based keep/discard; it is not evidence that the same loop
solves full lifecycle software development.

Karpathy's `program.md` makes the optimization framing explicit. It forbids
changing the evaluation harness or dependencies, requires a baseline run, logs
results in `results.tsv`, treats crashes as `crash`, keeps lower `val_bpb`
commits, resets equal/worse results, kills runs over ten minutes, and says to
give up on crash fixes after more than a few attempts. It also tells the agent
to continue indefinitely until manually stopped. For AutoDev, the useful parts
are the hard metric, immutable evaluator, result log, and explicit crash policy;
the indefinite stopping rule conflicts with R1 bounded autonomy unless
explicitly changed.

Karpathy's broader 2026 Sequoia summary is AI-generated content that he says he
read and found acceptable, so I treat it as lower-strength primary commentary,
not code evidence. It distinguishes "vibe coding" from "agentic engineering" and
claims professional agentic engineering needs specs, plans, diffs, tests,
permission management, isolated worktrees, and quality preservation. It also
states that AI moves fastest where work is verifiable: coding gives tests,
crashes, inspectable diffs, and benchmarks. This supports AutoDev's focus on
verification, but should not be read as Karpathy endorsing Ralph or any specific
handoff architecture.

## Limitations and failure modes

Loop evidence is strongest in narrow, externally verifiable settings. Ralph
reports emphasize greenfield projects, one bounded item per loop, and frequent
manual prompt tuning. Huntley explicitly expects broken states and senior
judgment; his article frames maintainability around further loops, which is a
claim rather than a demonstrated organizational control. `snarktank` and
`iannuttall` provide executable loop designs but no general benchmark evidence
in the inspected sources. Karpathy's AutoResearch is an optimization experiment
on one file, one GPU, one metric, and an immutable evaluator; transferring it to
product work requires acceptance criteria, review, security, and maintainability
evidence beyond a scalar score.

Failure modes to design for include false "not implemented" conclusions from
search, compounding broken code when checks are weak, placeholder
implementations that merely satisfy superficial tests, stale locked tasks after
crashes, oversized stories that exhaust context, and logs that preserve status
but not the reasoning needed by future fresh-context runs.

## Implications for AutoDev principles

For P1/P2, loop input should be a reviewed specification plus explicit
acceptance criteria; Ralph-style PRD JSON is useful only after analysis resolves
ambiguity. For P3/P7, iteration must be driven by failed checks, review
findings, or unmet criteria, not by repetition. For P4/P8/P9, the evidence
favors a small loop kernel with specialized handoff artifacts over a complex
agent platform at the outset. For P5/R4, process changes should be versioned and
compared against previous runs; do not promote prompt folklore into policy
without evidence. For R1, AutoDev should prefer bounded iteration, nonzero
incomplete exits, crash reporting, and escalation over indefinite "never stop"
loops.

## Recommended experiments, unapproved

1. Prototype a paper loop only: one ready spec, one implementation slot, one
   reviewer/tester verification slot, and a final report schema. Measure whether
   the artifacts make failure visible without running agents.
2. Compare retained versus fresh context by replaying the same small task from
   only durable files: spec, plan, progress, guardrails, errors, and
   verification evidence. Note what context is missing.
3. Define two stop policies for discussion: a Ralph-style max-iteration/story
   bound and an AutoResearch-style metric/crash bound. Evaluate which failures
   each would report clearly.

## References

- Geoffrey Huntley, "Ralph", no source date observed, accessed 2026-09-20:
  <https://ghuntley.com/ralph/>
- [snarktank/ralph](https://github.com/snarktank/ralph/tree/6c53cb0b831ebe8739c6a003e22af14902d8b0b5),
  commit `6c53cb0b831ebe8739c6a003e22af14902d8b0b5` (2026-02-02): README lines
  5, 122-130, 163-168; `ralph.sh` lines 7-9, 84-113; `prompt.md` lines 7-16,
  37-48, 76-101.
- [iannuttall/ralph](https://github.com/iannuttall/ralph/tree/5bc402540c45192bd1e9cacb84611ee2e5ba13a8),
  commit `5bc402540c45192bd1e9cacb84611ee2e5ba13a8` (2026-02-04): README lines
  5-13, 91-97, 150-156.
- [karpathy/autoresearch](https://github.com/karpathy/autoresearch/tree/228791fb499afffb54b46200aca536f79142f117),
  commit `228791fb499afffb54b46200aca536f79142f117` (2026-03-26): README lines
  7, 11-17, 61-65; `program.md` lines 23-39, 64-112.
- Andrej Karpathy, "Sequoia Ascent 2026 summary", 2026-04-30, accessed
  2026-09-20: <https://karpathy.bearblog.dev/sequoia-ascent-2026/>
- Andrej Karpathy, "2025 LLM Year in Review", 2025-12-19, accessed 2026-09-20:
  <https://karpathy.bearblog.dev/year-in-review-2025/>
