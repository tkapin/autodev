"""Local, transactional coordination for AutoDev. No model or network dependency."""

from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


class ContractError(ValueError):
    """An operation would violate the recorded workflow contract."""


ROLES = {"client", "gm", "ba", "architect", "pm", "developer", "reviewer", "tester", "auditor"}
DEFAULT_MODELS = ["gpt-6-astra", "gpt-5.4", "gpt-5.5", "grok-4.6", "gemini-3.8-flash"]
ARTIFACT_ROLES = {"spec": "ba", "architecture": "architect", "plan": "pm"}
AUDIT_REQUIREMENTS = ["journal", "work", "verification"]
READ_ACTIONS = {"status", "journal", "inspect", "context", "materialize"}
COMMANDS = {
    "init": ("gm client", "intent limits", "models"),
    "artifact": ("ba architect pm", "kind content", ""),
    "challenge-package": ("reviewer", "versions passed evidence", ""),
    "approve": ("client", "versions evidence", ""),
    "start-sprint": ("gm", "goal", "recovery_plan"),
    "add-task": ("gm pm", "sprint title paths", "depends_on"),
    "claim": ("developer", "task revision", ""),
    "submit": ("developer", "task revision files evidence", ""),
    "review": ("reviewer tester", "task revision digest passed evidence", ""),
    "reassign": ("gm pm", "task revision reconciled reason", ""),
    "integrate": ("tester", "sprint digest passed evidence", ""),
    "finish-sprint": ("gm", "sprint outcome reason", ""),
    "feedback": ("gm ba architect pm developer reviewer tester auditor", "sprint summary", "task"),
    "audit": ("auditor", "scope digest examined outstanding limitations findings evidence", ""),
    "disposition": ("gm", "scope audit finding decision reason", ""),
    "audit-exception": ("client", "sprint reason next_goal recovery_owner", ""),
    "accept": ("client", "sprint digest evidence", ""),
    "finish-run": ("gm", "outcome reason", ""),
    "close": ("gm", "handover", ""),
    "new-run": ("gm", "intent", ""),
    "pause": ("gm client", "reason", ""),
    "resume": ("gm", "reconciled reason", ""),
    "reopen": ("gm client", "reconciled reason", ""),
    "propose-improvement": ("gm ba architect pm developer reviewer tester auditor", "scope kind target content benefit", ""),
    "evaluate-improvement": ("reviewer tester", "improvement digest passed evidence", ""),
    "adopt-improvement": ("gm", "improvement", ""),
    "revert-improvement": ("gm", "improvement reason", ""),
    "approve-shared": ("client", "improvement digest evidence", ""),
    "handoff-shared": ("gm", "improvement", ""),
}


