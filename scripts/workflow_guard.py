#!/usr/bin/env python3
"""Portable entry, visual evidence and state gates for the Penpot workflow."""

from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.penpot_validation.validator import (  # noqa: E402
    MAX_CYCLES, VALID_STATES, VALIDATION_STATES, validate_manifest, validate_transition,
)

VISUAL_CAPABILITY = "image-input-or-image-inspection-tool"
CONTRACT = ROOT / "workflow/contract.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def session_path() -> Path:
    value = os.environ.get("PENPOT_WORKFLOW_SESSION")
    return Path(value).expanduser().resolve() if value else ROOT / ".local/workflow-session.json"


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return value


def atomic_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        os.chmod(temp, 0o600 if ".local" in path.parts else 0o644)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def begin() -> dict:
    value = {"session_id": str(uuid.uuid4()), "state": "ENTRYPOINT_PENDING", "began_at": now()}
    atomic_json(session_path(), value)
    return value


def get_session() -> dict | None:
    return read_json(session_path()) if session_path().is_file() else None


def select(mode: str, answer: str) -> dict:
    prior = get_session()
    if prior is None or prior.get("state") != "ENTRYPOINT_PENDING":
        raise ValueError("run begin before recording a new user choice")
    if mode not in read_json(CONTRACT)["entry_modes"] or not answer.strip():
        raise ValueError("unsupported mode or empty user answer")
    value = {"session_id": prior["session_id"], "mode": mode,
             "state": "INFRA_SELECTED" if mode == "infrastructure" else "DESIGN_SELECTED",
             "user_answer": answer.strip(), "selected_at": now()}
    atomic_json(session_path(), value)
    return value


def require(mode: str) -> dict:
    value = get_session()
    if value is None or value.get("state") == "ENTRYPOINT_PENDING":
        raise ValueError("ENTRYPOINT_PENDING: ask the mandatory infrastructure-or-design question first")
    if value.get("mode") != mode:
        raise ValueError(f"entry mode is {value.get('mode')!r}; required {mode!r}")
    return value


def visual_proof(path_value: str, observation: str) -> dict:
    path = Path(path_value).expanduser().resolve()
    if not path.is_file() or path.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
        raise ValueError("visual evidence must be an existing image the worker opened")
    if not observation.strip():
        raise ValueError("record a concrete observation after opening the image")
    try:
        ref = path.relative_to(ROOT).as_posix()
    except ValueError:
        ref = f"external-image:{path.name}"
    return {"reference": ref, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "observation": observation.strip(), "opened_by_worker": True}


