"""Explicitly invoked live Copilot trial. Not part of offline unittest discovery."""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "tkapin-autodev"
SCRIPTS = PLUGIN / "skills" / "autodev" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from autodev_core import ContractError, Store  # noqa: E402


def plugin_snapshot():
    return {
        str(path.relative_to(PLUGIN)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in PLUGIN.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


def prompt(project):
    return f"""Use /autodev as General Manager to conduct a small, real, local-only
disposable trial in {project}. The plugin root is {PLUGIN}; helper is
{SCRIPTS / 'autodev.py'}. Read the skill/guide, use the helper, and finish the
entire trial rather than only proposing a plan.

CLIENT MANDATE (synthetic test Client, not blanket authority for other projects):
The human user explicitly authorized small live disposable-project trials with
existing Copilot access. This fixture defines that trial's preapproved scope.
Build a Python standard-library greet.py CLI with --name defaulting to world.
For --name Ada print exactly Hello, Ada! and newline; omission prints
Hello, world!; --name "Grace Hopper" preserves the space; blank/whitespace-only
names exit 2 with an informative error. Include test_greet.py with unittest
checks for these requirements. No network, dependency installation, git push,
external publication, or edits outside this project. The shared plugin is
read-only. The test Client approves the package ONLY if it implements exactly
these criteria; record that scoped fixture decision with the actual versions.
The test Client accepts the finished artifact ONLY after actual independent
checks establish those criteria. Do not ask the absent human to repeat this
fixture decision, and do not infer new authority.

Use real separate host agent contexts, not simulated role personas. Explicitly
select non-Anthropic models: gpt-6-astra and gpt-5.4 are the permitted choices.
Use at most 12 initial role assignments and reuse their contexts for followups
where supported. Have BA, Architect, and PM supply concise artifacts. Two
independent package reviewers must actually use different permitted models.
Record actual context IDs (or documented assignment IDs linked to them) and
actual model names; never invent independence. Root GM uses its session ID.
Assign a stable tracking ID before each dispatch and link the returned native
agent ID in evidence; do not infer child identity from inherited environment.
The helper permits your trusted host to relay an agent's returned decision with
that actual agent's provenance. You need not force every agent to write JSON.

Initialize limits max_sprints=2, max_tasks=6, max_attempts=2. Use one sprint with
one small delivery task, independent Reviewer and Tester, integrated checks,
per-agent feedback, and a complete sprint audit. Keep artifacts short. Use the
native task tool and packaged custom roles where available; if nesting is
unavailable you may directly dispatch the bounded role work from the GM.

After inspecting actual progress/feedback, demonstrate a concrete project-local
tool improvement: a small work_summary.py whose summarize(status) function
returns task counts by status in tasks_by_status, audit_debt as the count of
sprint audits plus the run audit that are not 'complete', paused as a boolean,
and shared_pending as the count of shared improvement items without approval.
Its CLI takes one UTF-8 JSON status file path and prints that summary as JSON.
The tool must not mutate project state. Have an independent reviewer/tester
inspect it and exercise nonempty, empty, paused, pending/stale-audit, and
shared-proposal fixtures. Record the exact candidate/evaluation evidence, adopt
it project-locally at a safe boundary, and actually run it on current status.
This is functional correctness evidence, not a measured productivity claim.
Propose a separate shared-plugin guidance improvement but DO NOT approve or
apply it. Demonstrate that an unapproved shared handoff is rejected; record the
result without treating this expected rejection as a failed delivery.

Do improvement work and feedback before finish-run. Then record exact artifact
acceptance under the conditional fixture mandate, finish the run, commission
the final run audit, disposition findings, and close with a concise handover.
Audit-only feedback does not recursively require an audit. Pending ideas can
remain unimplemented. If a genuine capability or contract blocker remains,
report it with durable evidence instead of forging a successful closure.
Leave the working CLI, tests, .autodev state/journal, adopted tool, and short
handover. No need for extra framework, questionnaires, or lengthy reports.
"""


def verify(project):
    checks = []
    for args, expected, exit_code in [
        ([], "Hello, world!\n", 0),
        (["--name", "Ada"], "Hello, Ada!\n", 0),
        (["--name", "Grace Hopper"], "Hello, Grace Hopper!\n", 0),
        (["--name", "   "], None, 2),
        (["--name", ""], None, 2),
    ]:
        result = subprocess.run([sys.executable, str(project / "greet.py"), *args],
                                cwd=project, capture_output=True, text=True, check=False)
        if result.returncode != exit_code or (expected is not None and result.stdout != expected):
            raise RuntimeError(f"Greeting contract failed for {args}: {result.returncode}, {result.stdout!r}")
        if exit_code and not result.stderr.strip():
            raise RuntimeError("Blank-name rejection must include an informative error")
        checks.append({"args": args, "exit_code": result.returncode})
    tests = subprocess.run([sys.executable, "-m", "unittest", "-v", "test_greet"],
                           cwd=project, capture_output=True, text=True, check=False)
    if tests.returncode:
        raise RuntimeError(tests.stdout + tests.stderr)
    store = Store(project)
    state = store.execute("context")["state"]
    if not state["closed"] or state["outcome"] != "success":
        raise RuntimeError("The live run is not successfully closed")
    tools = [i for i in state["improvements"].values()
             if i["scope"] == "project" and i["kind"] == "tool" and i["status"] == "adopted"]
    shared = [i for i in state["improvements"].values() if i["scope"] == "shared"]
    if not tools or not shared or any(i["approval"] for i in shared):
        raise RuntimeError("Expected an adopted local tool and unapproved shared proposal")
    gm = next(a for a in state["contexts"].values() if a["role"] == "gm")
    # A closed run refuses mutations; check the shared gate on its unchanged current data.
    from autodev_core import Engine
    try:
        Engine(store, state, gm).do_handoff_shared({"improvement": shared[0]["id"]})
    except ContractError:
        gate_rejected = True
    else:
        raise RuntimeError("An unapproved shared proposal crossed its approval gate")
    tool = Path(store.execute("materialize", {"improvement": tools[0]["id"]})["path"])
    fixtures = [
        ({"sprints": [], "run_audit": "complete", "paused": None, "improvements": []},
         {"tasks_by_status": {}, "audit_debt": 0, "paused": False, "shared_pending": 0}),
        ({"sprints": [{"audit": "stale", "tasks": [{"status": "ready"}, {"status": "ready"},
                                                   {"status": "verified"}]}],
          "run_audit": "pending", "paused": "Client decision",
          "improvements": [{"scope": "shared", "approval": None},
                           {"scope": "shared", "approval": {"evidence": "approved"}},
                           {"scope": "project", "approval": None}]},
         {"tasks_by_status": {"ready": 2, "verified": 1}, "audit_debt": 2,
          "paused": True, "shared_pending": 1}),
    ]
    for index, (input_data, expected) in enumerate(fixtures):
        fixture = project / ".autodev" / f"external-check-{index}.json"
        fixture.write_text(json.dumps(input_data), encoding="utf-8")
        result = subprocess.run([sys.executable, str(tool), str(fixture)],
                                cwd=project, capture_output=True, text=True, check=False)
        if result.returncode or json.loads(result.stdout) != expected:
            raise RuntimeError(f"Adopted summary tool failed fixture {index}: {result.stdout} {result.stderr}")
    return {"greeting_checks": checks, "project_tests": tests.stderr.strip(),
            "closed": True, "local_tool": tools[0]["id"], "tool_fixtures_passed": len(fixtures),
            "shared_gate_rejected": gate_rejected, "state_revision": store.execute("status")["revision"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True, help="New empty disposable directory")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--resume", help="Resume this trial's existing Copilot session after resolving a blocker")
    args = parser.parse_args()
    project = args.project.resolve()
    if args.verify_only:
        print(json.dumps(verify(project), indent=2))
        return
    executable = shutil.which("copilot")
    if executable is None:
        raise SystemExit("Copilot CLI is required for an explicitly authorized live trial")
    project.mkdir(parents=True, exist_ok=True)
    if any(project.iterdir()) and not args.resume:
        raise SystemExit("Choose a new empty disposable project; existing work is never erased")
    before = plugin_snapshot()
    command = [
        executable, "-C", str(project), "--plugin-dir", str(PLUGIN), "--add-dir", str(PLUGIN),
        "--agent", "tkapin-autodev:autodev", "--model", "gpt-6-astra",
        "--no-custom-instructions", "--disable-builtin-mcps", "--no-remote",
        "--no-remote-export", "--allow-all-tools", "--no-ask-user",
        "--max-autopilot-continues", "20", "--mode", "autopilot",
        "--usage-output-file", str(project / f"usage-{time.time_ns()}.json"),
        "-p", prompt(project), "--silent",
    ]
    if args.resume:
        command += ["--resume", args.resume]
        command[command.index("-p") + 1] = (
            f"Resume the already authorized disposable AutoDev trial in {project}. "
            "Read durable status and trial-mandate.txt first. Do not reinitialize or repeat "
            "already verified planning/implementation. Complete the remaining sprint audit, "
            "independently evaluated project-local summary tool, unapproved shared proposal "
            "gate check, conditional fixture acceptance, final run audit, and closure. "
            "Use synchronous role calls when waiting on results, and continue the GM's work "
            "after each role result. Reuse known contexts for followups when available; keep "
            "within the original limit of 12 initial role assignments. Do not infer child "
            "context identity from inherited environment variables; preserve prior provenance "
            "and document aliases rather than rewriting earlier records. "
            "The plugin directory now has an explicit narrow path grant. The main operator "
            "updated instructions between invocations, not during active work; all prior "
            "project state and the original trial authority remain unchanged. "
            "Finish the actual authorized objective or report a concrete blocker, not "
            "merely the result of the last subagent. Shared-plugin edits remain unauthorized."
        )
    else:
        (project / "trial-mandate.txt").write_text(prompt(project), encoding="utf-8")
    with (project / "session.log").open("a", encoding="utf-8") as log:
        result = subprocess.run(command, cwd=project, stdout=log, stderr=subprocess.STDOUT, check=False)
    if plugin_snapshot() != before:
        raise RuntimeError("Live trial changed the shared plugin")
    if result.returncode:
        raise RuntimeError(f"Copilot exited {result.returncode}; inspect {project / 'session.log'}")
    receipt = verify(project)
    (project / "verification.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