def encoded(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(value: Any) -> str:
    return hashlib.sha256(encoded(value).encode("utf-8")).hexdigest()


def text(data: dict, name: str) -> str:
    value = data.get(name)
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{name} must be a nonempty string")
    return value


def number(data: dict, name: str, minimum: int = 0) -> int:
    value = data.get(name)
    if type(value) is not int or value < minimum:
        raise ContractError(f"{name} must be an integer >= {minimum}")
    return value


def boolean(data: dict, name: str) -> bool:
    if type(data.get(name)) is not bool:
        raise ContractError(f"{name} must be true or false")
    return data[name]


def strings(data: dict, name: str, *, nonempty: bool = False) -> list[str]:
    value = data.get(name)
    if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
        raise ContractError(f"{name} must be an array of nonempty strings")
    if nonempty and not value:
        raise ContractError(f"{name} cannot be empty")
    if len(value) != len(set(value)):
        raise ContractError(f"{name} cannot contain duplicates")
    return value


def model_allowed(model: str) -> bool:
    return bool(model.strip()) and model.strip().casefold() != "auto" and not re.search("claude|anthropic", model, re.I)


def actor_from(data: dict) -> dict:
    actor = data.get("actor")
    if not isinstance(actor, dict):
        raise ContractError("actor must contain id, role, and (for agents) model")
    text(actor, "id")
    if text(actor, "role") not in ROLES:
        raise ContractError("Unknown actor role")
    if actor["role"] != "client" and not model_allowed(text(actor, "model")):
        raise ContractError("An explicit permitted non-Anthropic model is required; no Auto routing")
    return {k: actor[k] for k in ("id", "role", "model") if k in actor}


def new_state(intent: str, policy: dict, run: int = 1) -> dict:
    return {
        "schema": 1, "run": run, "intent": intent, "policy": policy,
        "artifacts": {kind: [] for kind in ARTIFACT_ROLES},
        "approvals": [], "package_reviews": [], "baseline": None, "sprints": [], "feedback": [],
        "improvements": {}, "active_improvements": {}, "run_audits": [],
        "acceptance": None, "outcome": None, "closed": False, "paused": None,
        "past_runs": [], "contexts": {},
    }


class Store:
    def __init__(self, project: str | Path):
        self.project = Path(project).resolve(strict=True)
        if not self.project.is_dir():
            raise ContractError("Project must be an existing directory")
        plugin = Path(__file__).resolve().parents[3]
        if self.project.is_relative_to(plugin):
            raise ContractError("A target project cannot be inside the shared plugin")
        self.directory = self.project / ".autodev"
        self.path = self.directory / "state.sqlite3"
        self._check_private_path(self.path)

    def _check_private_path(self, path: Path) -> None:
        if not path.is_relative_to(self.directory):
            raise ContractError("Generated paths must stay inside project .autodev")
        current = path
        while current != self.project:
            if current.is_symlink() or (current.exists() and current.resolve() != current.absolute()):
                raise ContractError(f"Linked AutoDev state paths are not allowed: {current.name}")
            current = current.parent

    def _connect(self, create: bool = False) -> sqlite3.Connection:
        self._check_private_path(self.path)
        if create:
            self.directory.mkdir(exist_ok=True)
        elif not self.path.is_file():
            raise ContractError("Project is not initialized; run init first")
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        return connection

    def execute(self, action: str, data: dict | None = None) -> dict | str:
        data = {} if data is None else data
        if not isinstance(data, dict):
            raise ContractError("Request must be a JSON object")
        if action in READ_ACTIONS:
            return self.read(action, data)
        if action not in COMMANDS:
            raise ContractError(f"Unknown action: {action}")
        roles, required, optional = COMMANDS[action]
        unknown = set(data) - set((required + " " + optional).split()) - {"actor", "expected_revision"}
        missing = set(required.split()) - set(data)
        if unknown or missing:
            raise ContractError(f"Invalid fields; missing={sorted(missing)}, unknown={sorted(unknown)}")
        actor = actor_from(data)
        if actor["role"] not in roles.split():
            raise ContractError(f"{action} is not authorized for role {actor['role']}")
        with closing(self._connect(create=action == "init")) as db, db:
            db.execute("BEGIN IMMEDIATE")
            if action == "init":
                db.execute("CREATE TABLE IF NOT EXISTS current_state (id INTEGER PRIMARY KEY CHECK(id=1), revision INTEGER NOT NULL, body TEXT NOT NULL)")
                db.execute("CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, time TEXT NOT NULL, run INTEGER NOT NULL, action TEXT NOT NULL, actor TEXT NOT NULL, body TEXT NOT NULL)")
                db.execute("CREATE TRIGGER IF NOT EXISTS events_no_update BEFORE UPDATE ON events BEGIN SELECT RAISE(ABORT, 'journal is append-only'); END")
                db.execute("CREATE TRIGGER IF NOT EXISTS events_no_delete BEFORE DELETE ON events BEGIN SELECT RAISE(ABORT, 'journal is append-only'); END")
            row = db.execute("SELECT revision, body FROM current_state WHERE id=1").fetchone()
            if action == "init":
                if row:
                    raise ContractError("Already initialized; use status or new-run")
                limits = data["limits"]
                if not isinstance(limits, dict) or set(limits) != {"max_sprints", "max_tasks", "max_attempts"}:
                    raise ContractError("limits must specify max_sprints, max_tasks, and max_attempts")
                for key in limits:
                    number(limits, key, 1)
                models = strings(data, "models", nonempty=True) if "models" in data else DEFAULT_MODELS.copy()
                if any(not model_allowed(m) for m in models):
                    raise ContractError("Model policy must use explicit non-Anthropic models")
                state = new_state(text(data, "intent"), {"limits": limits, "models": models})
                revision = 0
                result = {"initialized": True, "policy": state["policy"]}
            else:
                if not row:
                    raise ContractError("State is missing; initialize the project")
                revision, state = row["revision"], json.loads(row["body"])
                if state.get("schema") != 1:
                    raise ContractError("Unsupported state schema; do not overwrite it")
                if "expected_revision" in data and number(data, "expected_revision") != revision:
                    raise ContractError("Stale state revision; reload context before deciding")
                if state["closed"] and action != "new-run":
                    raise ContractError("Run is closed; start a new run before changing it")
                if state["outcome"] and action not in {"audit", "disposition", "close", "feedback", "new-run", "reopen"}:
                    raise ContractError("Run has finished; complete its audit/handover or start a new run")
                known = state["contexts"].get(actor["id"])
                if known and known != actor:
                    raise ContractError("A context cannot change its recorded role/model; use a genuinely separate context")
                result = Engine(self, state, actor, sequence=revision + 1).apply(action, data)
            if actor["role"] != "client" and actor["model"] not in state["policy"]["models"]:
                raise ContractError("Actor model is not in this project's permitted model list")
            state["contexts"][actor["id"]] = actor
            revision += 1
            db.execute("INSERT OR REPLACE INTO current_state VALUES (1, ?, ?)", (revision, encoded(state)))
            event_data = dict(data)
            if "content" in event_data:
                event_data["content_hash"] = digest(event_data.pop("content"))
            db.execute(
                "INSERT INTO events(time,run,action,actor,body) VALUES (?,?,?,?,?)",
                (datetime.now(timezone.utc).isoformat(), state["run"], action, encoded(actor),
                 encoded({"request": event_data, "result": result})),
            )
            return {"revision": revision, "result": result}

    def load(self) -> tuple[int, dict]:
        with closing(self._connect()) as db:
            row = db.execute("SELECT revision,body FROM current_state WHERE id=1").fetchone()
            if not row:
                raise ContractError("State is not initialized")
            return row["revision"], json.loads(row["body"])

    def read(self, action: str, data: dict) -> dict | str:
        revision, state = self.load()
        if action == "journal":
            after = number(data, "after") if "after" in data else 0
            with closing(self._connect()) as db:
                rows = db.execute("SELECT * FROM events WHERE seq > ? ORDER BY seq LIMIT 200", (after,)).fetchall()
                return {"events": [dict(r) | {"actor": json.loads(r["actor"]), "body": json.loads(r["body"])} for r in rows]}
        engine = Engine(self, state, {"id": "observer", "role": "client"})
        if action == "materialize":
            item = engine.improvement(text(data, "improvement"))
            suffix = ".py" if item["kind"] == "tool" else ".md"
            path = self.directory / "generated" / f"{item['id']}-{item['digest']}{suffix}"
            self._check_private_path(path)
            path.parent.mkdir(exist_ok=True)
            content = item["content"].encode("utf-8")
            try:
                with path.open("xb") as output:
                    output.write(content)
            except FileExistsError:
                if path.read_bytes() != content:
                    raise ContractError("Materialized content was modified; preserve it and resolve the discrepancy")
            return {"path": str(path), "digest": item["digest"], "status": item["status"], "scope": item["scope"]}
        if action == "context":
            return {"revision": revision, "state": state, "scope_digests": engine.scope_digests()}
        summary = {
            "revision": revision, "run": state["run"], "intent": state["intent"],
            "paused": state["paused"], "baseline": state["baseline"],
            "outcome": state["outcome"], "accepted": state["acceptance"] is not None,
            "closed": state["closed"], "policy": state["policy"],
            "sprints": [{
                "id": s["id"], "goal": s["goal"], "outcome": s["outcome"],
                "tasks": [{"id": t["id"], "title": t["title"], "status": t["status"],
                           "revision": t["revision"], "owner": t["owner"],
                           "digest": t["submission"]["digest"] if t["submission"] else None}
                          for t in s["tasks"]],
                **engine.submission_status(s),
                "audit": engine.audit_status(s["id"]),
            } for s in state["sprints"]],
            "run_audit": engine.audit_status("run"),
            "improvements": [{k: v for k, v in i.items() if k not in {"content"}} for i in state["improvements"].values()],
            "active_improvements": state["active_improvements"],
            "scope_digests": engine.scope_digests(),
        }
        if action == "status":
            return summary
        lines = [
            "# AutoDev inspection", "", f"Intent: {state['intent']}",
            f"Run: {state['run']} | revision: {revision} | outcome: {state['outcome'] or 'in progress'}",
            f"Client accepted: {summary['accepted']} | closed: {state['closed']}", "",
        ]
        if state["paused"]:
            lines += [f"Paused: {state['paused']}", ""]
        for sprint in summary["sprints"]:
            lines += [f"## {sprint['id']}: {sprint['goal']}", f"Outcome: {sprint['outcome'] or 'in progress'}; audit: {sprint['audit']}", ""]
            if sprint["submission_blocker"]:
                lines += [f"Integration readiness: {sprint['submission_blocker']}", ""]
            lines += [f"- {t['id']}: {t['status']} (assignment {t['revision']}) - {t['title']}" for t in sprint["tasks"]]
            lines += [""]
        lines += ["## Process feedback", ""]
        lines += [f"- {f['actor']['role']} / {f['sprint']}: {f['summary']}" for f in state["feedback"]]
        lines += ["", "## Improvements", ""]
        lines += [f"- {i['id']}: {i['scope']} / {i['status']} - {i['benefit']}" for i in state["improvements"].values()]
        lines += ["", f"Run audit: {summary['run_audit']}", "",
                  "Evidence is recorded, not inferred. Actor identities and approvals depend on the trusted host.", ""]
        return "\n".join(lines)

    def relative(self, value: str, *, scope: bool = False) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ContractError("File paths must be nonempty strings")
        value = value.replace("\\", "/")
        raw = PurePosixPath(value)
        if raw.is_absolute() or PureWindowsPath(value).drive or ":" in value or ".." in raw.parts:
            raise ContractError("Only project-relative paths without traversal are allowed")
        if raw.parts and raw.parts[0].casefold() in {".autodev", ".git"}:
            raise ContractError("Delivery tasks cannot modify AutoDev state or Git internals")
        if not raw.parts and not scope:
            raise ContractError("Snapshot entries must name files, not the project root")
        path = self.project.joinpath(*raw.parts)
        if path.resolve() != path.absolute() or not path.resolve().is_relative_to(self.project):
            raise ContractError("Linked paths cannot be used as delivery scopes or evidence")
        return os.path.normcase(raw.as_posix()).replace("\\", "/")

    def snapshot(self, files: list[str]) -> dict:
        result = {}
        for name in files:
            relative = self.relative(name)
            path = self.project / relative
            if not path.is_file():
                raise ContractError(f"Evidence file does not exist: {relative}")
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        if not result:
            raise ContractError("At least one evidence file is required")
        if len(result) != len(files):
            raise ContractError("Duplicate snapshot file paths")
        return result


class Engine:
    def __init__(self, store: Store, state: dict, actor: dict, sequence: int | None = None):
        self.store, self.state, self.actor = store, state, actor
        self.sequence = sequence

    def sprint(self, identifier: str) -> dict:
        for item in self.state["sprints"]:
            if item["id"] == identifier:
                return item
        raise ContractError(f"Unknown sprint: {identifier}")

    def task(self, identifier: str) -> tuple[dict, dict]:
        for sprint in self.state["sprints"]:
            for task in sprint["tasks"]:
                if task["id"] == identifier:
                    return sprint, task
        raise ContractError(f"Unknown task: {identifier}")

    def improvement(self, identifier: str) -> dict:
        if identifier not in self.state["improvements"]:
            raise ContractError(f"Unknown improvement: {identifier}")
        return self.state["improvements"][identifier]

    def active(self, sprint: dict) -> None:
        if self.state["paused"]:
            raise ContractError("Run is paused; no new execution is authorized")
        if sprint["outcome"]:
            raise ContractError("Sprint is finished; its work cannot be silently rewritten")
        baseline = self.state["baseline"]
        if not baseline or sprint["baseline"] != baseline["digest"]:
            raise ContractError("Sprint baseline changed; finish/cancel and explicitly replan")
        if baseline["versions"] != {k: len(v) for k, v in self.state["artifacts"].items()}:
            raise ContractError("Current package contains unapproved revisions; resolve before execution")

    def check_revision(self, task: dict, data: dict) -> None:
        if number(data, "revision") != task["revision"]:
            raise ContractError("Stale assignment revision")

    def check_files(self, snapshot: dict) -> None:
        if self.store.snapshot(list(snapshot)) != snapshot:
            raise ContractError("Evidence is stale: files changed since verification/submission")

    def scope(self, identifier: str) -> dict:
        if identifier == "run":
            return {
                "run": self.state["run"], "intent": self.state["intent"],
                "sprints": [{"scope": self.scope(s["id"]), "audits": s["audits"],
                             "exception": s["exception"]} for s in self.state["sprints"]],
                "outcome": self.state["outcome"], "acceptance": self.state["acceptance"],
                "artifacts": self.state["artifacts"], "approvals": self.state["approvals"],
                "package_reviews": self.state["package_reviews"],
                "feedback": [f for f in self.state["feedback"] if f["actor"]["role"] != "auditor"],
                "improvements": self.state["improvements"],
                "active_improvements": self.state["active_improvements"],
            }
        sprint = self.sprint(identifier)
        return {k: sprint[k] for k in ("id", "goal", "baseline", "tasks", "integration", "outcome")} | {
            "feedback": [f for f in self.state["feedback"]
                         if f["sprint"] == identifier and f["actor"]["role"] != "auditor"],
        }

    def scope_digests(self) -> dict:
        return {key: digest(self.scope(key)) for key in ["run"] + [s["id"] for s in self.state["sprints"]]}

    def audits(self, scope: str) -> list:
        return self.state["run_audits"] if scope == "run" else self.sprint(scope)["audits"]

    def latest_audit(self, scope: str) -> dict | None:
        reports = self.audits(scope)
        return reports[-1] if reports else None

    def audit_status(self, scope: str) -> str:
        audit = self.latest_audit(scope)
        if not audit:
            return "pending"
        if audit["digest"] != digest(self.scope(scope)):
            return "stale"
        return "complete" if audit["complete"] else "incomplete"

    def audited(self, scope: str) -> None:
        if self.audit_status(scope) != "complete":
            raise ContractError(f"{scope} audit is not complete for the current scope")
        self.check_findings(scope)

    def check_findings(self, scope: str) -> None:
        for audit in self.audits(scope):
            for finding in audit["findings"]:
                disposition = audit["dispositions"].get(finding["id"])
                label = f"{scope}/{audit['id']}/{finding['id']}"
                if not disposition:
                    raise ContractError(f"Audit finding {label} needs a GM disposition")
                if finding["blocking"] and disposition["decision"] != "resolved":
                    raise ContractError(f"Blocking audit finding {label} must be resolved before continuation")

    @staticmethod
    def recorded_snapshot(sprint: dict) -> dict:
        candidates = {}
        for task in sprint["tasks"]:
            submission = task["submission"]
            if submission:
                for path, fingerprint in submission["files"].items():
                    candidates.setdefault(path, []).append((fingerprint, submission.get("sequence")))
        snapshots = {}
        for path, entries in candidates.items():
            if len({fingerprint for fingerprint, _ in entries}) == 1:
                snapshots[path] = entries[0][0]
                continue
            sequences = [sequence for _, sequence in entries]
            if any(type(sequence) is not int or sequence < 1 for sequence in sequences):
                raise ContractError(f"Overlapping legacy snapshots for {path} lack submission order; reassign and resubmit for fresh verification")
            if len(set(sequences)) != len(sequences):
                raise ContractError(f"Conflicting submission sequence for {path}")
            snapshots[path] = max(entries, key=lambda entry: entry[1])[0]
        return snapshots

    def submission_status(self, sprint: dict) -> dict:
        if not sprint["tasks"] or any(t["status"] != "verified" for t in sprint["tasks"]):
            return {"submission_digest": None, "submission_blocker": "Tasks are not all verified"}
        try:
            return {"submission_digest": digest(self.recorded_snapshot(sprint)), "submission_blocker": None}
        except ContractError as error:
            return {"submission_digest": None, "submission_blocker": str(error)}

    def integrated_snapshot(self, sprint: dict) -> dict:
        for task in sprint["tasks"]:
            if task["status"] != "verified":
                raise ContractError("Every task must be independently reviewed and tested")
        snapshots = self.recorded_snapshot(sprint)
        if not snapshots:
            raise ContractError("Sprint has no verified implementation")
        self.check_files(snapshots)
        return snapshots

    def apply(self, action: str, data: dict) -> dict:
        method = getattr(self, "do_" + action.replace("-", "_"))
        return method(data)

    def do_artifact(self, data: dict) -> dict:
        kind = text(data, "kind")
        if ARTIFACT_ROLES.get(kind) != self.actor["role"]:
            raise ContractError("Specification, architecture, and plan belong to BA, Architect, and PM respectively")
        versions = self.state["artifacts"][kind]
        record = {"version": len(versions) + 1, "content": text(data, "content"), "author": self.actor}
        record["digest"] = digest(record["content"])
        versions.append(record)
        return {"kind": kind, "version": record["version"], "digest": record["digest"]}

    def current_versions(self, data: dict) -> dict:
        versions = data["versions"]
        if not isinstance(versions, dict) or set(versions) != set(ARTIFACT_ROLES):
            raise ContractError("Approval must name spec, architecture, and plan versions")
        for kind in ARTIFACT_ROLES:
            if number(versions, kind, 1) != len(self.state["artifacts"][kind]):
                raise ContractError("Use the current named versions, not missing or superseded drafts")
        return versions

    def do_challenge_package(self, data: dict) -> dict:
        versions = self.current_versions(data)
        authors = {self.state["artifacts"][kind][-1]["author"]["id"] for kind in ARTIFACT_ROLES}
        if self.actor["id"] in authors:
            raise ContractError("Package challenge must be independent of its authors")
        review = {"actor": self.actor, "versions": versions, "passed": boolean(data, "passed"),
                  "evidence": text(data, "evidence")}
        self.state["package_reviews"].append(review)
        return review

    def do_approve(self, data: dict) -> dict:
        versions = self.current_versions(data)
        reviews = {r["actor"]["id"]: r for r in self.state["package_reviews"] if r["versions"] == versions}
        if len({r["actor"]["model"] for r in reviews.values() if r["passed"]}) < 2:
            raise ContractError("Package approval requires independent challenge by two different permitted models")
        if any(not review["passed"] for review in reviews.values()):
            raise ContractError("Resolve outstanding package-review blockers before approval")
        record = {"versions": versions, "evidence": text(data, "evidence"), "actor": self.actor}
        record["digest"] = digest({"versions": versions, "policy": self.state["policy"], "run": self.state["run"]})
        self.state["approvals"].append(record)
        if not self.state["baseline"] or self.state["baseline"]["digest"] != record["digest"]:
            self.state["acceptance"] = None
        self.state["baseline"] = record
        return record

    def do_start_sprint(self, data: dict) -> dict:
        if self.state["paused"]:
            raise ContractError("Run is paused")
        baseline = self.state["baseline"]
        if not baseline or baseline["versions"] != {k: len(v) for k, v in self.state["artifacts"].items()}:
            raise ContractError("Current specification, architecture, and plan require Client approval")
        sprints = self.state["sprints"]
        if len(sprints) >= self.state["policy"]["limits"]["max_sprints"]:
            raise ContractError("Sprint limit reached; stop and obtain a new mandate")
        goal = text(data, "goal")
        if sprints:
            previous = sprints[-1]
            if not previous["outcome"]:
                raise ContractError("Finish the current sprint before starting another")
            self.check_findings(previous["id"])
            if previous["outcome"] == "success":
                self.integrated_snapshot(previous)
            exception = previous["exception"]
            if self.audit_status(previous["id"]) != "complete" and exception and exception["next_goal"] == goal:
                if exception["consumed"]:
                    raise ContractError("Client audit exception has already been used")
                exception["consumed"] = True
            else:
                self.audited(previous["id"])
            if previous["outcome"] != "success":
                text(data, "recovery_plan")
        sprint = {
            "id": f"sprint-{len(sprints) + 1}", "goal": goal, "baseline": baseline["digest"],
            "tasks": [], "integration": None, "outcome": None, "audits": [], "exception": None,
        }
        sprints.append(sprint)
        self.state["acceptance"] = None
        return {"sprint": sprint["id"], "baseline": sprint["baseline"]}

    def do_add_task(self, data: dict) -> dict:
        sprint = self.sprint(text(data, "sprint"))
        self.active(sprint)
        if sprint["baseline"] != self.state["baseline"]["digest"]:
            raise ContractError("The active sprint uses an older baseline; explicitly replan before assigning work")
        count = sum(len(s["tasks"]) for s in self.state["sprints"])
        if count >= self.state["policy"]["limits"]["max_tasks"]:
            raise ContractError("Task limit reached")
        paths = [self.store.relative(p, scope=True) for p in strings(data, "paths", nonempty=True)]
        dependencies = strings(data, "depends_on") if "depends_on" in data else []
        for identifier in dependencies:
            dep_sprint, _ = self.task(identifier)
            if dep_sprint["id"] != sprint["id"]:
                raise ContractError("Task dependencies must refer to this sprint")
        task = {
            "id": f"task-{count + 1}", "title": text(data, "title"), "paths": paths,
            "depends_on": dependencies, "status": "ready", "revision": 0, "attempts": 0,
            "owner": None, "contributors": [], "submission": None, "reviews": {},
        }
        sprint["tasks"].append(task)
        sprint["integration"] = None
        return task

    @staticmethod
    def overlaps(first: str, second: str) -> bool:
        a, b = PurePosixPath(first), PurePosixPath(second)
        return a.is_relative_to(b) or b.is_relative_to(a)

    def do_claim(self, data: dict) -> dict:
        sprint, task = self.task(text(data, "task"))
        self.active(sprint)
        self.check_revision(task, data)
        if task["status"] != "ready":
            raise ContractError("Task already has an owner or is awaiting verification")
        if task["attempts"] >= self.state["policy"]["limits"]["max_attempts"]:
            raise ContractError("Task retry limit reached; escalate rather than repeat")
        if any(self.task(dep)[1]["status"] != "verified" for dep in task["depends_on"]):
            raise ContractError("Task dependencies are not verified")
        for other in sprint["tasks"]:
            if other["status"] in {"in_progress", "submitted"}:
                if any(self.overlaps(a, b) for a in task["paths"] for b in other["paths"]):
                    raise ContractError("Conflicting active write scopes; serialize the work")
        task.update(status="in_progress", owner=self.actor, revision=task["revision"] + 1,
                    attempts=task["attempts"] + 1, submission=None, reviews={})
        if self.actor["id"] not in task["contributors"]:
            task["contributors"].append(self.actor["id"])
        sprint["integration"] = None
        return {"task": task["id"], "revision": task["revision"], "owner": task["owner"]}

    def do_submit(self, data: dict) -> dict:
        sprint, task = self.task(text(data, "task"))
        self.active(sprint)
        self.check_revision(task, data)
        if task["status"] != "in_progress" or task["owner"]["id"] != self.actor["id"]:
            raise ContractError("Only the current assigned owner can submit")
        files = self.store.snapshot(strings(data, "files", nonempty=True))
        for path in files:
            if not any(PurePosixPath(path).is_relative_to(PurePosixPath(scope)) for scope in task["paths"]):
                raise ContractError("Submitted file is outside the assignment's write scope")
        if self.sequence is None:
            raise ContractError("Submissions require the transactional store's event sequence")
        submission = {"files": files, "digest": digest(files), "evidence": text(data, "evidence"),
                      "sequence": self.sequence}
        task.update(status="submitted", submission=submission)
        return {"task": task["id"], "revision": task["revision"], "digest": submission["digest"]}

    def do_review(self, data: dict) -> dict:
        sprint, task = self.task(text(data, "task"))
        self.active(sprint)
        self.check_revision(task, data)
        if task["status"] != "submitted" or self.actor["id"] in task["contributors"]:
            raise ContractError("Review requires a submitted task and a separate agent context")
        if text(data, "digest") != task["submission"]["digest"]:
            raise ContractError("Review is for the wrong submission")
        self.check_files(task["submission"]["files"])
        passed = boolean(data, "passed")
        verdict = {"actor": self.actor, "passed": passed, "evidence": text(data, "evidence"),
                   "digest": data["digest"]}
        task["reviews"][self.actor["role"]] = verdict
        if not passed:
            task["status"] = "ready"
            task["owner"] = None
            sprint["integration"] = None
        elif set(task["reviews"]) == {"reviewer", "tester"} and all(r["passed"] for r in task["reviews"].values()):
            task["status"] = "verified"
        return {"task": task["id"], "status": task["status"], "verdict": verdict}

    def do_reassign(self, data: dict) -> dict:
        sprint, task = self.task(text(data, "task"))
        if sprint["outcome"]:
            raise ContractError("Reopen a finished sprint before changing its assignments")
        self.check_revision(task, data)
        if not boolean(data, "reconciled"):
            raise ContractError("Reconcile previous workers and external effects before reassignment")
        reason = text(data, "reason")
        task.update(status="ready", owner=None, revision=task["revision"] + 1,
                    submission=None, reviews={})
        sprint["integration"] = None
        return {"task": task["id"], "revision": task["revision"], "reason": reason}

    def do_integrate(self, data: dict) -> dict:
        sprint = self.sprint(text(data, "sprint"))
        self.active(sprint)
        if any(self.actor["id"] in t["contributors"] for t in sprint["tasks"]):
            raise ContractError("Integrated verification must be independent of implementers")
        files = self.integrated_snapshot(sprint)
        if text(data, "digest") != digest(files):
            raise ContractError("Integrated evidence must match the combined submission files")
        sprint["integration"] = {"files": files, "digest": digest(files), "actor": self.actor,
                                 "passed": boolean(data, "passed"), "evidence": text(data, "evidence")}
        return sprint["integration"]

    def do_finish_sprint(self, data: dict) -> dict:
        sprint = self.sprint(text(data, "sprint"))
        if sprint["outcome"]:
            raise ContractError("Sprint outcome is already recorded")
        outcome = text(data, "outcome")
        if outcome not in {"success", "failed", "cancelled"}:
            raise ContractError("Sprint outcome must be success, failed, or cancelled")
        if any(t["status"] == "in_progress" for t in sprint["tasks"]):
            raise ContractError("Reconcile/reassign active workers before finishing")
        if outcome == "success":
            self.active(sprint)
            files = self.integrated_snapshot(sprint)
            integration = sprint["integration"]
            if not integration or not integration["passed"] or integration["files"] != files:
                raise ContractError("Passing integrated verification is required")
        sprint["outcome"] = outcome
        return {"sprint": sprint["id"], "outcome": outcome, "reason": text(data, "reason"), "audit": "pending"}

    def do_feedback(self, data: dict) -> dict:
        sprint = self.sprint(text(data, "sprint"))
        if "task" in data:
            task_sprint, _ = self.task(text(data, "task"))
            if task_sprint["id"] != sprint["id"]:
                raise ContractError("Feedback task belongs to a different sprint")
        record = {"sprint": sprint["id"], "actor": self.actor, "task": data.get("task"),
                  "summary": text(data, "summary")}
        self.state["feedback"].append(record)
        return record

    def do_audit(self, data: dict) -> dict:
        scope = text(data, "scope")
        if scope == "run":
            if not self.state["outcome"]:
                raise ContractError("Record the run outcome before its retrospective")
        elif not self.sprint(scope)["outcome"]:
            raise ContractError("Finish the sprint before its retrospective")
        covered = self.state["sprints"] if scope == "run" else [self.sprint(scope)]
        participants = [context for s in covered for t in s["tasks"] for context in t["contributors"]]
        if self.actor["id"] in participants:
            raise ContractError("Auditor must be independent of implementation")
        if text(data, "digest") != digest(self.scope(scope)):
            raise ContractError("Audit scope changed; inspect the current scope before reporting")
        examined = strings(data, "examined")
        if set(examined) - set(AUDIT_REQUIREMENTS):
            raise ContractError("Unknown audit evidence category")
        outstanding = strings(data, "outstanding")
        limitations = strings(data, "limitations")
        findings = data["findings"]
        if not isinstance(findings, list):
            raise ContractError("findings must be an array")
        identifiers = set()
        for finding in findings:
            if not isinstance(finding, dict):
                raise ContractError("Each finding must be an object")
            identifier = text(finding, "id")
            if identifier in identifiers:
                raise ContractError("Finding IDs must be unique")
            identifiers.add(identifier)
            text(finding, "summary")
            text(finding, "evidence")
            boolean(finding, "blocking")
        reports = self.audits(scope)
        report = {
            "id": f"audit-{len(reports) + 1}", "actor": self.actor, "digest": data["digest"],
            "examined": examined, "outstanding": outstanding, "limitations": limitations,
            "complete": set(examined) == set(AUDIT_REQUIREMENTS) and not outstanding,
            "findings": findings, "dispositions": {}, "evidence": text(data, "evidence"),
        }
        reports.append(report)
        return report

    def do_disposition(self, data: dict) -> dict:
        scope = text(data, "scope")
        identifier = text(data, "audit")
        report = next((audit for audit in self.audits(scope) if audit["id"] == identifier), None)
        if report is None:
            raise ContractError("Disposition must identify an existing audit")
        finding = text(data, "finding")
        if finding not in {f["id"] for f in report["findings"]}:
            raise ContractError("Unknown finding")
        decision = text(data, "decision")
        if decision not in {"resolved", "deferred", "rejected", "scheduled"}:
            raise ContractError("Unknown finding disposition")
        report["dispositions"][finding] = {"decision": decision, "reason": text(data, "reason"), "actor": self.actor}
        return report["dispositions"][finding]

    def do_audit_exception(self, data: dict) -> dict:
        sprint = self.sprint(text(data, "sprint"))
        if not sprint["outcome"]:
            raise ContractError("Exception must name a finished sprint")
        sprint["exception"] = {
            "actor": self.actor, "reason": text(data, "reason"),
            "next_goal": text(data, "next_goal"), "recovery_owner": text(data, "recovery_owner"),
            "consumed": False,
        }
        return sprint["exception"]

    def do_accept(self, data: dict) -> dict:
        sprint = self.sprint(text(data, "sprint"))
        if sprint is not self.state["sprints"][-1] or sprint["outcome"] != "success":
            raise ContractError("Acceptance must name the latest successful increment")
        if sprint["baseline"] != self.state["baseline"]["digest"]:
            raise ContractError("Delivery does not match the current approved baseline")
        if self.state["baseline"]["versions"] != {k: len(v) for k, v in self.state["artifacts"].items()}:
            raise ContractError("Current package contains unapproved revisions")
        files = self.integrated_snapshot(sprint)
        if text(data, "digest") != digest(files):
            raise ContractError("Acceptance must name the exact delivered files")
        self.state["acceptance"] = {
            "sprint": sprint["id"], "digest": data["digest"], "actor": self.actor,
            "evidence": text(data, "evidence"), "baseline": sprint["baseline"],
        }
        return self.state["acceptance"]

    def do_finish_run(self, data: dict) -> dict:
        if any(not s["outcome"] for s in self.state["sprints"]):
            raise ContractError("Finish active sprints before recording the run outcome")
        outcome = text(data, "outcome")
        if outcome not in {"success", "failed", "cancelled"}:
            raise ContractError("Unknown run outcome")
        if outcome == "success":
            if not self.state["acceptance"]:
                raise ContractError("Client acceptance is required for successful delivery")
            latest = self.state["sprints"][-1]
            if self.state["acceptance"]["sprint"] != latest["id"]:
                raise ContractError("Client acceptance does not cover the latest sprint")
            if self.state["acceptance"]["baseline"] != self.state["baseline"]["digest"]:
                raise ContractError("Client acceptance does not cover the current approved baseline")
            if self.state["baseline"]["versions"] != {k: len(v) for k, v in self.state["artifacts"].items()}:
                raise ContractError("Current package contains unapproved revisions")
            self.integrated_snapshot(latest)
        self.state["outcome"] = outcome
        return {"outcome": outcome, "reason": text(data, "reason"), "audit": "pending"}

    def do_close(self, data: dict) -> dict:
        if not self.state["outcome"]:
            raise ContractError("Record the run outcome first")
        for sprint in self.state["sprints"]:
            self.audited(sprint["id"])
        self.audited("run")
        if self.state["outcome"] == "success":
            self.integrated_snapshot(self.state["sprints"][-1])
        self.state["closed"] = True
        return {"closed": True, "handover": text(data, "handover")}

    def do_new_run(self, data: dict) -> dict:
        if not self.state["closed"]:
            raise ContractError("Close the previous run, including audits, before starting another")
        old = {k: v for k, v in self.state.items() if k != "past_runs"}
        fresh = new_state(text(data, "intent"), self.state["policy"], self.state["run"] + 1)
        fresh["past_runs"] = self.state["past_runs"] + [old]
        fresh["improvements"] = dict(self.state["improvements"])
        fresh["active_improvements"] = dict(self.state["active_improvements"])
        fresh["contexts"] = dict(self.state["contexts"])
        self.state.clear()
        self.state.update(fresh)
        return {"run": fresh["run"], "intent": fresh["intent"]}

    def do_pause(self, data: dict) -> dict:
        self.state["paused"] = text(data, "reason")
        return {"paused": self.state["paused"], "note": "Stop requested; the host must quiesce active workers"}

    def do_resume(self, data: dict) -> dict:
        if not boolean(data, "reconciled"):
            raise ContractError("Reconcile owners, permissions, and external effects before resuming")
        self.state["paused"] = None
        return {"resumed": True, "reason": text(data, "reason")}

    def do_reopen(self, data: dict) -> dict:
        if not boolean(data, "reconciled"):
            raise ContractError("Reconcile workers and effects before reopening work")
        if not self.state["sprints"] or not self.state["sprints"][-1]["outcome"]:
            raise ContractError("Reopen requires a finished latest sprint")
        sprint = self.state["sprints"][-1]
        if (self.state["outcome"] == "cancelled" or sprint["outcome"] == "cancelled") and self.actor["role"] != "client":
            raise ContractError("Cancelled scope needs explicit renewed Client authorization")
        sprint["outcome"] = None
        sprint["integration"] = None
        self.state["outcome"] = None
        self.state["acceptance"] = None
        return {"sprint": sprint["id"], "reason": text(data, "reason"),
                "note": "Prior outcomes/acceptance remain in the journal; reverify and obtain acceptance again"}

    def do_propose_improvement(self, data: dict) -> dict:
        scope, kind, target = text(data, "scope"), text(data, "kind"), text(data, "target")
        if scope not in {"project", "shared"} or kind not in {"guidance", "tool"}:
            raise ContractError("Improvement scope must be project/shared and kind guidance/tool")
        if kind == "guidance" and target not in ROLES - {"client"}:
            raise ContractError("Guidance target must name an internal role")
        if kind == "tool" and not re.fullmatch(r"[a-z][a-z0-9_-]*\.py", target):
            raise ContractError("Project tool targets must be simple Python filenames")
        key = f"{kind}:{target}"
        item = {
            "id": f"improvement-{len(self.state['improvements']) + 1}",
            "scope": scope, "kind": kind, "target": target, "key": key,
            "content": text(data, "content"), "benefit": text(data, "benefit"),
            "author": self.actor, "baseline": self.state["active_improvements"].get(key),
            "evaluation": None, "approval": None, "status": "proposed",
        }
        item["digest"] = digest(item["content"])
        self.state["improvements"][item["id"]] = item
        return {k: v for k, v in item.items() if k != "content"}

    def do_evaluate_improvement(self, data: dict) -> dict:
        item = self.improvement(text(data, "improvement"))
        if item["status"] not in {"proposed", "evaluated"}:
            raise ContractError("Only an unadopted candidate can be evaluated")
        if item["author"]["id"] == self.actor["id"]:
            raise ContractError("Improvement evaluation must use a separate agent context")
        if text(data, "digest") != item["digest"]:
            raise ContractError("Evaluation must match the exact candidate")
        item["evaluation"] = {
            "actor": self.actor, "digest": data["digest"], "passed": boolean(data, "passed"),
            "evidence": text(data, "evidence"),
        }
        item["status"] = "evaluated"
        return {"improvement": item["id"], "evaluation": item["evaluation"]}

    def has_active_assignments(self) -> bool:
        return any(not sprint["outcome"] and task["status"] in {"in_progress", "submitted"}
                   for sprint in self.state["sprints"] for task in sprint["tasks"])

    def do_adopt_improvement(self, data: dict) -> dict:
        item = self.improvement(text(data, "improvement"))
        if item["scope"] != "project":
            raise ContractError("Shared-plugin improvements require Client approval and a separate source-change handoff")
        if item["status"] != "evaluated" or not item["evaluation"]["passed"]:
            raise ContractError("Passing independent evaluation is required before adoption")
        if self.state["active_improvements"].get(item["key"]) != item["baseline"]:
            raise ContractError("Improvement baseline changed; re-propose and evaluate against current guidance/tooling")
        if self.has_active_assignments():
            raise ContractError("Adopt only at an assignment boundary; do not silently change active contracts")
        self.state["active_improvements"][item["key"]] = item["id"]
        item["status"] = "adopted"
        return {"improvement": item["id"], "active": item["key"], "revert_to": item["baseline"]}

    def do_revert_improvement(self, data: dict) -> dict:
        item = self.improvement(text(data, "improvement"))
        if item["scope"] != "project" or self.state["active_improvements"].get(item["key"]) != item["id"]:
            raise ContractError("Only the current project-local improvement can be reverted")
        if self.has_active_assignments():
            raise ContractError("Reconcile active assignments before reverting their guidance/tooling")
        if item["baseline"] is None:
            self.state["active_improvements"].pop(item["key"])
        else:
            self.state["active_improvements"][item["key"]] = item["baseline"]
        item["status"] = "reverted"
        return {"improvement": item["id"], "active": item["baseline"], "reason": text(data, "reason")}

    def do_approve_shared(self, data: dict) -> dict:
        item = self.improvement(text(data, "improvement"))
        if item["scope"] != "shared" or data["digest"] != item["digest"]:
            raise ContractError("Approval must identify an exact shared-plugin proposal")
        item["approval"] = {"actor": self.actor, "digest": data["digest"], "evidence": text(data, "evidence")}
        return {"improvement": item["id"], "approval": item["approval"]}

    def do_handoff_shared(self, data: dict) -> dict:
        item = self.improvement(text(data, "improvement"))
        if item["scope"] != "shared" or not item["approval"]:
            raise ContractError("Shared-plugin change requires an explicit Client approval")
        if not item["evaluation"] or not item["evaluation"]["passed"]:
            raise ContractError("Shared-plugin candidate requires independent evaluation")
        item["status"] = "approved_for_source_change"
        return {"improvement": item["id"], "digest": item["digest"], "status": item["status"],
                "next": "Separate approved plugin-source change, verification, and installation; installed plugin was not modified"}
