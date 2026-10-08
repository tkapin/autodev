"""Command-line adapter for AutoDev's local workflow store."""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from autodev_core import COMMANDS, READ_ACTIONS, ContractError, Store


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["help", *sorted(COMMANDS), *sorted(READ_ACTIONS)])
    parser.add_argument("--project", type=Path, default=Path.cwd())
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--input", type=Path, help="UTF-8 JSON request file")
    source.add_argument("--data", help="Inline JSON request (prefer --input for shell portability)")
    args = parser.parse_args()
    try:
        if args.action == "help":
            result = {
                "mutations": {name: {"roles": roles.split(), "required": required.split(),
                                     "optional": optional.split()}
                              for name, (roles, required, optional) in COMMANDS.items()},
                "reads": sorted(READ_ACTIONS),
                "focus": {
                    "selector": "Exactly one of task or sprint (existing ID)",
                    "optional": ["after", "feedback_after", "limit", "expected_revision"],
                    "pagination": "limit 1..200 (default 20); event sequence after and sprint feedback "
                                  "offset feedback_after default 0. Nonzero cursors require "
                                  "expected_revision from the first page; restart on revision change.",
                    "coverage": "Selected tasks and transitive dependencies; all sprint feedback; "
                                "current-run events, including failures and authority changes. "
                                "Explicitly partial; full context and journal remain available.",
                },
                "actor": {"id": "actual host context/agent identifier", "role": "gm", "model": "gpt-6-astra"},
                "note": "All mutations require actor; optional expected_revision prevents stale decisions. Client identity/approval evidence must come from the trusted host.",
            }
        else:
            raw = args.input.read_text(encoding="utf-8-sig") if args.input else args.data or "{}"
            result = Store(args.project).execute(args.action, json.loads(raw))
        if isinstance(result, str):
            print(result)
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ContractError, OSError, sqlite3.Error, json.JSONDecodeError) as error:
        print(json.dumps({"error": str(error), "action": args.action}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
