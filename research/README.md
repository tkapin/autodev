# AutoDev research handoff

## Status

Three bounded research tracks completed on 2026-09-20 using separate
clean-context research subagents, explicitly configured with GPT-5.5.
The reports are source-based research, not runtime evaluations. No framework
was installed or executed, and no recommendations were promoted to approved
principles or architecture.

## Reports

- [Existing systems](01-existing-systems.md): Spec Kit, mini-SWE-agent, Aider,
  OpenHands, Microsoft Agent Framework, and MCP as potential artifact,
  execution, orchestration, and interoperability references.
- [Autonomous loops](02-autonomous-loops.md): distinct Ralph implementations,
  Karpathy's narrower optimization-loop evidence, verification, durable state,
  fresh contexts, and stopping behavior.
- [Agent organization](03-agent-organization.md): comparative evidence and its
  limits for specialization, structured handoffs, context management,
  independent verification, and coordination cost.

Each report contains sources, limitations, implications for the current
principles, and suggested experiments. Read the findings with their evidence
limits, not as endorsements of a complete solution.

## Signals to examine during synthesis

These are cross-report observations, not new project decisions:

- Specifications, explicit handoff artifacts, external verification, and durable
  state recur across otherwise different approaches.
- Small execution loops are useful baselines; an exact human organizational
  chart is not established by the reviewed evidence.
- Fresh context can reduce irrelevant history but requires sufficient durable
  inputs. The reports do not establish that restarting context is always better.
- Evidence from issue repair, generated small applications, or narrow metric
  optimization does not establish full-lifecycle product delivery.
- Existing tools address different layers. A protocol such as MCP does not
  itself provide lifecycle orchestration or universal skill/plugin packaging.

## Remaining due diligence

The reports are a bounded sample, not an exhaustive market or literature review.
Claims from READMEs and authors must not be confused with independently
reproduced results. The multi-agent report relies substantially on older
studies; current model behavior and more recent evidence may differ.

License compatibility, dependency/platform support, model-provider policy,
installation behavior, and exact host integration need separate checks before
adopting code or dependencies. No package or framework has been selected.

## Recommended next work package

Use a fresh main session for synthesis with the owner. Read the project README
and these three reports rather than importing the research conversations.

First separate supported findings, plausible inferences, and unresolved
hypotheses. Then select one representative development task and propose a
minimal experiment with a simpler baseline, observable acceptance evidence,
and an explicit resource budget. Discuss specification readiness and the
smallest useful specialized agent structure in that concrete setting.

This is a recommendation, not authorization to implement or run the experiment.
Apply P6 before starting the new work package.

Suggested fresh-session prompt:

> Read README.md and the four Markdown files under its research
> directory. Recommend how to run the synthesis work package and obtain my
> execution-placement choice under P6. Help me distinguish research-supported
> principles from untested organizational hypotheses, then choose one small
> representative task and propose an experiment. Do not select a runtime, adopt
> recommendations, implement agents, or run an experiment without agreement.
