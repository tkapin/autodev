# Existing Systems Research

Purpose/status: documentation-only research for AutoDev, accessed 2026-09-20.
No framework was installed or run. Recommendations below are experiment prompts,
not approved architecture. Sources are primary repositories/docs at the commits
listed in References.

## Sourced findings

Spec Kit is the closest match for AutoDev's specification artifact layer. Its
README presents independent processes for spec-driven development, bug fixing,
and idea assessment, producing respectively a spec carried through planning and
implementation, an assessed fix with verification, and an evidence-backed
go/clarify/stop decision.[^speckit-processes] Its SDD path explicitly says to
define "what and why" before "how", then produce a specification, technical
plan, tasks, implementation, and convergence loop.[^speckit-sdd] Its bug flow
keeps diagnosis, repair, and verification separate and states that missing
verification is not a successful fix.[^speckit-bug] Reuse candidate: borrow the
artifact sequence, clarification markers, checklists, and convergence language
before inventing AutoDev's own spec format. Constraint: it is a CLI/skill
toolkit requiring Python 3.11+, `uv`, and a supported coding agent, not a full
autonomous runtime.[^speckit-setup]

Spec Kit's methodology also validates AutoDev's emphasis on reviewable business
intent. Its long-form SDD document says specs become the primary artifact, code
serves specs, and AI should ask clarifying questions, identify edge cases, and
define acceptance criteria.[^speckit-primary] It also claims templates constrain
LLMs by preventing premature implementation details, forcing `[NEEDS
CLARIFICATION]`, and applying checklist-style self-review.[^speckit-templates]
That maps directly to P1, P2, P7, and P4. The unverified part for AutoDev is
whether Spec Kit's "converge" is strong enough for owner acceptance and session
audit, because the README documents the skill sequence but not AutoDev-like
manager/owner handoffs.

Mini-SWE-agent/SWE-agent is the best small execution-harness baseline. The
larger SWE-agent README says development effort has moved to mini-SWE-agent and
recommends it going forward.[^sweagent-superseded] Mini-SWE-agent's README says
its agent class is about 100 lines, it supports local and sandboxed execution
environments, and it has a trajectory browser/Python bindings.[^mini-summary]
The most transferable design choices are intentionally minimal: no tools other
than bash, linear message history, and independent `subprocess.run` actions
instead of a stateful shell.[^mini-minimal] Reuse candidate: use it as a
reference implementation for P4/P7/P8 experiments, especially durable
trajectories and shell-based verification. Constraint: it solves GitHub
issue-like coding tasks; it does not provide business analysis, spec readiness,
or multi-role handoffs.

Aider is a mature human-in-the-loop coding interface rather than an autonomous
process manager. Its README documents repo maps for large codebases, automatic
git commits, IDE comment triggers, and lint/test integration.[^aider-features]
Its lint/test docs are especially relevant to P7: tests can be run after each AI
edit and Aider attempts to fix non-zero test results.[^aider-test] Reuse
candidate: copy interaction patterns, not architecture--repo maps for
context-minimal implementation agents, git-level undoability, and explicit
test-command hooks. Constraint: Aider is designed as pair programming in a
terminal, so AutoDev would still need spec gating, handoff records, and session
audit around it.

OpenHands Agent Canvas is relevant to orchestration and hosting, not spec
analysis. Its README describes a self-hosted developer control center for coding
agents and automations, local/remote/cloud backends, event/scheduled
automations, and support for ACP-compatible agents.[^openhands-overview] It can
run without a sandbox, warning that the agent will have full filesystem access,
or with a Docker sandbox and project mounts.[^openhands-sandbox] Its
architecture separates Agent Canvas, a software-agent SDK/Agent Server,
automation scheduling, and client APIs.[^openhands-architecture] Reuse
candidate: study its backend abstraction and run-history/scheduling split
before building a plugin/runtime. Constraint: adopting it wholesale may add UI
and platform scope before AutoDev has validated the smallest useful loop.

