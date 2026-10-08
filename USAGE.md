# Using AutoDev v0.2.0

## Requirements

- Copilot CLI with plugin/custom-agent/skill support and existing authentication.
- Python 3.11 or later on PATH. No Python packages or API keys are required.
- For app registration, the installed `agency` host CLI.
- Permitted access to the target project and this plugin's helper directory.

The default GM model is `gpt-6-astra`; supporting roles use `gpt-5.4` and
`gpt-6-astra`. Model availability depends on the account/host. Do not silently
fall back to Auto routing or an Anthropic model. An operator can select another
explicitly permitted model and align the project policy before executing work.
For an initialized project, relay the Client's exact authorized allowlist
through `update-models` with `models`, `reason`, `evidence`, and a fresh mandatory
`expected_revision`. This is a Client-only policy decision, not permission to
relabel a prior actor or bypass delivery/audit gates. See the operating guide
for the request schema and retained history.

## Install locally

From this PoC directory in PowerShell 7:

```powershell
.\Install-AutoDev.ps1
```

The installer makes an immutable, content-addressed copy under
`$HOME\.autodev\releases`, then uses the native CLI and app-host plugin managers
to register it. Existing unrelated plugins/configuration are preserved.
It does not restart sessions or publish to a marketplace. New sessions load the
registered release. Updating requires deliberately running the installer again
from an approved source version, not allowing a project agent to edit the copy.
For an app upgrade to a different content-addressed release, first remove the
old `tkapin-autodev` app registration with the uninstall command below; Agency
otherwise correctly treats a different local source with the same name as a
conflict. Cached release files are retained for recovery.

Stop active AutoDev work before upgrading its code. If this CLI build rejects
replacement of an existing direct-install cache, the installer provides an
explicit, narrowly checked recovery path:

```powershell
.\Install-AutoDev.ps1 -RepairOwnedDirectCache
```

This option checks the existing AutoDev registration, source location, immutable
source fingerprint, and every cached source file. It refuses linked files,
unexpected contents, and local modifications. Only the verified static cache
copy is removed, without `-Force` or ACL changes, and the native manager
reinstalls it. Project state, immutable releases, authentication, and unrelated
configuration are not removed or edited by the recovery step.

The tested app build exposes plugin agents but does not expose plugin-bundled
skills to its skill loader. For the app, the installer also creates a personal
`autodev` skill link to the same immutable release, not a separate copy.
Fresh app sessions then support `/autodev`; already-running sessions retain
their earlier skill catalog. Existing unrelated personal skills are untouched,
and a conflicting regular `autodev` directory is never overwritten.

The current CLI accepts direct local plugin installation but warns that this
form is deprecated for a future release. There is no marketplace publication;
a future CLI migration may require a local marketplace registration.

Use `-HostTarget CLI` or `-HostTarget App` to install only one host. A partial
installation error is reported explicitly; a successful first host is not
silently undone. No cached releases are deleted automatically.

For development without persistent registration:

```powershell
$plugin = (Resolve-Path .\tkapin-autodev).Path
copilot --plugin-dir $plugin --add-dir $plugin --agent tkapin-autodev:autodev
```

The narrow `--add-dir` grant permits the bundled helper. Do not use
`--allow-all-paths` merely to make the plugin work. Interactive hosts may
instead ask for that specific path permission.

## One entry point

In a target-project session, use:

```text
/autodev Build a small tool that ...
/autodev inspect
/autodev resume
/autodev improve the way this project reports progress
```

These are natural-language requests to the `autodev` skill. The skill makes the
current assistant act as GM; it does not itself change the host model. Select
the `tkapin-autodev:autodev` custom agent when you want the packaged GM model
configuration. In CLI:

```powershell
copilot --agent tkapin-autodev:autodev
```

The GM clarifies intent, uses BA/Architect/PM, and presents a concise
specification/architecture/plan package for Client approval before coding.
It then delegates bounded delivery, independent review/testing, and audits.
Only material choices need Client attention. Pending audit work still blocks
the next sprint unless the Client grants a specific exception.

## What persists

Each target project gets `.autodev/state.sqlite3`. It contains current work
state, immutable artifact versions, attributed feedback/evidence, and an
append-only event journal. SQLite transactions keep state and journal
consistent. Preserve that directory to resume; do not reset it to escape
failed checks. Back it up with the project's other important local artifacts.

Add `.autodev/` to the target project's ignore rules unless you have an explicit
private-artifact retention policy. It can contain Client requirements and
feedback. Do not publish it or raw Copilot transcripts automatically.

The helper has no server and no network connection. To inspect directly, use
the helper path reported by the loaded skill:

```powershell
python "<skill-root>\scripts\autodev.py" status --project "<project>"
python "<skill-root>\scripts\autodev.py" inspect --project "<project>"
python "<skill-root>\scripts\autodev.py" help
```

For bounded task evidence, call `focus` with an input such as
`{"task":"task-3","limit":20}`. It returns current work and transitive dependencies,
active guidance, audit obligations, and separate pages of sprint feedback and
current-run events. It is explicitly partial, not a replacement for approved
specifications or a complete audit. Follow its cursors with `expected_revision`;
restart paging if the revision changes. Full `context` and global `journal`
reads remain available. CLI output is UTF-8, including redirected Windows output.

Mutations accept UTF-8 JSON via `--input <file>`. Prefer files over complex
shell quoting. The [operating guide](tkapin-autodev/skills/autodev/references/operating-guide.md)
describes the action sequence and evidence fields.

## Self-improvement boundary

Project-local role guidance and Python tools can be proposed, independently
evaluated, adopted at safe boundaries, and reverted. The current active
versions are part of the context supplied to future assignments. Generated
tool files are immutable views of versioned content, not a second source of
truth.

Shared-plugin improvements remain proposals until the Client approves the
exact candidate. Approval permits a separate source-change, verification, and
installation workflow; the helper never changes its own installation.
Installation permission is not blanket approval of all future updates.

No improvement may redefine governing principles, model/tool permissions,
Client commitments, acceptance authority, or audit gates. Actor labels and
decision evidence are supplied by the trusted host: the helper is not an
identity provider or a sandbox against an agent with arbitrary shell access.

## Validation commands

Offline tests from the PoC directory:

```powershell
python -m unittest discover -s .\tests -v
```

Live trials consume existing Copilot quota and are opt-in:

```powershell
python .\tests\live_trial.py --project .\.trial-output\my-new-trial
```

The target must be empty; the runner never deletes previous work. It invokes
the real plugin, checks actual delivery behavior, and verifies a project-local
tool plus the shared-approval gate. The fixture uses a synthetic Client mandate
for its narrowly defined disposable project, not approval for other projects.
Raw transcripts/usage remain local under the ignored trial directory.
See [the validation report](VALIDATION.md) for the actual completed checks and
observed host limitations.

If a trial stops on a fixable host blocker, preserve the project and resume its
known session with `--resume <session-id>`. `--verify-only` reruns external
checks without starting a model. Exit code zero from Copilot alone is not
considered proof that the trial succeeded.

## Current limits

- Local projects and host-native execution; no distributed scheduler.
- Regular-file evidence snapshots, not filesystem sandboxing or automatic
  deletion/rename tracking. Review the actual Git diff for omitted changes.
- Conservative approval of changed package versions; no automatic semantic
  classification of whether a requirement change is material.
- Actor identities, model names, actual Client decisions, and test execution
  are host/operator assertions. The helper detects inconsistent records but
  cannot authenticate a human or independently prove arbitrary shell output.
- A missing mandatory audit or unavailable permitted model remains a blocker.
  The framework never fabricates success to get past it.
- This CLI build returned access denied when replacing/removing an existing
  direct-install cache on the test machine. Identical-content installation is
  a verified no-op. The explicit owned-cache recovery option successfully
  installed the reviewed patch without changing ACLs or clearing user state.
- Before 0.1.1, submissions did not record chronological precedence. Existing
  non-overlapping or identical snapshots remain usable. Ambiguous legacy
  overlapping hashes require fresh submission/review; the helper does not
  guess their order. Follow-up audits retain earlier finding obligations.

## Uninstall

Remove the native registrations, leaving project history intact:

```powershell
copilot plugin uninstall tkapin-autodev
agency plugin uninstall tkapin-autodev --engine copilot
```

Use only the command for the host you installed. Project `.autodev` directories
and immutable cached releases are not deleted automatically.
For an app installation, also remove its personal skill link after checking
that it still points into this installer's release cache:

```powershell
$path = Join-Path $HOME ".copilot\skills\autodev"
$link = Get-Item -LiteralPath $path -Force
$root = [IO.Path]::GetFullPath((Join-Path $HOME ".autodev\releases")) + "\"
$comparison = [StringComparison]::OrdinalIgnoreCase
if ($link.LinkType -eq "Junction" -and
    ([string]$link.Target).StartsWith($root, $comparison)) {
    Remove-Item -LiteralPath $path -Force
} else {
    throw "Not an owned AutoDev junction; inspect rather than delete it."
}
```

This Windows command removes only the junction, not the release it points to.
