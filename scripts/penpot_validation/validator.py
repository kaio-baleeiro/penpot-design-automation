"""Explainable, immutable scoring for source screenshots and Penpot exports."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from .images import connected_components, detail_board, diff_values, overlay, read_png, sha256, side_by_side, write_png
from .frame import CAPTURE_MODES, HORIZONTAL_POLICIES, VERTICAL_POLICIES
from .metrics import METRIC_TABLE, METRIC_TABLE_VERSION, compare_metrics
from .structure import load_inventory, validate_structure_inventory


MIN_SCORE = 90.0
MIN_COVERAGE = 0.80
MAX_CYCLES = 3
SCHEMA_VERSION = "1.0"
WORKER_MODEL = "gpt-5.6-luna"
VALID_STATES = {
    "INTAKE_PENDING", "INTAKE_REVIEW", "AMBIGUITY_ANALYSIS", "SOURCE_CAPTURED",
    "BRIEF_REFINEMENT", "BUILD_PLANNED", "BUILDING", "VALIDATING", "REFACTORING",
    "USER_REVIEW", "DS_FORMALIZATION", "DS_REVALIDATING", "DELIVERED", "NEEDS_REVIEW",
    "BLOCKED_MODEL_UNAVAILABLE", "READY_FOR_USER_REVIEW", "READY_FOR_DELIVERY", "REFINEMENT",
}
VALIDATION_STATES = {"VALIDATING", "DS_REVALIDATING"}
FRAME_SPEC_KEYS = {
    "screen_id", "viewport", "document", "frame", "vertical_policy",
    "horizontal_policy", "capture_mode", "stable", "build_ready",
    "requires_user_decision", "evidence",
}

STATE_TRANSITIONS = {
    "INTAKE_PENDING": {"INTAKE_REVIEW"},
    "INTAKE_REVIEW": {"AMBIGUITY_ANALYSIS"},
    "AMBIGUITY_ANALYSIS": {"SOURCE_CAPTURED", "BRIEF_REFINEMENT"},
    "SOURCE_CAPTURED": {"BUILD_PLANNED"},
    "BRIEF_REFINEMENT": {"BUILD_PLANNED"},
    "BUILD_PLANNED": {"BUILDING"},
    "BUILDING": {"VALIDATING", "USER_REVIEW"},
    "VALIDATING": {"REFACTORING", "REFINEMENT", "USER_REVIEW", "READY_FOR_USER_REVIEW", "DS_FORMALIZATION", "READY_FOR_DELIVERY", "NEEDS_REVIEW"},
    "REFACTORING": {"VALIDATING"},
    "REFINEMENT": {"VALIDATING", "BUILDING"},
    "USER_REVIEW": {"BUILDING", "DS_FORMALIZATION", "READY_FOR_USER_REVIEW"},
    "READY_FOR_USER_REVIEW": {"USER_REVIEW", "BUILDING", "DS_FORMALIZATION", "READY_FOR_DELIVERY"},
    "DS_FORMALIZATION": {"DS_REVALIDATING"},
    "DS_REVALIDATING": {"REFINEMENT", "READY_FOR_USER_REVIEW", "READY_FOR_DELIVERY", "NEEDS_REVIEW", "DELIVERED"},
    "READY_FOR_DELIVERY": {"DELIVERED", "NEEDS_REVIEW", "DS_REVALIDATING"},
    "DELIVERED": set(),
    "NEEDS_REVIEW": set(),
    "BLOCKED_MODEL_UNAVAILABLE": set(),
}


def _write_exclusive_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)


def _severity(area_ratio: float, mean_delta: float, dimensions_match: bool) -> str:
    if not dimensions_match or area_ratio >= 0.40 or mean_delta >= 160:
        return "P0"
    if area_ratio >= 0.20 or (area_ratio >= 0.08 and mean_delta >= 64):
        return "P1"
    if area_ratio >= 0.02 or mean_delta >= 80:
        return "P2"
    return "P3"


def _issue(screen_id: str, viewport: dict[str, Any], index: int, severity: str, title: str, detail: str, bounds: dict[str, int] | None = None,
           *, expected: str = "match approved source evidence", actual: str = "visual divergence in Penpot export",
           probable_cause: str = "geometry, style, typography or asset mismatch", suggested_fix: str = "inspect the marked source/export region and refactor only the mismatched elements",
           evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"id": f"{screen_id}-{viewport['width']}x{viewport['height']}-I{index}", "screen": screen_id,
            "viewport": viewport, "severity": severity, "title": title, "detail": detail,
            "region": f"y={bounds['y']}..{bounds['y'] + bounds['height']}" if bounds else "global",
            "bounds": bounds, "expected": expected, "actual": actual, "probable_cause": probable_cause,
            "suggested_fix": suggested_fix, "evidence": evidence or {}, "status": "open", "source": "deterministic-validator"}


def validate_screen(screen: dict[str, Any], output_dir: Path, baseline_screen: dict[str, Any] | None = None) -> dict[str, Any]:
    screen_id = str(screen["id"])
    viewport = {"width": int(screen["viewport"]["width"]), "height": int(screen["viewport"]["height"])}
    source_path = Path(screen["source"])
    export_path = Path(screen["penpot_export"])
    source = read_png(str(source_path))
    exported = read_png(str(export_path))
    frame_spec = screen.get("frame_spec") if isinstance(screen.get("frame_spec"), dict) else {}
    expected_frame = frame_spec.get("frame") if isinstance(frame_spec.get("frame"), dict) else viewport
    expected_width, expected_height = int(expected_frame["width"]), int(expected_frame["height"])
    heatmap, values, pixel_similarity, coverage = diff_values(source, exported)
    exact_similarity = sum(value == 0 for value in values) / len(values)
    visual_metrics = compare_metrics(source, exported)
    score = visual_metrics["weighted_score"]
    source_matches_frame = source.width == expected_width and source.height == expected_height
    export_matches_frame = exported.width == expected_width and exported.height == expected_height
    dimensions_match = source_matches_frame and export_matches_frame
    components = connected_components(values, source.width, source.height)
    min_component_area = max(1, int(source.width * source.height * 0.001))
    components = [component for component in components if component[4] >= min_component_area][:20]
    issues: list[dict[str, Any]] = []
    if not source_matches_frame:
        issues.append(_issue(screen_id, viewport, len(issues) + 1, "P0", "Source capture does not match approved frame",
                             f"Frame esperado {expected_width}x{expected_height}; fonte {source.width}x{source.height}.",
                             {"x": 0, "y": 0, "width": source.width, "height": source.height}))
    if not export_matches_frame:
        issues.append(_issue(screen_id, viewport, len(issues) + 1, "P0", "Penpot frame is truncated or incorrectly expanded",
                             f"Frame esperado {expected_width}x{expected_height}; export Penpot {exported.width}x{exported.height}.",
                             {"x": 0, "y": 0, "width": source.width, "height": source.height}))
    total = source.width * source.height
    for component in components:
        x, y, width, height, area = component
        ratio = area / total
        component_values = [values[yy * source.width + xx] for yy in range(y, min(source.height, y + height)) for xx in range(x, min(source.width, x + width)) if values[yy * source.width + xx] > 32]
        mean_delta = sum(component_values) / max(1, len(component_values))
        max_delta = max(component_values, default=0)
        severity = _severity(ratio, mean_delta, dimensions_match)
        issues.append(_issue(screen_id, viewport, len(issues) + 1, severity, "Visual difference region",
                             f"{area} pixels ({ratio * 100:.2f}% da tela) ultrapassam o limiar; delta médio={mean_delta:.1f}, máximo={max_delta}.",
                             {"x": x, "y": y, "width": width, "height": height},
                             actual=f"region differs on {area} connected pixels",
                             evidence={"area_ratio": round(ratio, 6), "mean_delta": round(mean_delta, 2), "max_delta": max_delta}))
    if baseline_screen and score < float(baseline_screen.get("score", score)) - 2.0:
        issues.append(_issue(screen_id, viewport, len(issues) + 1, "P1", "Regression against previous cycle",
                             f"Score caiu de {baseline_screen['score']:.2f} para {score:.2f}; revisar antes de aprovar."))
    has_blocker = any(issue["severity"] in {"P0", "P1"} for issue in issues)
    passed = score >= MIN_SCORE and coverage >= MIN_COVERAGE and not has_blocker
    output_dir.mkdir(parents=True, exist_ok=True)
    write_png(heatmap, str(output_dir / f"{screen_id}-heatmap.png"))
    write_png(overlay(source, exported), str(output_dir / f"{screen_id}-overlay.png"))
    write_png(side_by_side(source, exported, [tuple(issue["bounds"][key] for key in ("x", "y", "width", "height")) for issue in issues if issue.get("bounds")]), str(output_dir / f"{screen_id}-side-by-side-annotated.png"))
    write_png(detail_board(source, exported, heatmap), str(output_dir / f"{screen_id}-detail-board.png"))
    return {
        "screen": screen_id, "viewport": viewport,
        "frame": {"width": expected_width, "height": expected_height},
        "frame_policy": {
            "vertical": frame_spec.get("vertical_policy", "viewport_bounded"),
            "horizontal": frame_spec.get("horizontal_policy", "viewport_bounded"),
            "capture_mode": frame_spec.get("capture_mode", "viewport"),
        },
        "source": str(source_path), "penpot_export": str(export_path),
        "source_dimensions": {"width": source.width, "height": source.height},
        "export_dimensions": {"width": exported.width, "height": exported.height},
        "metric_table_version": METRIC_TABLE_VERSION, "metrics": visual_metrics["metrics"], "weighted_score": score,
        "regional": visual_metrics.get("regional", {}), "export_sha256": sha256(exported),
        "pixel_similarity": round(pixel_similarity, 6), "exact_similarity": round(exact_similarity, 6),
        "score": score, "coverage": round(coverage, 6), "thresholds": {"score": MIN_SCORE, "coverage": MIN_COVERAGE},
        "passed": passed, "issue_count": len(issues), "artifacts": {
            "heatmap": f"{screen_id}-heatmap.png", "overlay": f"{screen_id}-overlay.png",
            "side_by_side": f"{screen_id}-side-by-side-annotated.png", "detail_board": f"{screen_id}-detail-board.png"}, "issues": issues,
    }


def render_report(result: dict[str, Any], output_path: Path) -> None:
    today = datetime.now(timezone.utc).date().isoformat()
    lines = ["---", "type: validation-report", f"status: {'complete' if result['passed'] else 'needs-review'}",
             f"created: {today}", f"updated: {today}", "source_agent: codex", "agent_context: penpot-design-automation",
             "confidence: high", f"review: {'false' if result['passed'] else 'true'}", "---", "",
             f"# Penpot validation report — cycle {result['cycle']}", "", f"Gate result: **{'PASS' if result['passed'] else 'FAIL'}**", "",
             f"Aggregate score: **{result['aggregate_score']:.2f}/100**", f"Minimum screen score: **{result['minimum_score']:.2f}/100**",
             f"Coverage: **{result['aggregate_coverage'] * 100:.2f}%** (required ≥80%)", "",
             f"Metric table: **{METRIC_TABLE_VERSION}**. The detail board presents source, Penpot export and heatmap in readable vertical slices; the full annotated comparison remains available.", "",
             "The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.", ""]
    if result.get("structure_gate") is not None:
        gate = result["structure_gate"]
        lines += [f"Structural gate: **{'PASS' if gate.get('passed') else 'FAIL'}**", ""]
        if gate.get("errors"):
            lines += ["Structural blockers:"] + [f"- {error}" for error in gate["errors"]] + [""]
    lines += [f"Next state: **{result.get('next_state', 'UNSPECIFIED')}**", ""]
    for screen in result["screens"]:
        lines += [f"## {screen['screen']} — {screen['viewport']['width']}×{screen['viewport']['height']}", "",
                  f"- Score: **{screen['score']:.2f}**; coverage: **{screen['coverage'] * 100:.2f}%**; status: **{'PASS' if screen['passed'] else 'FAIL'}**",
                  f"- Viewport: **{screen['viewport']['width']}×{screen['viewport']['height']}**; frame: **{screen['frame']['width']}×{screen['frame']['height']}**; capture: **{screen['frame_policy']['capture_mode']}**",
                  f"- Similarity evidence: pixel={screen['pixel_similarity']:.4f}, exact={screen['exact_similarity']:.4f}",
                  f"- Readable detail board: `{screen['artifacts']['detail_board']}`; full comparison: `{screen['artifacts']['side_by_side']}`; overlay: `{screen['artifacts']['overlay']}`; heatmap: `{screen['artifacts']['heatmap']}`", ""]
        lines += ["Metric breakdown:", "", "| Dimension | Weight | Score | Contribution | Explanation |", "|---|---:|---:|---:|---|"]
        for metric in screen["metrics"].values():
            lines.append(f"| {metric['label']} | {metric['weight']} | {metric['score']:.2f} | {metric['weighted_contribution']:.2f} | {metric['explanation']} |")
        lines.append("")
        if screen["issues"]:
            lines.append("Issues:")
            for issue in screen["issues"]:
                bounds = issue.get("bounds")
                location = f" at `{bounds}`" if bounds else ""
                lines.append(f"- **{issue['severity']}** `{issue['id']}` — {issue['title']}{location}: {issue['detail']}")
        else:
            lines.append("- No differences above the configured threshold.")
        lines.append("")
    if result.get("regressions"):
        lines += ["## Regression gate", "", "The cycle is not approved because at least one screen regressed against the prior cycle.", ""]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def _is_legacy_manifest(manifest: dict[str, Any]) -> bool:
    return "schema_version" not in manifest and "route" not in manifest and "worker_model" not in manifest


def _evidence_present(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)):
        return bool(value)
    return value is not None


def _viewport(value: Any) -> tuple[int, int] | None:
    if isinstance(value, str) and "x" in value.lower():
        try:
            width, height = (int(item) for item in value.lower().split("x", 1))
            return (width, height) if width > 0 and height > 0 else None
        except ValueError:
            return None
    if not isinstance(value, dict):
        return None
    try:
        width, height = int(value.get("width", 0)), int(value.get("height", 0))
    except (TypeError, ValueError):
        return None
    return (width, height) if width > 0 and height > 0 else None


def _validate_frame_spec(screen: dict[str, Any], viewport: tuple[int, int]) -> None:
    spec = screen.get("frame_spec")
    if not isinstance(spec, dict):
        raise ValueError(f"screen {screen['id']} requires frame_spec")
    if spec.get("screen_id") != screen["id"]:
        raise ValueError(f"screen {screen['id']} frame_spec screen_id must match")
    if _viewport(spec.get("viewport")) != viewport:
        raise ValueError(f"screen {screen['id']} frame_spec viewport must match")
    frame = _viewport(spec.get("frame"))
    if not frame:
        raise ValueError(f"screen {screen['id']} frame_spec has invalid frame bounds")
    frame_width, frame_height = frame
    viewport_width, viewport_height = viewport
    document = _viewport(spec.get("document"))
    if not document:
        raise ValueError(f"screen {screen['id']} frame_spec has invalid document bounds")
    document_width, document_height = document
    if not isinstance(spec.get("stable"), bool):
        raise ValueError(f"screen {screen['id']} frame_spec stable must be boolean")
    vertical = spec.get("vertical_policy")
    horizontal = spec.get("horizontal_policy")
    capture_mode = spec.get("capture_mode")
    if vertical not in VERTICAL_POLICIES:
        raise ValueError(f"screen {screen['id']} frame_spec has invalid vertical_policy")
    if horizontal not in HORIZONTAL_POLICIES:
        raise ValueError(f"screen {screen['id']} frame_spec has invalid horizontal_policy")
    if capture_mode not in CAPTURE_MODES:
        raise ValueError(f"screen {screen['id']} frame_spec has invalid capture_mode")
    if not isinstance(spec.get("evidence"), list) or not spec["evidence"]:
        raise ValueError(f"screen {screen['id']} frame_spec requires evidence")
    if spec.get("build_ready") is not True or spec.get("requires_user_decision") is not False:
        raise ValueError(f"screen {screen['id']} frame_spec must resolve material sizing decisions before build")
    if frame_width < viewport_width or frame_height < viewport_height:
        raise ValueError(f"screen {screen['id']} frame cannot be smaller than its viewport")
    if vertical == "viewport_bounded" and (frame_height != viewport_height or document_height > viewport_height + 2):
        raise ValueError(f"screen {screen['id']} viewport_bounded height must equal viewport height")
    if vertical == "finite_document" and (
        not spec["stable"]
        or document_height <= viewport_height + 2
        or frame_height != document_height
        or capture_mode not in {"full_page", "frame_bounds"}
    ):
        raise ValueError(f"screen {screen['id']} finite_document requires a taller full_page frame")
    if vertical == "dynamic_bounded" and (spec["stable"] or capture_mode not in {"bounded_state", "frame_bounds"}):
        raise ValueError(f"screen {screen['id']} dynamic_bounded requires bounded_state capture")
    if horizontal == "intentional_page" and (
        document_width <= viewport_width + 2
        or frame_width != document_width
        or capture_mode != "frame_bounds"
    ):
        raise ValueError(f"screen {screen['id']} intentional_page requires a wider frame")
    if horizontal != "intentional_page" and frame_width != viewport_width:
        raise ValueError(f"screen {screen['id']} horizontal policy must keep viewport width")
    if horizontal in {"viewport_bounded", "container_overflow"} and document_width > viewport_width + 2:
        raise ValueError(f"screen {screen['id']} horizontal policy contradicts document width")
    if horizontal == "accidental_overflow" and document_width <= viewport_width + 2:
        raise ValueError(f"screen {screen['id']} accidental_overflow requires measured page overflow")


def _validate_canonical_frame_specs(root: Path, manifest: dict[str, Any]) -> None:
    path = root / "source" / "frame-spec.json"
    if not path.is_file():
        raise ValueError("strict validation requires source/frame-spec.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0" or not isinstance(payload.get("screens"), list):
        raise ValueError("source/frame-spec.json has an invalid schema")
    canonical: dict[str, dict[str, Any]] = {}
    for item in payload["screens"]:
        if not isinstance(item, dict) or not isinstance(item.get("screen_id"), str):
            raise ValueError("source/frame-spec.json contains an invalid screen entry")
        if item["screen_id"] in canonical:
            raise ValueError(f"source/frame-spec.json duplicates screen {item['screen_id']}")
        canonical[item["screen_id"]] = item
    for screen in manifest["screens"]:
        expected = canonical.get(screen["id"])
        if expected is None:
            raise ValueError(f"source/frame-spec.json is missing screen {screen['id']}")
        embedded = screen["frame_spec"]
        for key in FRAME_SPEC_KEYS:
            if embedded.get(key) != expected.get(key):
                raise ValueError(f"screen {screen['id']} frame_spec differs from source/frame-spec.json at {key}")


def _approval_values(manifest: dict[str, Any]) -> dict[str, bool]:
    approvals = manifest.get("approvals", manifest.get("approval", manifest.get("approval_flags", {})))
    if not isinstance(approvals, dict):
        return {}
    aliases = {
        "briefing": ("briefing", "briefing_approved"),
        "version": ("version", "version_approved", "prototype", "prototype_approved", "design", "design_approved"),
        "user": ("user", "user_approved", "formal_user_approval"),
        "design_system": ("design_system", "design_system_approved", "ds_formalized"),
    }
    result: dict[str, bool] = {}
    for name, keys in aliases.items():
        for key in keys:
            if key in approvals:
                result[name] = approvals[key]
                break
    return result


def _required_manifest_fields(manifest: dict[str, Any]) -> list[str]:
    required = ["schema_version", "route", "state", "worker_model", "source_refs", "target_viewports",
                "screens", "validation_cycle", "max_validation_cycles", "user_review_round", "lesson_refs"]
    missing = [key for key in required if key not in manifest]
    if "approvals" not in manifest and "approval" not in manifest and "approval_flags" not in manifest:
        missing.append("approvals")
    if "evidence" not in manifest and "question_evidence" not in manifest and "intake" not in manifest:
        missing.append("evidence")
    return missing


def validate_manifest(manifest: dict[str, Any], strict: bool = True) -> None:
    """Validate schema 1.0 and its workflow invariants.

    ``strict=False`` exists solely for the pre-schema unit-test fixture API;
    normal CLI commands always call this function with strict validation.
    """
    if not isinstance(manifest, dict):
        raise ValueError("manifest must be a JSON object")
    if strict:
        missing = _required_manifest_fields(manifest)
        if missing:
            raise ValueError("manifest missing required field(s): " + ", ".join(missing))
        if manifest.get("schema_version") != SCHEMA_VERSION:
            raise ValueError(f"manifest schema_version must be {SCHEMA_VERSION}")
        if manifest.get("route") not in {"reproduction", "directed_creation"}:
            raise ValueError("manifest route must be reproduction or directed_creation")
        if manifest.get("state") not in VALID_STATES:
            raise ValueError(f"manifest state is invalid: {manifest.get('state')}")
        if manifest.get("worker_model") != WORKER_MODEL:
            raise ValueError(f"manifest worker_model must be exactly {WORKER_MODEL}")
        if not isinstance(manifest.get("lesson_refs"), list) or any(
            not isinstance(value, str) or not value.strip() for value in manifest["lesson_refs"]
        ):
            raise ValueError("manifest lesson_refs must be a list of non-empty strings")
        if not isinstance(manifest.get("source_refs"), list):
            raise ValueError("manifest source_refs must be a list")
        if manifest["route"] == "reproduction" and not manifest["source_refs"]:
            raise ValueError("reproduction manifests require at least one source_ref")
        if manifest["route"] == "directed_creation" and manifest["source_refs"]:
            raise ValueError("directed_creation manifests cannot invent source_refs")
        if not isinstance(manifest.get("target_viewports"), list) or not manifest["target_viewports"]:
            raise ValueError("manifest target_viewports must be a non-empty list")
        target_viewports = []
        for target in manifest["target_viewports"]:
            parsed = _viewport(target)
            if not parsed:
                raise ValueError("manifest target_viewports contain an invalid viewport")
            target_viewports.append(parsed)
        if manifest.get("max_validation_cycles") != MAX_CYCLES:
            raise ValueError("manifest max_validation_cycles must be 3")
        if not isinstance(manifest.get("user_review_round"), int) or manifest["user_review_round"] < 0:
            raise ValueError("manifest user_review_round must be a non-negative integer")
        approval_payload = manifest.get("approvals", manifest.get("approval", manifest.get("approval_flags")))
        if not isinstance(approval_payload, dict) or not approval_payload:
            raise ValueError("manifest approvals must contain boolean approval flags")
        if any(not isinstance(value, bool) for value in approval_payload.values()):
            raise ValueError("manifest approvals values must be boolean")
        evidence = manifest.get("evidence", manifest.get("question_evidence", manifest.get("intake")))
        if not isinstance(evidence, dict):
            raise ValueError("manifest evidence must be an object")
        initial = evidence.get("initial_questions", evidence.get("initial_questionnaire", evidence.get("initial_questions_completed")))
        addendum = evidence.get("addendum_question", evidence.get("addendum", evidence.get("addendum_question_completed")))
        ambiguity = evidence.get("ambiguity_analysis", evidence.get("ambiguity_analysis_completed"))
        if not _evidence_present(initial):
            raise ValueError("manifest evidence must include initial_questions")
        if not _evidence_present(addendum):
            raise ValueError("manifest evidence must include addendum_question")
        if not _evidence_present(ambiguity):
            raise ValueError("manifest evidence must include ambiguity_analysis")
        if not isinstance(manifest.get("validation_cycle"), int) or not 0 <= manifest["validation_cycle"] <= MAX_CYCLES:
            raise ValueError("manifest validation_cycle must be an integer between 0 and 3")
    if not isinstance(manifest.get("screens"), list) or not manifest["screens"]:
        raise ValueError("manifest must contain a non-empty screens list")
    target_viewports = {_viewport(item) for item in manifest.get("target_viewports", []) if _viewport(item)}
    for screen in manifest["screens"]:
        for key in ("id", "viewport", "source", "penpot_export"):
            if key not in screen:
                raise ValueError(f"screen missing required field: {key}")
        screen_viewport = _viewport(screen.get("viewport"))
        if not screen_viewport:
            raise ValueError(f"screen {screen['id']} has invalid viewport")
        if strict and screen_viewport not in target_viewports:
            raise ValueError(f"screen {screen['id']} viewport is not in target_viewports")
        if strict:
            _validate_frame_spec(screen, screen_viewport)


def validate_transition(current_state: str, next_state: str, manifest: dict[str, Any] | None = None) -> bool:
    """Validate a state-machine edge and return True for a permitted edge."""
    if current_state not in VALID_STATES or next_state not in VALID_STATES:
        raise ValueError(f"invalid workflow state transition: {current_state} -> {next_state}")
    if next_state not in STATE_TRANSITIONS.get(current_state, set()):
        raise ValueError(f"invalid workflow state transition: {current_state} -> {next_state}")
    if next_state == "READY_FOR_USER_REVIEW" and manifest and manifest.get("route") not in {"reproduction", "directed_creation"}:
        raise ValueError("READY_FOR_USER_REVIEW requires a declared route")
    return True


validate_state_transition = validate_transition


def derive_next_state(manifest: dict[str, Any], result: dict[str, Any], structural: dict[str, Any] | None = None) -> str:
    """Derive the only state reachable after a validation score is recorded."""
    cycle = int(result.get("cycle", manifest.get("validation_cycle", 1)))
    max_cycles = int(manifest.get("max_validation_cycles", MAX_CYCLES))
    passed = bool(result.get("passed"))
    # Delivery is never inferred from a visual score alone. It only becomes
    # reachable from DS_REVALIDATING after formal approvals and a passing
    # structural inventory.
    structural_passed = structural is not None and bool(structural.get("passed"))
    if manifest.get("state") == "DS_REVALIDATING" and not structural_passed:
        return "NEEDS_REVIEW" if cycle >= max_cycles else "REFINEMENT"
    if not passed:
        return "NEEDS_REVIEW" if cycle >= max_cycles else "REFINEMENT"
    approvals = _approval_values(manifest)
    user_approved = approvals.get("user", approvals.get("version", False))
    ds_approved = approvals.get("design_system", False)
    if manifest.get("state") == "DS_REVALIDATING":
        return "READY_FOR_DELIVERY" if user_approved and ds_approved and structural_passed else "READY_FOR_USER_REVIEW"
    # A regular visual pass always returns to the user. Componentization and
    # DS revalidation are mandatory before delivery.
    return "READY_FOR_USER_REVIEW"


def validate_run(
    run_dir: str | Path,
    cycle: int,
    baseline: str | Path | None = None,
    *,
    strict: bool = False,
    inventory: str | Path | None = None,
) -> dict[str, Any]:
    if cycle < 1 or cycle > MAX_CYCLES:
        raise ValueError("cycle must be between 1 and 3")
    root = Path(run_dir)
    manifest_path = root / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    legacy = _is_legacy_manifest(manifest)
    effective_strict = strict or not legacy
    validate_manifest(manifest, strict=effective_strict)
    if effective_strict:
        _validate_canonical_frame_specs(root, manifest)
    if effective_strict and manifest["state"] not in VALIDATION_STATES:
        raise ValueError("validate is only allowed when manifest state is VALIDATING or DS_REVALIDATING")
    if effective_strict and cycle <= int(manifest.get("validation_cycle", 0)):
        raise ValueError("cycle must advance beyond manifest validation_cycle")
    output_dir = root / "cycles" / f"cycle-{cycle}"
    if output_dir.exists() and any(output_dir.iterdir()):
        raise FileExistsError(f"cycle output already exists and is immutable: {output_dir}")
    prior_path = Path(baseline) if baseline else (root / "cycles" / f"cycle-{cycle - 1}" / "score.json" if cycle > 1 else Path())
    previous = json.loads(prior_path.read_text(encoding="utf-8")) if prior_path and str(prior_path) != "." and prior_path.exists() else None
    prior_by_screen = {screen["screen"]: screen for screen in previous.get("screens", [])} if previous else {}
    if previous and not previous.get("passed", False):
        for screen in manifest["screens"]:
            prior = prior_by_screen.get(screen["id"])
            if prior and prior.get("export_sha256"):
                current_hash = sha256(read_png(str(screen["penpot_export"])))
                if current_hash == prior["export_sha256"]:
                    raise ValueError(f"screen {screen['id']} reuses the failed prior-cycle export; refactor and export a new Penpot render before validating")
    output_dir.mkdir(parents=True, exist_ok=True)
    screens = [validate_screen(screen, output_dir, prior_by_screen.get(screen["id"])) for screen in manifest["screens"]]
    aggregate_score = sum(screen["score"] for screen in screens) / len(screens)
    aggregate_coverage = sum(screen["coverage"] for screen in screens) / len(screens)
    result = {"run_id": manifest.get("run_id", root.name), "cycle": cycle, "mode": manifest.get("mode", "source"),
              "state": manifest.get("state", "VALIDATING"),
              "metric_table_version": METRIC_TABLE_VERSION,
              "metric_table": {key: {"label": value["label"], "weight": value["weight"], "limit": value["limit"]} for key, value in METRIC_TABLE.items()},
              "passed": all(screen["passed"] for screen in screens), "aggregate_score": round(aggregate_score, 2),
              "minimum_score": min(screen["score"] for screen in screens), "aggregate_coverage": round(aggregate_coverage, 6),
              "screens": screens, "regressions": any(any(issue["title"].startswith("Regression") for issue in screen["issues"]) for screen in screens)}
    result["passed"] = result["passed"] and not result["regressions"]
    structure_result = None
    inventory_ref = inventory or manifest.get("penpot_inventory") or manifest.get("structure_inventory") or manifest.get("inventory")
    if inventory_ref:
        inventory_path = Path(inventory_ref)
        if not inventory_path.is_absolute():
            inventory_path = root / inventory_path
        structure_result = validate_structure_inventory(load_inventory(inventory_path), manifest, require_reusable=effective_strict)
    elif effective_strict:
        structure_result = {"passed": False, "errors": ["strict validation requires a Penpot structural inventory JSON"],
                            "missing_inventory_keys": [], "missing_tokens": [], "missing_components": [],
                            "missing_component_instances": [], "detached_instances": 0}
    if structure_result is not None:
        result["structure_gate"] = structure_result
        if not structure_result["passed"]:
            result["passed"] = False
    result["next_state"] = derive_next_state(manifest, result, structure_result)
    if effective_strict:
        validate_transition(manifest["state"], result["next_state"], manifest)
    # Exclusive creation is the guardrail against agents overwriting a score.
    _write_exclusive_json(output_dir / "score.json", result)
    _write_exclusive_json(output_dir / "issues.json", {"run_id": result["run_id"], "cycle": cycle, "issues": [issue for screen in screens for issue in screen["issues"]]})
    render_report(result, output_dir / "report.md")
    history_path = root / "history.json"
    history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else []
    history = [entry for entry in history if entry.get("cycle") != cycle]
    history.append({"cycle": cycle, "score": result["aggregate_score"], "coverage": result["aggregate_coverage"], "passed": result["passed"], "score_path": str(output_dir / "score.json")})
    history = sorted(history, key=lambda entry: entry["cycle"])[-MAX_CYCLES:]
    if history_path.exists():
        history_path.unlink()
    history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    return result
