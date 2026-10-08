import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from pathlib import Path


PLUGIN = Path(os.environ.get("AUTODEV_PLUGIN_ROOT", Path(__file__).resolve().parents[1] / "tkapin-autodev"))
SCRIPTS = PLUGIN / "skills" / "autodev" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from autodev_core import ContractError, Engine, Store, digest  # noqa: E402


def actor(role, identity=None, model="gpt-5.4"):
    value = {"id": identity or f"context-{role}", "role": role}
    if role != "client":
        value["model"] = model
    return value


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.store = Store(self.project)
        self.call("init", "gm", intent="Build a local greeting CLI", limits={
            "max_sprints": 3, "max_tasks": 10, "max_attempts": 2,
        })

    def call(self, action, role="gm", identity=None, **data):
        return self.store.execute(action, {"actor": actor(role, identity), **data})["result"]

    def approved(self):
        versions = {}
        for kind, role in [("spec", "ba"), ("architecture", "architect"), ("plan", "pm")]:
            versions[kind] = self.call("artifact", role, kind=kind, content=f"Versioned {kind}")["version"]
        for model in ["gpt-5.4", "gpt-6-astra"]:
            self.store.execute("challenge-package", {
                "actor": actor("reviewer", f"package-{model}", model),
                "versions": versions, "passed": True, "evidence": "Independently checked package coherence",
            })
        return self.call("approve", "client", versions=versions, evidence="Client explicitly approved these versions")

    def sprint(self):
        self.approved()
        return self.call("start-sprint", goal="Deliver the greeting")["sprint"]

    def submitted(self, sprint, name="app.py", identity=None):
        task = self.call("add-task", "pm", sprint=sprint, title=f"Implement {name}", paths=[name])
        claim = self.call("claim", "developer", identity, task=task["id"], revision=0)
        (self.project / name).write_text("def greet(name):\n    return f'Hello, {name}!'\n", encoding="utf-8")
        submission = self.call("submit", "developer", identity, task=task["id"],
                               revision=claim["revision"], files=[name], evidence="Implemented and tested")
        return task["id"], claim["revision"], submission["digest"]

    def verified(self, sprint, name="app.py"):
        identifier, revision, fingerprint = self.submitted(sprint, name)
        for role in ["reviewer", "tester"]:
            self.call("review", role, task=identifier, revision=revision, digest=fingerprint,
                      passed=True, evidence=f"{role}: inspected exact artifact and ran applicable checks")
        return identifier, revision, fingerprint

    def finished(self):
        sprint = self.sprint()
        self.verified(sprint)
        fingerprint = self.store.execute("status")["sprints"][-1]["submission_digest"]
        self.call("integrate", "tester", sprint=sprint, digest=fingerprint, passed=True,
                  evidence="Integrated CLI and regression checks passed")
        self.call("finish-sprint", sprint=sprint, outcome="success", reason="Verified increment")
        return sprint, fingerprint

    def audit(self, scope, **changes):
        data = {
            "scope": scope, "digest": self.store.execute("status")["scope_digests"][scope],
            "examined": ["journal", "work", "verification"], "outstanding": [],
            "limitations": [], "findings": [], "evidence": "Examined scoped records and supporting evidence",
        }
        data.update(changes)
        return self.call("audit", "auditor", **data)

    def proposal(self, scope="project", content="Keep handoffs concise", target="pm", kind="guidance"):
        return self.call("propose-improvement", "auditor", scope=scope, kind=kind,
                         target=target, content=content, benefit="Reduce repeated coordination work")

    def evaluate(self, item, passed=True):
        return self.call("evaluate-improvement", "reviewer", improvement=item["id"],
                         digest=item["digest"], passed=passed, evidence="Independent before/after case comparison")

    def test_current_state_and_journal_are_atomic_on_failure(self):
        before = self.store.execute("status")
        events = self.store.execute("journal")
        with self.assertRaises(ContractError):
            self.call("start-sprint", goal="Unauthorized execution")
        self.assertEqual(before, self.store.execute("status"))
        self.assertEqual(events, self.store.execute("journal"))

    def test_restart_reads_the_same_state(self):
        self.sprint()
        self.assertEqual(self.store.execute("status"), Store(self.project).execute("status"))

    def test_journal_rejects_update_and_delete(self):
        with closing(sqlite3.connect(self.store.path)) as db, db:
            for sql in ["DELETE FROM events", "UPDATE events SET action='edited'"]:
                with self.assertRaises(sqlite3.IntegrityError):
                    db.execute(sql)

    def test_event_write_failure_rolls_back_current_state(self):
        before = self.store.execute("status")
        with closing(sqlite3.connect(self.store.path)) as db, db:
            db.execute("CREATE TRIGGER fail_pause BEFORE INSERT ON events WHEN NEW.action='pause' "
                       "BEGIN SELECT RAISE(ABORT, 'simulated journal failure'); END")
        with self.assertRaises(sqlite3.IntegrityError):
            self.call("pause", reason="Must not persist without its event")
        self.assertEqual(self.store.execute("status"), before)

    def test_approval_is_client_only_and_exact_version(self):
        self.approved()
        self.call("artifact", "ba", kind="spec", content="New behavior")
        with self.assertRaises(ContractError):
            self.call("start-sprint", goal="Use unapproved revision")
        with self.assertRaises(ContractError):
            self.call("approve", versions={"spec": 2, "architecture": 1, "plan": 1}, evidence="GM thinks yes")
        with self.assertRaises(ContractError):
            self.call("approve", "client", versions={"spec": 1, "architecture": 1, "plan": 1}, evidence="Old spec")

    def test_models_and_context_roles_are_explicit(self):
        with self.assertRaises(ContractError):
            self.store.execute("pause", {"actor": actor("gm", model="claude-opus-5"), "reason": "test"})
        for model in ["auto", "Auto", " AUTO "]:
            with self.subTest(model=model), self.assertRaises(ContractError):
                self.store.execute("pause", {"actor": actor("gm", model=model), "reason": "test"})
        for role in [[], {}, None, False]:
            with self.subTest(role=role), self.assertRaises(ContractError):
                self.store.execute("pause", {"actor": {"id": "invalid-role", "role": role}, "reason": "test"})
        with self.assertRaises(ContractError):
            self.call("artifact", "ba", identity="context-gm", kind="spec", content="Persona switch")

    def test_package_requires_distinct_models_and_preserves_blockers(self):
        versions = {}
        for kind, role in [("spec", "ba"), ("architecture", "architect"), ("plan", "pm")]:
            versions[kind] = self.call("artifact", role, kind=kind, content="Ready package")["version"]
        for identity in ["review-one", "review-two"]:
            self.call("challenge-package", "reviewer", identity, versions=versions,
                      passed=True, evidence="Same model, separate contexts")
        with self.assertRaises(ContractError):
            self.call("approve", "client", versions=versions, evidence="Ready")
        self.store.execute("challenge-package", {
            "actor": actor("reviewer", "third", "gpt-6-astra"), "versions": versions,
            "passed": False, "evidence": "Material unresolved behavior",
        })
        with self.assertRaises(ContractError):
            self.call("approve", "client", versions=versions, evidence="Ignore dissent")
        self.store.execute("challenge-package", {
            "actor": actor("reviewer", "third", "gpt-6-astra"), "versions": versions,
            "passed": True, "evidence": "Resolved using an existing explicit criterion; no changes needed",
        })
        self.call("approve", "client", versions=versions, evidence="Client accepts resolved package")

    def test_stale_assignment_cannot_submit(self):
        sprint = self.sprint()
        task = self.call("add-task", "pm", sprint=sprint, title="File", paths=["app.py"])
        self.call("claim", "developer", task=task["id"], revision=0)
        (self.project / "app.py").write_text("old", encoding="utf-8")
        self.call("reassign", "pm", task=task["id"], revision=1, reconciled=True, reason="Worker stopped")
        self.call("claim", "developer", "replacement", task=task["id"], revision=2)
        with self.assertRaises(ContractError):
            self.call("submit", "developer", task=task["id"], revision=1, files=["app.py"], evidence="Late result")

    def test_conflicting_writers_are_rejected_but_disjoint_work_is_allowed(self):
        sprint = self.sprint()
        tasks = [self.call("add-task", "pm", sprint=sprint, title=p, paths=[p])
                 for p in ["src", "src/main.py", "tests"]]
        self.call("claim", "developer", task=tasks[0]["id"], revision=0)
        with self.assertRaises(ContractError):
            self.call("claim", "developer", "second", task=tasks[1]["id"], revision=0)
        self.call("claim", "developer", "third", task=tasks[2]["id"], revision=0)

    def test_concurrent_claim_has_exactly_one_winner(self):
        sprint = self.sprint()
        task = self.call("add-task", "pm", sprint=sprint, title="File", paths=["app.py"])

        def claim(identity):
            try:
                Store(self.project).execute("claim", {
                    "actor": actor("developer", identity), "task": task["id"], "revision": 0,
                })
                return "claimed"
            except ContractError:
                return "rejected"

        with ThreadPoolExecutor(max_workers=2) as executor:
            self.assertCountEqual(list(executor.map(claim, ["one", "two"])), ["claimed", "rejected"])

    def test_dependencies_and_limits_are_enforced(self):
        sprint = self.sprint()
        first = self.call("add-task", "pm", sprint=sprint, title="First", paths=["one.py"])
        second = self.call("add-task", "pm", sprint=sprint, title="Second", paths=["two.py"],
                           depends_on=[first["id"]])
        with self.assertRaises(ContractError):
            self.call("claim", "developer", task=second["id"], revision=0)
        for _ in range(2):
            revision = self.store.execute("status")["sprints"][0]["tasks"][0]["revision"]
            self.call("claim", "developer", task=first["id"], revision=revision)
            self.call("reassign", "pm", task=first["id"], revision=revision + 1,
                      reconciled=True, reason="Recovery")
        revision = self.store.execute("status")["sprints"][0]["tasks"][0]["revision"]
        with self.assertRaises(ContractError):
            self.call("claim", "developer", task=first["id"], revision=revision)

    def test_path_traversal_and_metadata_scopes_are_rejected(self):
        sprint = self.sprint()
        for path in ["../outside", "..\\outside", "C:\\outside", "/outside", ".git/config", ".AUTODEV/state.sqlite3"]:
            with self.subTest(path=path), self.assertRaises(ContractError):
                self.call("add-task", "pm", sprint=sprint, title="Bad scope", paths=[path])

    def test_linked_file_evidence_is_rejected(self):
        target = self.project / "real.py"
        target.write_text("data", encoding="utf-8")
        link = self.project / "alias.py"
        try:
            link.symlink_to(target)
        except OSError as error:
            self.skipTest(f"Symlinks unavailable: {error}")
        with self.assertRaises(ContractError):
            self.store.snapshot(["alias.py"])

    @unittest.skipUnless(sys.platform == "win32", "Windows junction test")
    def test_windows_junction_evidence_is_rejected(self):
        executable = shutil.which("pwsh")
        if executable is None:
            self.skipTest("PowerShell 7 is unavailable")
        real = self.project / "real"
        real.mkdir()
        (real / "code.py").write_text("print('real')", encoding="utf-8")
        env = os.environ | {"AUTODEV_TEST_LINK": str(self.project / "linked"),
                            "AUTODEV_TEST_TARGET": str(real)}
        result = subprocess.run(
            [executable, "-NoProfile", "-NonInteractive", "-Command",
             "New-Item -ItemType Junction -Path $env:AUTODEV_TEST_LINK -Target $env:AUTODEV_TEST_TARGET | Out-Null"],
            env=env, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        with self.assertRaises(ContractError):
            self.store.snapshot(["linked/code.py"])

    def test_self_review_and_stale_evidence_are_rejected(self):
        sprint = self.sprint()
        identifier, revision, fingerprint = self.submitted(sprint)
        with self.assertRaises(ContractError):
            self.call("review", "tester", "context-developer", task=identifier, revision=revision,
                      digest=fingerprint, passed=True, evidence="Self review")
        (self.project / "app.py").write_text("changed", encoding="utf-8")
        with self.assertRaises(ContractError):
            self.call("review", "tester", task=identifier, revision=revision,
                      digest=fingerprint, passed=True, evidence="Old result")

    def test_failed_review_routes_bounded_rework(self):
        sprint = self.sprint()
        identifier, revision, fingerprint = self.submitted(sprint)
        self.call("review", "reviewer", task=identifier, revision=revision, digest=fingerprint,
                  passed=False, evidence="Reproducible defect")
        task = self.store.execute("status")["sprints"][0]["tasks"][0]
        self.assertEqual(task["status"], "ready")
        claim = self.call("claim", "developer", task=identifier, revision=revision)
        self.assertEqual(claim["revision"], revision + 1)

    def test_task_success_is_not_integration(self):
        sprint = self.sprint()
        self.verified(sprint)
        with self.assertRaises(ContractError):
            self.call("finish-sprint", sprint=sprint, outcome="success", reason="All tasks green")

    def test_changed_files_invalidate_integrated_evidence(self):
        sprint, _ = self.finished()
        (self.project / "app.py").write_text("changed after verification", encoding="utf-8")
        with self.assertRaises(ContractError):
            self.call("accept", "client", sprint=sprint, digest="anything", evidence="Accept")

    def test_incomplete_audit_pauses_next_sprint(self):
        sprint, _ = self.finished()
        report = self.audit(sprint, examined=["work", "verification"], outstanding=["Recover journal export"])
        self.assertFalse(report["complete"])
        with self.assertRaises(ContractError):
            self.call("start-sprint", goal="Next increment")
        self.audit(sprint)
        self.call("start-sprint", goal="Next increment")

    def test_missing_supplemental_feedback_does_not_block_completed_audit(self):
        sprint, _ = self.finished()
        report = self.audit(sprint, limitations=["Developer feedback unavailable; objective examination completed"])
        self.assertTrue(report["complete"])
        self.call("start-sprint", goal="Next increment")

    def test_client_exception_is_specific_and_preserves_audit_debt(self):
        sprint, _ = self.finished()
        self.call("audit-exception", "client", sprint=sprint, reason="Bounded continuation",
                  next_goal="Allowed increment", recovery_owner="Auditor replacement")
        with self.assertRaises(ContractError):
            self.call("start-sprint", goal="A different increment")
        self.call("start-sprint", goal="Allowed increment")
        self.assertEqual(self.store.execute("status")["sprints"][0]["audit"], "pending")

    def test_audit_findings_need_disposition_and_exceptions_do_not_waive_blockers(self):
        sprint, _ = self.finished()
        report = self.audit(sprint, findings=[{
            "id": "F1", "summary": "Unresolved authorization", "evidence": "Decision record",
            "blocking": True,
        }])
        with self.assertRaises(ContractError):
            self.call("start-sprint", goal="Next")
        self.call("disposition", scope=sprint, audit=report["id"], finding="F1",
                  decision="deferred", reason="Later")
        with self.assertRaises(ContractError):
            self.call("start-sprint", goal="Next")
        self.call("disposition", scope=sprint, audit=report["id"], finding="F1",
                  decision="resolved", reason="Client decision recorded and conflict reconciled")
        self.call("start-sprint", goal="Next")

    def test_incomplete_followup_cannot_hide_an_older_blocker(self):
        sprint, _ = self.finished()
        first = self.audit(sprint, findings=[{
            "id": "F1", "summary": "Known blocker", "evidence": "Unresolved required decision",
            "blocking": True,
        }])
        self.audit(sprint, examined=["verification"], outstanding=["Journal review not finished"])
        self.call("audit-exception", "client", sprint=sprint, reason="Bounded recovery",
                  next_goal="Recovery", recovery_owner="auditor")
        with self.assertRaisesRegex(ContractError, "audit-1/F1"):
            self.call("start-sprint", goal="Recovery")
        self.call("disposition", scope=sprint, audit=first["id"], finding="F1",
                  decision="resolved", reason="Required decision obtained; not waived by exception")
        self.call("start-sprint", goal="Recovery")

    def test_complete_followup_and_run_audit_preserve_older_finding_obligations(self):
        sprint, fingerprint = self.finished()
        first = self.audit(sprint, findings=[{
            "id": "F1", "summary": "Unresolved observation", "evidence": "Handoff record",
            "blocking": False,
        }])
        self.audit(sprint)
        with self.assertRaisesRegex(ContractError, "audit-1/F1"):
            self.call("start-sprint", goal="Next")
        self.call("disposition", scope=sprint, audit=first["id"], finding="F1",
                  decision="deferred", reason="Recorded for a later improvement run")
        self.call("accept", "client", sprint=sprint, digest=fingerprint, evidence="Accepted")
        self.call("finish-run", outcome="success", reason="Delivered")
        run_first = self.audit("run", findings=[{
            "id": "R1", "summary": "Closure blocker", "evidence": "Outstanding handover",
            "blocking": True,
        }])
        self.audit("run")
        with self.assertRaisesRegex(ContractError, "run/audit-1/R1"):
            self.call("close", handover="Premature")
        self.call("disposition", scope="run", audit=run_first["id"], finding="R1",
                  decision="resolved", reason="Handover completed and verified")
        self.call("close", handover="Completed")

    def test_acceptance_and_full_closure_are_distinct(self):
        sprint, fingerprint = self.finished()
        self.call("accept", "client", sprint=sprint, digest=fingerprint, evidence="Client accepts delivered version")
        self.call("finish-run", outcome="success", reason="Delivered")
        with self.assertRaises(ContractError):
            self.call("close", handover="Files and instructions")
        self.audit(sprint)
        self.audit("run")
        self.call("close", handover="Files, evidence, and improvement report")
        self.assertTrue(self.store.execute("status")["closed"])

    def test_failed_discovery_still_requires_a_run_audit(self):
        self.call("finish-run", outcome="cancelled", reason="Client withdrew before implementation")
        with self.assertRaises(ContractError):
            self.call("close", handover="Discovery notes")
        self.audit("run")
        self.call("close", handover="Discovery and cancellation findings")

    def test_reopen_preserves_history_and_invalidates_acceptance(self):
        sprint, fingerprint = self.finished()
        self.call("accept", "client", sprint=sprint, digest=fingerprint, evidence="Accepted")
        self.call("finish-run", outcome="success", reason="Delivered")
        self.audit(sprint)
        self.audit("run")
        self.call("reopen", reconciled=True, reason="New evidence of defect")
        status = self.store.execute("status")
        self.assertFalse(status["accepted"])
        self.assertIsNone(status["outcome"])
        self.assertEqual(status["sprints"][0]["audit"], "stale")
        self.assertIn("accept", [event["action"] for event in self.store.execute("journal")["events"]])

    def test_improvement_requires_independence_and_supports_revert(self):
        item = self.proposal()
        with self.assertRaises(ContractError):
            self.call("adopt-improvement", improvement=item["id"])
        with self.assertRaises(ContractError):
            self.call("evaluate-improvement", "reviewer", "context-auditor", improvement=item["id"],
                      digest=item["digest"], passed=True, evidence="Self-evaluation")
        self.evaluate(item)
        self.call("adopt-improvement", improvement=item["id"])
        self.assertEqual(self.store.execute("status")["active_improvements"]["guidance:pm"], item["id"])
        self.call("revert-improvement", improvement=item["id"], reason="Observed regression")
        self.assertEqual(self.store.execute("status")["active_improvements"], {})

    def test_improvement_rejects_stale_candidate_and_baseline(self):
        first, second = self.proposal(), self.proposal(content="A different candidate")
        with self.assertRaises(ContractError):
            self.call("evaluate-improvement", "reviewer", improvement=first["id"],
                      digest=second["digest"], passed=True, evidence="Wrong content")
        self.evaluate(first)
        self.evaluate(second)
        self.call("adopt-improvement", improvement=first["id"])
        with self.assertRaises(ContractError):
            self.call("adopt-improvement", improvement=second["id"])

    def test_finished_failed_submissions_do_not_block_project_learning(self):
        first = self.proposal()
        self.evaluate(first)
        self.call("adopt-improvement", improvement=first["id"])
        sprint = self.sprint()
        task, _, _ = self.submitted(sprint)
        self.call("finish-sprint", sprint=sprint, outcome="failed", reason="Stop before remaining verification")
        self.audit(sprint)
        self.call("start-sprint", goal="Recovery", recovery_plan="New bounded implementation assignment")
        second = self.proposal(content="Improved project guidance after the failed sprint")
        self.evaluate(second)
        self.call("adopt-improvement", improvement=second["id"])
        self.call("revert-improvement", improvement=second["id"], reason="Restore prior guidance")
        self.call("revert-improvement", improvement=first["id"], reason="Return to shipped baseline")
        state = self.store.execute("context")["state"]
        self.assertEqual(state["sprints"][0]["tasks"][0]["id"], task)
        self.assertEqual(state["sprints"][0]["tasks"][0]["status"], "submitted")
        self.assertEqual(state["active_improvements"], {})

    def test_real_active_submissions_still_block_adoption_and_revert(self):
        first = self.proposal()
        self.evaluate(first)
        self.call("adopt-improvement", improvement=first["id"])
        second = self.proposal(content="Next guidance")
        self.evaluate(second)
        sprint = self.sprint()
        self.submitted(sprint)
        with self.assertRaisesRegex(ContractError, "active contracts"):
            self.call("adopt-improvement", improvement=second["id"])
        with self.assertRaisesRegex(ContractError, "active assignments"):
            self.call("revert-improvement", improvement=first["id"], reason="Not yet safe")

    def test_serialized_overlapping_snapshots_use_submission_not_creation_order(self):
        sprint = self.sprint()
        for order in [(0, 1), (1, 0)]:
            with self.subTest(order=order):
                tasks = [self.call("add-task", "pm", sprint=sprint, title=f"Edit {index}",
                                   paths=["shared.py"]) for index in range(2)]
                for index in order:
                    task = tasks[index]
                    claim = self.call("claim", "developer", task=task["id"], revision=0)
                    (self.project / "shared.py").write_text(f"VALUE = {task['id']!r}\n", encoding="utf-8")
                    submission = self.call("submit", "developer", task=task["id"], revision=claim["revision"],
                                           files=["shared.py"], evidence="Serialized change")
                    for role in ["reviewer", "tester"]:
                        self.call("review", role, task=task["id"], revision=claim["revision"],
                                  digest=submission["digest"], passed=True, evidence="Checked this exact revision")
                expected = digest(self.store.snapshot(["shared.py"]))
                status = self.store.execute("status")["sprints"][0]
                self.assertEqual(status["submission_digest"], expected)
                self.assertIsNone(status["submission_blocker"])
                self.call("integrate", "tester", sprint=sprint, digest=expected,
                          passed=True, evidence="Combined behavior checked")
        state = self.store.execute("context")["state"]
        submissions = {e["body"]["request"]["task"]: e["seq"]
                       for e in self.store.execute("journal")["events"] if e["action"] == "submit"}
        for task in state["sprints"][0]["tasks"]:
            self.assertEqual(task["submission"]["sequence"], submissions[task["id"]])

    def test_legacy_overlaps_are_reported_without_guessing_order(self):
        sprint = {"tasks": [
            {"status": "verified", "submission": {"files": {"shared.py": "older"}}},
            {"status": "verified", "submission": {"files": {"shared.py": "newer"}}},
        ]}
        engine = Engine(self.store, self.store.load()[1], actor("gm"))
        with self.assertRaisesRegex(ContractError, "legacy"):
            engine.recorded_snapshot(sprint)
        status = engine.submission_status(sprint)
        self.assertIsNone(status["submission_digest"])
        self.assertIn("reassign and resubmit", status["submission_blocker"])
        sprint["tasks"][1]["submission"]["files"]["shared.py"] = "older"
        self.assertEqual(engine.recorded_snapshot(sprint), {"shared.py": "older"})

    def test_shared_improvement_never_writes_plugin_and_requires_client_handoff(self):
        before = (SCRIPTS / "autodev_core.py").read_bytes()
        item = self.proposal(scope="shared")
        self.evaluate(item)
        with self.assertRaises(ContractError):
            self.call("adopt-improvement", improvement=item["id"])
        with self.assertRaises(ContractError):
            self.call("handoff-shared", improvement=item["id"])
        with self.assertRaises(ContractError):
            self.call("approve-shared", improvement=item["id"], digest=item["digest"], evidence="GM says yes")
        self.call("approve-shared", "client", improvement=item["id"], digest=item["digest"],
                  evidence="Client approves separate source-change work")
        result = self.call("handoff-shared", improvement=item["id"])
        self.assertEqual(result["status"], "approved_for_source_change")
        self.assertEqual(before, (SCRIPTS / "autodev_core.py").read_bytes())

    def test_materialized_tool_is_content_addressed_and_preserves_tampering(self):
        item = self.proposal(kind="tool", target="summary.py", content="print('summary')\n")
        result = self.store.execute("materialize", {"improvement": item["id"]})
        path = Path(result["path"])
        self.assertTrue(path.is_relative_to(self.project / ".autodev"))
        self.assertEqual(path.read_text(encoding="utf-8"), "print('summary')\n")
        path.write_text("unexpected edit", encoding="utf-8")
        with self.assertRaises(ContractError):
            self.store.execute("materialize", {"improvement": item["id"]})
        self.assertEqual(path.read_text(), "unexpected edit")

    def test_new_run_retains_previous_outcomes_and_project_learning(self):
        item = self.proposal()
        self.evaluate(item)
        self.call("adopt-improvement", improvement=item["id"])
        self.call("finish-run", outcome="cancelled", reason="Changed priority")
        self.audit("run")
        self.call("close", handover="Recorded cancellation and learning")
        self.call("new-run", intent="Next request")
        state = self.store.execute("context")["state"]
        self.assertEqual(state["run"], 2)
        self.assertEqual(state["past_runs"][0]["outcome"], "cancelled")
        self.assertEqual(state["active_improvements"]["guidance:pm"], item["id"])

    def test_pause_prevents_execution_and_resume_requires_reconciliation(self):
        sprint = self.sprint()
        task = self.call("add-task", "pm", sprint=sprint, title="Task", paths=["app.py"])
        self.call("pause", reason="Client decision outstanding")
        with self.assertRaises(ContractError):
            self.call("claim", "developer", task=task["id"], revision=0)
        with self.assertRaises(ContractError):
            self.call("resume", reconciled=False, reason="Guess")
        self.call("resume", reconciled=True, reason="Owners/effects/authority checked")
        self.call("claim", "developer", task=task["id"], revision=0)

    def test_pause_allows_reconciling_workers_before_cancellation(self):
        sprint = self.sprint()
        task = self.call("add-task", "pm", sprint=sprint, title="Task", paths=["app.py"])
        self.call("claim", "developer", task=task["id"], revision=0)
        self.call("pause", reason="Stop requested")
        self.call("reassign", "pm", task=task["id"], revision=1, reconciled=True,
                  reason="Worker stopped before file write")
        self.call("finish-sprint", sprint=sprint, outcome="cancelled", reason="Client cancelled")
        self.call("finish-run", outcome="cancelled", reason="Client cancelled")
        with self.assertRaises(ContractError):
            self.call("reopen", reconciled=True, reason="GM changed its mind")
        self.call("reopen", "client", reconciled=True, reason="Client explicitly authorizes restart")

    def test_unapproved_artifact_revision_freezes_affected_execution(self):
        sprint = self.sprint()
        task = self.call("add-task", "pm", sprint=sprint, title="Task", paths=["app.py"])
        self.call("artifact", "ba", kind="spec", content="Changed acceptance")
        with self.assertRaises(ContractError):
            self.call("claim", "developer", task=task["id"], revision=0)

    def test_late_feedback_invalidates_prior_audit_scope(self):
        sprint, _ = self.finished()
        self.audit(sprint)
        self.call("feedback", "developer", sprint=sprint, summary="New evidence of a handoff problem")
        self.assertEqual(self.store.execute("status")["sprints"][0]["audit"], "stale")
        with self.assertRaises(ContractError):
            self.call("start-sprint", goal="Next")

    def test_auditor_feedback_does_not_recursively_invalidate_its_audit(self):
        sprint, _ = self.finished()
        self.audit(sprint)
        self.call("feedback", "auditor", sprint=sprint, summary="Audit itself was straightforward")
        self.assertEqual(self.store.execute("status")["sprints"][0]["audit"], "complete")

    def test_gm_feedback_before_audit_avoids_reaudit_without_waiving_late_evidence(self):
        sprint, _ = self.finished()
        self.call("feedback", sprint=sprint, summary="GM handoff before audit")
        self.audit(sprint, limitations=["Supplemental BA feedback unavailable"])
        state = self.store.execute("context")["state"]
        self.assertEqual(len(state["sprints"][0]["audits"]), 1)
        self.assertEqual(self.store.execute("status")["sprints"][0]["audit"], "complete")
        self.call("feedback", sprint=sprint, summary="New evidence must not be suppressed")
        self.assertEqual(self.store.execute("status")["sprints"][0]["audit"], "stale")
        with self.assertRaises(ContractError):
            self.call("start-sprint", goal="Cannot continue on a stale audit")

    def test_focus_matches_authoritative_work_dependencies_and_active_guidance(self):
        item = self.proposal(content="Use approved project preflight; retain independent checks")
        self.evaluate(item)
        self.call("adopt-improvement", improvement=item["id"])
        sprint = self.sprint()
        root = self.call("add-task", "pm", sprint=sprint, title="Root", paths=["root.py"])
        middle = self.call("add-task", "pm", sprint=sprint, title="Middle", paths=["middle.py"],
                           depends_on=[root["id"]])
        leaf = self.call("add-task", "pm", sprint=sprint, title="Leaf", paths=["leaf.py"],
                         depends_on=[middle["id"]])
        other = self.call("add-task", "pm", sprint=sprint, title="Other", paths=["other.py"])
        self.call("feedback", sprint=sprint, task=root["id"], summary="Dependency warning")
        before = self.store.execute("context")
        history = self.store.execute("journal")
        packet = self.store.execute("focus", {"task": leaf["id"]})
        state = before["state"]
        self.assertTrue(packet["partial"])
        self.assertTrue(packet["package_current"])
        self.assertEqual(packet["revision"], before["revision"])
        self.assertEqual(packet["policy"], state["policy"])
        self.assertEqual(packet["baseline"], state["baseline"])
        self.assertEqual(packet["scope_digests"], before["scope_digests"])
        self.assertEqual(packet["sprint"]["tasks"], state["sprints"][0]["tasks"][:3])
        self.assertEqual(packet["sprint"]["omitted_task_ids"], [other["id"]])
        self.assertEqual(packet["feedback"]["items"], state["feedback"])
        self.assertEqual(packet["active_improvements"]["guidance:pm"],
                         state["improvements"][item["id"]])
        self.assertEqual(self.store.execute("focus", {"sprint": sprint})["sprint"]["tasks"],
                         state["sprints"][0]["tasks"])
        self.assertEqual(before, self.store.execute("context"))
        self.assertEqual(history, self.store.execute("journal"))
        self.call("artifact", "ba", kind="spec", content="Unapproved new scope")
        self.assertFalse(self.store.execute("focus", {"task": leaf["id"]})["package_current"])

    def test_focus_pages_preserve_failed_attempts_and_unrelated_authority_events(self):
        sprint = self.sprint()
        task, revision, fingerprint = self.submitted(sprint)
        self.call("review", "tester", task=task, revision=revision, digest=fingerprint,
                  passed=False, evidence="Retained-handle race reproduced despite green suite")
        self.call("claim", "developer", task=task, revision=revision)
        for index in range(7):
            self.call("feedback", sprint=sprint, summary=f"Complete evidence {index}")
        self.call("pause", reason="Authority decision unrelated to a specific task")
        before = self.store.execute("context")
        request = {"task": task, "limit": 3}
        events, feedback = [], []
        while True:
            packet = self.store.execute("focus", request)
            self.assertLessEqual(len(packet["events"]["items"]), 3)
            self.assertLessEqual(len(packet["feedback"]["items"]), 3)
            events.extend(packet["events"]["items"])
            feedback.extend(packet["feedback"]["items"])
            if not packet["events"]["has_more"] and not packet["feedback"]["has_more"]:
                break
            request["expected_revision"] = packet["revision"]
            request["after"] = events[-1]["seq"] if events else 0
            request["feedback_after"] = len(feedback)
        self.assertEqual(events, self.store.execute("journal")["events"])
        self.assertEqual(feedback, before["state"]["feedback"])
        failure = next(event for event in events if event["action"] == "review")
        self.assertFalse(failure["body"]["request"]["passed"])
        self.assertIn("Retained-handle", failure["body"]["request"]["evidence"])
        self.assertEqual(packet["sprint"]["tasks"][0]["attempts"], 2)
        self.assertEqual(packet["sprint"]["tasks"][0]["reviews"], {})
        self.assertEqual(packet["paused"], before["state"]["paused"])
        self.assertEqual(packet["events"]["total"], len(events))
        self.assertEqual(packet["feedback"]["total"], len(feedback))
        self.assertEqual(before, self.store.execute("context"))
        with self.assertRaises(ContractError):
            self.call("claim", "developer", task=task, revision=2)

    def test_focus_retains_all_audit_findings_and_dispositions(self):
        sprint, _ = self.finished()
        report = self.audit(sprint, findings=[{
            "id": "provenance", "summary": "Artifact identity unresolved",
            "evidence": "Synthetic installed-byte mismatch", "blocking": True,
        }])
        self.call("disposition", scope=sprint, audit=report["id"], finding="provenance",
                  decision="scheduled", reason="Retained as unresolved")
        self.audit(sprint)
        packet = self.store.execute("focus", {"sprint": sprint})
        self.assertEqual(packet["sprint"]["audits"],
                         self.store.execute("context")["state"]["sprints"][0]["audits"])
        self.assertEqual(packet["sprint"]["audit_status"], "complete")
        with self.assertRaises(ContractError):
            self.call("start-sprint", goal="Cannot bypass old blocking findings")

    def test_focus_validates_selectors_limits_and_revision_bound_cursors(self):
        sprint = self.sprint()
        revision = self.store.execute("context")["revision"]
        invalid = [
            {}, {"task": "task-404"}, {"sprint": "sprint-404"},
            {"sprint": sprint, "task": "task-1"}, {"sprint": []},
            {"sprint": sprint, "unknown": True}, {"sprint": sprint, "limit": 0},
            {"sprint": sprint, "limit": 201}, {"sprint": sprint, "limit": True},
            {"sprint": sprint, "after": -1}, {"sprint": sprint, "after": 1},
            {"sprint": sprint, "feedback_after": 1},
            {"sprint": sprint, "expected_revision": revision + 1},
            {"sprint": sprint, "after": revision + 1, "expected_revision": revision},
            {"sprint": sprint, "feedback_after": 1, "expected_revision": revision},
        ]
        before = self.store.execute("context")
        for request in invalid:
            with self.subTest(request=request), self.assertRaises(ContractError):
                self.store.execute("focus", request)
        empty = self.store.execute("focus", {
            "sprint": sprint, "after": revision, "expected_revision": revision, "limit": 200,
        })
        self.assertEqual(empty["events"]["items"], [])
        self.assertEqual(empty["feedback"]["items"], [])
        self.assertIsNone(empty["events"]["next_after"])
        self.assertIsNone(empty["feedback"]["next_feedback_after"])
        self.assertEqual(before, self.store.execute("context"))
        self.call("feedback", sprint=sprint, summary="New state between pages")
        with self.assertRaisesRegex(ContractError, "Stale focus revision"):
            self.store.execute("focus", {"sprint": sprint, "after": 1, "expected_revision": revision})

    def test_focus_history_pages_beyond_legacy_journal_ceiling(self):
        sprint = self.sprint()
        for index in range(205):
            self.call("feedback", sprint=sprint, summary=f"Event {index}")
        first = self.store.execute("focus", {"sprint": sprint, "limit": 200})
        second = self.store.execute("focus", {
            "sprint": sprint, "limit": 200, "expected_revision": first["revision"],
            "after": first["events"]["next_after"],
            "feedback_after": first["feedback"]["next_feedback_after"],
        })
        self.assertFalse(second["events"]["has_more"])
        self.assertFalse(second["feedback"]["has_more"])
        events = first["events"]["items"] + second["events"]["items"]
        self.assertEqual(len(events), first["events"]["total"])
        self.assertEqual(len({event["seq"] for event in events}), len(events))
        self.assertEqual(len(first["feedback"]["items"] + second["feedback"]["items"]), 205)

    def test_focus_excludes_past_runs_but_keeps_global_history_available(self):
        sprint, fingerprint = self.finished()
        self.call("feedback", sprint=sprint, summary="Past-run feedback")
        self.audit(sprint)
        self.call("accept", "client", sprint=sprint, digest=fingerprint,
                  evidence="Synthetic Client acceptance of exact artifact")
        self.call("finish-run", outcome="success", reason="Synthetic run complete")
        self.audit("run")
        self.call("close", handover="Synthetic verified handover")
        self.call("new-run", intent="Next synthetic increment")
        sprint = self.sprint()
        packet = self.store.execute("focus", {"sprint": sprint})
        self.assertEqual(packet["run"], 2)
        self.assertTrue(all(event["run"] == 2 for event in packet["events"]["items"]))
        self.assertEqual(packet["feedback"]["items"], [])
        self.assertTrue(any(event["run"] == 1 for event in self.store.execute("journal")["events"]))
        self.assertTrue(self.store.execute("context")["state"]["past_runs"])

    def test_focus_reduces_fixture_payload_without_truncating_selected_evidence(self):
        sprint = self.sprint()
        self.call("artifact", "ba", kind="spec", content="Detailed fixture requirement. " * 1000)
        for index in range(25):
            self.call("feedback", sprint=sprint, summary=f"Evidence {index}: " + "x" * 100)
        context = self.store.execute("context")
        packet = self.store.execute("focus", {"sprint": sprint})
        self.assertEqual(len(packet["events"]["items"]), 20)
        self.assertEqual(len(packet["feedback"]["items"]), 20)
        self.assertTrue(packet["events"]["has_more"])
        self.assertTrue(packet["feedback"]["has_more"])
        self.assertLess(len(json.dumps(packet)), len(json.dumps(context)))
        self.assertEqual(packet["feedback"]["items"], context["state"]["feedback"][:20])
        self.assertEqual(packet["artifacts"]["spec"][-1]["digest"],
                         context["state"]["artifacts"]["spec"][-1]["digest"])
        self.assertFalse(packet["package_current"])

    def test_cli_pipes_unicode_json_and_errors_as_utf8(self):
        sprint = self.sprint()
        self.call("feedback", sprint=sprint, summary="Diagnostic \u2192 caf\u00e9 \u4e2d\u6587")
        env = dict(os.environ, PYTHONIOENCODING="cp1252", PYTHONUTF8="0")
        for action, data in [("context", {}), ("focus", {"sprint": sprint}), ("inspect", {})]:
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "autodev.py"), action, "--project", str(self.project),
                 "--data", json.dumps(data)], capture_output=True, env=env, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8"))
            self.assertIn("Diagnostic \u2192 caf\u00e9 \u4e2d\u6587", result.stdout.decode("utf-8"))
            if action != "inspect":
                json.loads(result.stdout.decode("utf-8"))
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "autodev.py"), "focus", "--project", str(self.project),
             "--data", json.dumps({"task": "\u2192"})], capture_output=True, env=env, check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("error", json.loads(result.stderr.decode("utf-8")))

    def test_cli_reads_json_files_and_reports_errors_nonzero(self):
        request = self.project / "request.json"
        request.write_text(json.dumps({"actor": actor("gm"), "goal": "No approval"}), encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPTS / "autodev.py"), "start-sprint",
                                 "--project", str(self.project), "--input", str(request)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 2)
        self.assertIn("approval", json.loads(result.stderr)["error"])
        result = subprocess.run([sys.executable, str(SCRIPTS / "autodev.py"), "inspect",
                                 "--project", str(self.project)], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0)
        self.assertIn("# AutoDev inspection", result.stdout)


if __name__ == "__main__":
    unittest.main()
