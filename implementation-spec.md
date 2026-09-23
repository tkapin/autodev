# AutoDev v0.1 implementation

## Authorized scope

The Client authorized autonomous completion of a lightweight, usable v0.1 for
Copilot CLI and the Copilot app, with an intended `/autodev` GM entry point.
Self-inspection and self-evolution are essential, not deferred aspirations.
Use the existing role/workflow design proportionately rather than building a
general-purpose agent platform.

The initial implementation used explicitly authorized local installations and
small live trials with existing Copilot access. Those historical permissions
are not standing authorization for future contributors or runs to install,
publish, spend resources, or push changes. Each engagement needs its own
authority and operating limits. Use explicitly selected non-Anthropic models
under the shipped default policy.

At runtime, project-local improvements may be adopted automatically after
independent evaluation and with a revert path. Shared-plugin changes require a
Client decision. The implementation permission above is not a standing runtime
grant to rewrite the shared plugin.

## Smallest useful architecture

- A single installable `tkapin-autodev` plugin: an `autodev` skill and GM agent,
  supporting role agents, and concise shared operating instructions.
- Copilot supplies model execution, separate agent contexts, permission prompts,
  and normal coding tools. AutoDev does not duplicate that runtime.
- A Python 3.11+ standard-library helper implements deterministic local
  coordination. There is no service, package dependency, API key, or broker.
- Each target project has its own `.autodev/state.sqlite3`: current state,
  immutable artifact versions, and an append-only material-event journal.
  Updates to state and journal are one SQLite transaction.
- The helper emits JSON for agents and a concise Markdown inspection report for
  people. Versioned guidance and tools can be materialized within `.autodev`;
  SQLite remains authoritative.

The legacy root `plugin.json` layout is deliberately used for compatibility
with both installed hosts' agent discovery. The newer Agent Plugins 1.0 schema
moves agents into a client namespace; declaring that schema while shipping
legacy agent paths would be incorrect. No duplicated agent definitions are
needed.

## Required behaviors

1. Load the plugin and discover the `autodev` skill and GM agent in both hosts.
   A skill entry point follows the GM contract; selecting the custom GM agent
   also pins its configured model. A skill alone does not change the host model.
2. Start or resume from project-local durable records. Keep the Client-facing
   interaction with GM and authorized BA clarification.
3. Record versioned specification, architecture, and plan artifacts. Bind
   Client approval to their exact versions before executing a sprint.
4. Delegate bounded work, with one active owner and assignment revision.
   Reject stale submissions and conflicting active write scopes. Record
   independent review and test evidence for exact file snapshots.
5. Require integrated verification for technical sprint success. Preserve
   actual failed/cancelled outcomes and pending audits. Block the next sprint
   on an incomplete audit unless the Client records a specific exception.
6. Record audit scope, completion requirements, coverage limitations, findings,
   and GM dispositions. Missing supplemental feedback differs from unfinished
   mandatory examination. Produce a useful GM-to-Client progress summary.
7. Inspect recorded work and feedback, propose an improvement, independently
   evaluate its exact content, and adopt or revert project-local guidance or
   tooling. Reject stale evaluations and incompatible baseline changes.
8. Keep shared improvements as approval-gated proposals. The helper never
   silently rewrites its installation. Approved shared work is handed off to a
   separately authorized change to the plugin source and subsequent installation.
9. Keep product verification, Client acceptance, run outcome, release authority,
   and audit/handover closure distinct. Do not claim a draft or mocked
   evaluation establishes runtime effectiveness.

## Authority and limits

The helper validates workflow invariants, versions, roles, and scope; it is not
an OS sandbox or identity provider. Actor/context identifiers and Client
decision evidence come from the trusted host/operator. A caller with arbitrary
filesystem or shell access can bypass a local database; do not market prompt
instructions or role labels as a security boundary.

Agents must obtain actual Client decisions through their host, not fabricate
approval evidence. Model/tool permissions, access controls, and cancellation
remain host responsibilities. Project-local overrides cannot alter these rules.
Do not log secrets or copy whole private transcripts.

New engagements specify sprint, task, and retry limits in their proposed plan.
The implementation run's lack of a time limit does not authorize an unbounded
autonomous delivery loop. No automatic improvement chain is launched by an
audit or adoption. Safe parallel execution is permitted only with explicit
non-conflicting scopes; serial execution is an acceptable v0.1 default.

## Evidence for completion

- Standard-library automated tests for state/journal atomicity, restart,
  approval/version gates, stale and conflicting ownership, integration,
  incomplete audits, improvement independence, scope boundaries, and rollback.
- Manifest/agent/skill discovery through the actual installed CLI and app
  integration, not filename inspection alone.
- A small live disposable-project delivery using the plugin, plus inspection
  and a verified project-local improvement. Demonstrate that an unapproved
  shared improvement cannot be adopted through the helper.
- Document actual commands, versions, outcomes, remaining limitations, and
  installation/use/uninstall instructions. Preserve evidence without committing
  private session logs or credentials.

## Non-goals

No cloud service, custom model API integration, remote message bus, dashboard,
general distributed scheduler, automatic deployment, or benchmark platform.
No claim to prevent malicious agents with unrestricted shell access. The first
release favors recoverable local work and useful agent instructions over
perfect automation of every organizational policy.

## Host references

- [Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)
- [Custom agent configuration](https://docs.github.com/en/copilot/reference/custom-agents-configuration)
- Installed `copilot --help`, `copilot plugin --help`, and `copilot skill --help`.
- For the optional app adapter, the installed host's plugin-management help.

Checked against Copilot CLI 1.0.87-0. Host-specific discovery and invocation are
verified again with the completed package before reporting installation success.