Microsoft Agent Framework is a current production-oriented orchestration option
and is more relevant than older AutoGen for new work: AutoGen's README states
it is in maintenance mode and points feature development to Microsoft Agent
Framework.[^autogen-maintenance] MAF advertises production-grade agents and
multi-agent workflows for .NET/Python, with sequential, concurrent, handoff, and
group collaboration patterns, checkpointing, streaming, human-in-the-loop,
time-travel, observability, declarative agents, and skills.[^maf-overview]
Reuse candidate: evaluate MAF only if AutoDev's first experiments prove a need
for durable graph orchestration. Constraint: it brings Azure/Foundry-oriented
samples and explicit responsibility warnings for third-party systems, data
sharing, quality, reliability, security, and trustworthiness.[^maf-warning]

MCP is the strongest interoperability reuse target. The spec repo says MCP
contains the specification, schema, and docs, with TypeScript and JSON Schema
schemas.[^mcp-readme] Its architecture defines a host-client-server model with
multiple isolated client sessions and clear security boundaries.[^mcp-arch] MCP
separates model-controlled tools, user-controlled prompts, and
application-driven resources.[^mcp-tools][^mcp-prompts][^mcp-resources] Reuse
candidate: express AutoDev prompts/skills/context resources through MCP where a
host supports it, instead of inventing an integration protocol. Constraint: MCP
standardizes context/tool exchange; it does not define a software-development
lifecycle or acceptance process.

## Implications for AutoDev principles

For P1/P2/P7, reuse Spec Kit-style Markdown artifacts, clarification markers,
and verification verdicts before creating novel BA documents. For P3/P5, borrow
trajectory/run-history ideas from mini-SWE-agent, OpenHands, and MAF, but keep
audit criteria independent of any single runtime. For P4/P8/P9, begin with one
spec agent/checker and one implementation harness plus an independent verifier;
add manager/PM roles only when evidence shows a missing responsibility. For R1,
MCP and OpenHands both reinforce explicit permission/sandbox boundaries.

## Small experiments/reuse checks

1. Convert one AutoDev sample feature into Spec Kit-style `spec.md`, `plan.md`,
   `tasks.md`, and verification notes; assess whether P2 questions and P7
   evidence are naturally captured.
2. Run a paper design of a mini-SWE-agent-like executor contract: input spec,
   clean context, shell commands, patch, tests, linear trajectory; decide which
   fields AutoDev must preserve for audit before executing anything.
3. Prototype no code: map AutoDev artifacts to MCP resources, prompts, and
   tools, then identify what remains outside MCP as lifecycle policy.

## Limitations

I did not install or execute any framework. Some performance and adoption claims
are documented by project READMEs but not independently verified here. I used
current repository content and official docs only; vendor marketing language is
treated as capability claims until tested in AutoDev-specific experiments.

## References