def valid_artifact(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size == 0:
        return False
    try:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix == ".jsonl":
            lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            if not lines:
                return False
            for line in lines:
                json.loads(line)
        elif path.suffix == ".png":
            return path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
        elif path.suffix == ".md":
            return "#" in path.read_text(encoding="utf-8")
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    return True


def latest_score(run: Path):
    found = []
    for path in run.glob("cycles/cycle-*/score.json"):
        match = re.fullmatch(r"cycle-(\d+)", path.parent.name)
        if match and valid_artifact(path):
            found.append((int(match.group(1)), path))
    return (max(found, default=(0, None))[1])


def audit(run: Path, expected: set[str] | None = None) -> list[str]:
    errors = []
    manifest_path = run / "manifest.json"
    if not manifest_path.is_file():
        return ["manifest.json is missing"]
    try:
        manifest = read_json(manifest_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [f"manifest.json is invalid: {exc}"]
    state = manifest.get("state")
    if state not in VALID_STATES:
        return [f"invalid state: {state!r}"]
    if expected and state not in expected:
        errors.append(f"state {state} is not one of: {', '.join(sorted(expected))}")
    execution = manifest.get("execution", {})
    proof = execution.get("visual_evidence") if isinstance(execution, dict) else None
    if (execution.get("visual_capability") != VISUAL_CAPABILITY or
        execution.get("visual_capability_verified") is not True or
        not isinstance(proof, dict) or proof.get("opened_by_worker") is not True or
        not re.fullmatch(r"[a-f0-9]{64}", str(proof.get("sha256", ""))) or
        not str(proof.get("observation", "")).strip()):
        errors.append("worker visual capability/evidence is not verified")
    elif not str(proof.get("reference", "")).startswith("external-image:"):
        image = ROOT / proof["reference"]
        if not image.is_file() or hashlib.sha256(image.read_bytes()).hexdigest() != proof["sha256"]:
            errors.append("visual evidence file/hash mismatch")
    for pattern in read_json(CONTRACT).get("state_artifacts", {}).get(state, []):
        if not any(valid_artifact(item) for item in run.glob(pattern)):
            errors.append(f"missing or invalid artifact for {state}: {pattern}")
    if state not in {"INTAKE_PENDING", "INTAKE_REVIEW"}:
        evidence = manifest.get("evidence", {})
        for key in ("initial_questions", "addendum_question", "ambiguity_analysis"):
            if not evidence.get(key):
                errors.append(f"intake evidence is incomplete: {key}")
    if state not in {"INTAKE_PENDING", "INTAKE_REVIEW", "AMBIGUITY_ANALYSIS", "SOURCE_CAPTURED", "BRIEF_REFINEMENT"}:
        try:
            validate_manifest(manifest, strict=True)
        except ValueError as exc:
            errors.append(str(exc))
    if state in {"REFINEMENT", "REFACTORING", "READY_FOR_USER_REVIEW", "USER_REVIEW", "READY_FOR_DELIVERY", "DELIVERED", "NEEDS_REVIEW"}:
        score_path = latest_score(run)
        if score_path is None:
            errors.append("no valid immutable score exists")
        else:
            cycle = score_path.parent
            for name in ("issues.json",):
                if not valid_artifact(cycle / name): errors.append(f"missing or invalid {cycle / name}")
            for pattern in ("*-side-by-side-annotated.png", "*-overlay.png", "*-heatmap.png", "*-detail-board.png"):
                if not any(valid_artifact(p) for p in cycle.glob(pattern)):
                    errors.append(f"missing validation visual: {cycle / pattern}")
            score = read_json(score_path)
            if int(manifest.get("validation_cycle", -1)) != int(score.get("cycle", -2)):
                errors.append("validation_cycle does not match immutable score")
    return errors


def event(run: Path, payload: dict) -> None:
    path = run / "workflow/events.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False) + "\n")


def new_run(args) -> dict:
    require("design")
    run = Path(args.run_dir).resolve()
    if run.exists() and any(run.iterdir()): raise FileExistsError(f"run directory is not empty: {run}")
    run.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": "1.0", "workflow_controller": True, "run_id": run.name,
        "route": args.route, "state": "INTAKE_PENDING", "execution": {
            "runtime": args.runtime, "orchestrator_model": args.orchestrator_model,
            "worker_model": args.worker_model, "worker_class": "cost-efficient", "delegation": "subagent",
            "visual_capability": VISUAL_CAPABILITY, "visual_capability_verified": True,
            "visual_evidence": visual_proof(args.visual_evidence, args.visual_observation)},
        "source_refs": [], "target_viewports": [], "screens": [], "validation_cycle": 0,
        "max_validation_cycles": MAX_CYCLES, "user_review_round": 0, "lesson_refs": [],
        "approvals": {"briefing": False, "user": False, "design_system": False},
        "evidence": {"initial_questions": False, "addendum_question": False, "ambiguity_analysis": False},
        "created_at": now(), "updated_at": now()}
    atomic_json(run / "manifest.json", payload)
    event(run, {"event": "run-created", "state": payload["state"], "at": now()})
    return payload


def transition(run: Path, next_state: str) -> dict:
    require("design")
    path = run / "manifest.json"
    manifest = read_json(path)
    original = copy.deepcopy(manifest)
    current = manifest["state"]
    validate_transition(current, next_state, manifest)
    score_path = latest_score(run) if current in VALIDATION_STATES else None
    if current in VALIDATION_STATES:
        if score_path is None: raise ValueError("validation state needs immutable score")
        score = read_json(score_path)
        if score.get("next_state") != next_state: raise ValueError(f"deterministic score requires {score.get('next_state')}")
        manifest["validation_cycle"] = int(score["cycle"])
    manifest["state"] = next_state
    manifest["updated_at"] = now()
    atomic_json(path, manifest)
    errors = audit(run, {next_state})
    if errors:
        atomic_json(path, original)
        raise ValueError("transition blocked:\n- " + "\n- ".join(errors))
    event(run, {"event": "transition", "from": current, "to": next_state, "at": now()})
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("entry"); sub.add_parser("begin"); sub.add_parser("status")
    select_p = sub.add_parser("select"); select_p.add_argument("mode", choices=("infrastructure", "design")); select_p.add_argument("--user-answer", required=True)
    req = sub.add_parser("require"); req.add_argument("mode", choices=("infrastructure", "design"))
    ready = sub.add_parser("mark-infra-ready"); ready.add_argument("--env-file", default=str(ROOT / ".env"))
    create = sub.add_parser("new-run")
    for flag in ("run-dir", "runtime", "orchestrator-model", "worker-model", "visual-evidence", "visual-observation"):
        create.add_argument("--" + flag, required=True)
    create.add_argument("--route", required=True, choices=("reproduction", "directed_creation")); create.add_argument("--visual-capability-verified", action="store_true", required=True)
    check = sub.add_parser("audit-run"); check.add_argument("--run-dir", required=True); check.add_argument("--expect-state", action="append")
    move = sub.add_parser("transition"); move.add_argument("--run-dir", required=True); move.add_argument("--to", required=True, choices=sorted(VALID_STATES))
    args = parser.parse_args(argv)
    try:
        if args.cmd == "entry": print(read_json(CONTRACT)["entry_question"])
        elif args.cmd == "begin": begin(); print(read_json(CONTRACT)["entry_question"])
        elif args.cmd == "status": print(json.dumps(get_session() or {"state": "ENTRYPOINT_PENDING"}, indent=2))
        elif args.cmd == "select": print(json.dumps(select(args.mode, args.user_answer), indent=2, ensure_ascii=False))
        elif args.cmd == "require": require(args.mode); print(f"entry mode verified: {args.mode}")
        elif args.cmd == "mark-infra-ready":
            value = require("infrastructure"); env = Path(args.env_file)
            content = env.read_text(encoding="utf-8")
            for key in ("PENPOT_ADMIN_EMAIL", "PENPOT_ADMIN_PASSWORD", "PENPOT_MCP_URL", "PENPOT_MCP_TOKEN"):
                if not re.search(rf"(?m)^{key}=.+$", content): raise ValueError(f"{key} missing from local env")
            value["state"] = "INFRA_READY"; atomic_json(session_path(), value); print("infrastructure ready")
        elif args.cmd == "new-run": print(json.dumps(new_run(args), indent=2, ensure_ascii=False))
        elif args.cmd == "audit-run":
            errors = audit(Path(args.run_dir).resolve(), set(args.expect_state or []) or None)
            if errors: raise ValueError("run audit failed:\n- " + "\n- ".join(errors))
            print("run audit passed")
        elif args.cmd == "transition": print(f"transitioned to {transition(Path(args.run_dir).resolve(), args.to)['state']}")
    except (OSError, ValueError, FileExistsError, json.JSONDecodeError) as exc:
        print(f"workflow guard: {exc}", file=sys.stderr); return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
