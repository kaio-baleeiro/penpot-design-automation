"""Derive explicit Penpot frame bounds from captured document metrics."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping


HORIZONTAL_POLICIES = {
    "viewport_bounded",
    "intentional_page",
    "container_overflow",
    "accidental_overflow",
}
VERTICAL_POLICIES = {"viewport_bounded", "finite_document", "dynamic_bounded"}
CAPTURE_MODES = {"viewport", "full_page", "frame_bounds", "bounded_state"}


def _dimensions(value: Mapping[str, Any], label: str) -> tuple[int, int]:
    try:
        width = int(value["width"])
        height = int(value["height"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"{label} requires positive integer width and height") from exc
    if width <= 0 or height <= 0:
        raise ValueError(f"{label} requires positive integer width and height")
    return width, height


def _is_horizontal_container(value: Any) -> bool:
    if not isinstance(value, Mapping):
        return False
    try:
        return int(value.get("scroll_width", 0)) > int(value.get("client_width", 0)) + 2
    except (TypeError, ValueError):
        return False


def derive_frame_spec(
    capture: Mapping[str, Any],
    *,
    screen_id: str,
    horizontal_policy: str | None = None,
    horizontal_evidence: list[str] | None = None,
    dynamic_boundary: int | None = None,
) -> dict[str, Any]:
    """Create a frame decision while refusing to infer horizontal intent from width alone."""
    metrics = capture.get("document_metrics")
    if not isinstance(metrics, Mapping):
        raise ValueError("capture requires document_metrics")
    viewport = metrics.get("viewport", capture.get("viewport"))
    document = metrics.get("document")
    if not isinstance(viewport, Mapping) or not isinstance(document, Mapping):
        raise ValueError("document_metrics requires viewport and document")
    viewport_width, viewport_height = _dimensions(viewport, "viewport")
    document_width, document_height = _dimensions(document, "document")
    stable = bool(metrics.get("stable_after_wait"))
    horizontal_evidence_values = list(horizontal_evidence or [])
    evidence = ["capture:document_metrics", *horizontal_evidence_values]

    if stable:
        vertical_policy = "finite_document" if document_height > viewport_height + 2 else "viewport_bounded"
        frame_height = max(viewport_height, document_height)
        capture_mode = "full_page" if vertical_policy == "finite_document" else "viewport"
        needs_decision = False
    elif dynamic_boundary is not None:
        if dynamic_boundary < viewport_height:
            raise ValueError("dynamic boundary cannot be smaller than the viewport height")
        vertical_policy = "dynamic_bounded"
        frame_height = int(dynamic_boundary)
        capture_mode = "bounded_state"
        needs_decision = False
        evidence.append(f"approved-boundary:{frame_height}")
    else:
        vertical_policy = "dynamic_bounded"
        frame_height = viewport_height
        capture_mode = "bounded_state"
        needs_decision = True

    containers = metrics.get("scroll_containers")
    has_horizontal_container = isinstance(containers, list) and any(_is_horizontal_container(item) for item in containers)
    horizontal_overflow = document_width > viewport_width + 2
    if not horizontal_overflow:
        resolved_horizontal = "container_overflow" if has_horizontal_container else "viewport_bounded"
        frame_width = viewport_width
    elif horizontal_policy is None:
        page_overflow = metrics.get("page_overflow")
        if isinstance(page_overflow, Mapping) and not page_overflow.get("horizontal") and has_horizontal_container:
            resolved_horizontal = "container_overflow"
            frame_width = viewport_width
        else:
            resolved_horizontal = "accidental_overflow"
            frame_width = viewport_width
            needs_decision = True
    else:
        if horizontal_policy not in HORIZONTAL_POLICIES - {"viewport_bounded"}:
            raise ValueError("invalid horizontal policy for an overflowing document")
        resolved_horizontal = horizontal_policy
        if resolved_horizontal == "intentional_page":
            if not horizontal_evidence_values:
                raise ValueError("intentional page-level horizontal growth requires evidence")
            frame_width = document_width
            capture_mode = "frame_bounds"
        else:
            frame_width = viewport_width

    return {
        "schema_version": "1.0",
        "screen_id": str(screen_id),
        "viewport": {"width": viewport_width, "height": viewport_height},
        "document": {"width": document_width, "height": document_height},
        "frame": {"width": frame_width, "height": frame_height},
        "vertical_policy": vertical_policy,
        "horizontal_policy": resolved_horizontal,
        "capture_mode": capture_mode,
        "stable": stable,
        "build_ready": not needs_decision,
        "requires_user_decision": needs_decision,
        "evidence": evidence,
    }


def write_frame_spec(value: Mapping[str, Any], output: str | Path) -> None:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as handle:
        json.dump(dict(value), handle, ensure_ascii=False, indent=2)