[^speckit-processes]:
    GitHub Spec Kit README, commit
    `d4229c071c7ea3885b43e8a7739847300f618f13`, lines
    [23-33](https://github.com/github/spec-kit/blob/d4229c071c7ea3885b43e8a7739847300f618f13/README.md#L23-L33).

[^speckit-setup]:
    GitHub Spec Kit README, lines
    [37-65](https://github.com/github/spec-kit/blob/d4229c071c7ea3885b43e8a7739847300f618f13/README.md#L37-L65).

[^speckit-sdd]:
    GitHub Spec Kit README, lines
    [70-90](https://github.com/github/spec-kit/blob/d4229c071c7ea3885b43e8a7739847300f618f13/README.md#L70-L90).

[^speckit-bug]:
    GitHub Spec Kit README, lines
    [100-119](https://github.com/github/spec-kit/blob/d4229c071c7ea3885b43e8a7739847300f618f13/README.md#L100-L119).

[^speckit-primary]:
    Spec Kit SDD methodology, lines
    [7-29](https://github.com/github/spec-kit/blob/d4229c071c7ea3885b43e8a7739847300f618f13/spec-driven.md#L7-L29).

[^speckit-templates]:
    Spec Kit SDD methodology, lines
    [165-204](https://github.com/github/spec-kit/blob/d4229c071c7ea3885b43e8a7739847300f618f13/spec-driven.md#L165-L204).

[^sweagent-superseded]:
    SWE-agent README, commit `3ea751c087f32b16e039a2233dd6eefecef325d5`,
    lines
    [19-25](https://github.com/SWE-agent/SWE-agent/blob/3ea751c087f32b16e039a2233dd6eefecef325d5/README.md#L19-L25).

[^mini-summary]:
    Mini-SWE-agent README, commit
    `04d809ceab9df28f9adaed044884180159172930`, lines
    [23-32](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/README.md#L23-L32)
    and
    [128-148](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/README.md#L128-L148).

[^mini-minimal]:
    Mini-SWE-agent README, lines
    [38-54](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/README.md#L38-L54)
    and
    [69-79](https://github.com/SWE-agent/mini-swe-agent/blob/04d809ceab9df28f9adaed044884180159172930/README.md#L69-L79).

[^aider-features]:
    Aider README, commit `5dc9490bb35f9729ef2c95d00a19ccd30c26339c`,
    lines
    [49-94](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/README.md#L49-L94).

[^aider-test]:
    Aider lint/test docs, lines
    [59-73](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/website/docs/usage/lint-test.md#L59-L73).

[^openhands-overview]:
    OpenHands README, commit `a07364828c8f202e7745c6bce3dcef3915ae7ac1`,
    lines
    [33-47](https://github.com/OpenHands/OpenHands/blob/a07364828c8f202e7745c6bce3dcef3915ae7ac1/README.md#L33-L47).

[^openhands-sandbox]:
    OpenHands README, lines
    [63-104](https://github.com/OpenHands/OpenHands/blob/a07364828c8f202e7745c6bce3dcef3915ae7ac1/README.md#L63-L104).

[^openhands-architecture]:
    OpenHands README, lines
    [124-150](https://github.com/OpenHands/OpenHands/blob/a07364828c8f202e7745c6bce3dcef3915ae7ac1/README.md#L124-L150).

[^autogen-maintenance]:
    AutoGen README, lines
    [216-218](https://github.com/microsoft/autogen/blob/main/README.md#L216-L218).

[^maf-overview]:
    Microsoft Agent Framework README, commit
    `723256961e8e46980b869ee2c75ef05f16644921`, lines
    [12-15](https://github.com/microsoft/agent-framework/blob/723256961e8e46980b869ee2c75ef05f16644921/README.md#L12-L15),
    [31-38](https://github.com/microsoft/agent-framework/blob/723256961e8e46980b869ee2c75ef05f16644921/README.md#L31-L38),
    and
    [50-59](https://github.com/microsoft/agent-framework/blob/723256961e8e46980b869ee2c75ef05f16644921/README.md#L50-L59).

[^maf-warning]:
    Microsoft Agent Framework README, lines
    [211-219](https://github.com/microsoft/agent-framework/blob/723256961e8e46980b869ee2c75ef05f16644921/README.md#L211-L219).

[^mcp-readme]:
    MCP README, commit `24efd6e7cbd7a074e6b3b781eb370891df40afad`,
    lines
    [5-16](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/24efd6e7cbd7a074e6b3b781eb370891df40afad/README.md#L5-L16)
    and
    [26-28](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/24efd6e7cbd7a074e6b3b781eb370891df40afad/README.md#L26-L28).

[^mcp-arch]:
    MCP architecture spec, lines
    [7-11](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/24efd6e7cbd7a074e6b3b781eb370891df40afad/docs/specification/2025-06-18/architecture/index.mdx#L7-L11)
    and
    [48-70](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/24efd6e7cbd7a074e6b3b781eb370891df40afad/docs/specification/2025-06-18/architecture/index.mdx#L48-L70).

[^mcp-tools]:
    MCP tools spec, lines
    [7-20](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/24efd6e7cbd7a074e6b3b781eb370891df40afad/docs/specification/2025-06-18/server/tools.mdx#L7-L20)
    and
    [22-33](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/24efd6e7cbd7a074e6b3b781eb370891df40afad/docs/specification/2025-06-18/server/tools.mdx#L22-L33).

[^mcp-prompts]:
    MCP prompts spec, lines
    [7-26](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/24efd6e7cbd7a074e6b3b781eb370891df40afad/docs/specification/2025-06-18/server/prompts.mdx#L7-L26).

[^mcp-resources]:
    MCP resources spec, lines
    [7-28](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/24efd6e7cbd7a074e6b3b781eb370891df40afad/docs/specification/2025-06-18/server/resources.mdx#L7-L28).
