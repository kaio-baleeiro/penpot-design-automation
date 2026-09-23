"""Compile traceable, privacy-safe maps for Penpot source material."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Iterable, Mapping
from urllib.parse import urlsplit, urlunsplit

from .images import read_png, sha256


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sanitize_location(location: str | Path) -> str:
    """Sanitize URL/path provenance without leaking credentials or local roots."""
    value = str(location)
    parts = urlsplit(value)
    if parts.scheme.lower() in {"http", "https"} and parts.hostname:
        host = parts.hostname.lower()
        if ":" in host and not host.startswith("["):
            host = f"[{host}]"
        try:
            port = parts.port
        except ValueError:
            port = None
        netloc = host if port is None else f"{host}:{port}"
        return urlunsplit((parts.scheme.lower(), netloc, parts.path or "/", "", ""))
    candidate = Path(value)
    try:
        resolved = candidate.resolve()
        cwd = Path.cwd().resolve()
        safe = resolved.relative_to(cwd).as_posix()
    except (OSError, ValueError):
        safe = candidate.name or "source"
    safe = re.sub(r"[\x00-\x1f\x7f]", "", safe).replace("\\", "/")
    return safe.lstrip("/") or "source"


def stable_source_id(kind: str, digest: str) -> str:
    """Return an identity stable across runs and independent of local paths."""
    normalized_kind = re.sub(r"[^a-z0-9_-]+", "-", kind.lower()).strip("-") or "source"
    normalized_digest = re.sub(r"[^0-9a-f]", "", digest.lower())
    if not normalized_digest:
        raise ValueError("source digest must contain hexadecimal characters")
    return f"src-{normalized_kind}-{normalized_digest[:24]}"


def _file_sha256(path: str | Path) -> str:
    source = Path(path)
    if source.is_file():
        return hashlib.sha256(source.read_bytes()).hexdigest()
    if not source.is_dir():
        raise ValueError("source path must be an existing file or directory")
    digest = hashlib.sha256()
    excluded_dirs = {".git", "node_modules", ".next", "dist", "build", ".venv", "venv", "__pycache__"}
    excluded_names = {".env", ".env.local", ".env.production", ".env.development"}
    files = sorted(
        item for item in source.rglob("*")
        if item.is_file()
        and not any(part in excluded_dirs for part in item.relative_to(source).parts)
        and item.name not in excluded_names
        and not item.name.endswith((".pem", ".key"))
    )
    for item in files:
        relative = item.relative_to(source).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        try:
            data = item.read_bytes()
        except OSError:
            continue
        digest.update(len(data).to_bytes(8, "big"))
        digest.update(data)
    return digest.hexdigest()


def _url_source(value: str, *, confidence: float = 0.9, precedence: int = 1,
                anchors: Iterable[Any] | None = None) -> dict[str, Any]:
    safe = sanitize_location(value)
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return {"source_id": stable_source_id("url", digest), "kind": "url", "location": safe,
            "sha256": digest, "confidence": float(confidence),
            "anchors": list(anchors or [{"type": "canonical-location", "value": safe}]),
            "precedence": int(precedence), "relationships": [], "conflicts": []}


def _file_source(value: str | Path, kind: str, *, confidence: float, precedence: int,
                 anchors: Iterable[Any] | None = None) -> dict[str, Any]:
    path = Path(value)
    digest = _file_sha256(path)
    safe = sanitize_location(path)
    default_anchor = {"type": "repository" if path.is_dir() else "file", "value": Path(safe).name}
    return {"source_id": stable_source_id(kind, digest), "kind": kind, "location": safe,
            "sha256": digest, "confidence": float(confidence),
            "anchors": list(anchors or [default_anchor]),
            "precedence": int(precedence), "relationships": [], "conflicts": []}


def _normalize_source(source: Mapping[str, Any] | str | Path, *, default_precedence: int) -> dict[str, Any]:
    """Normalize a descriptor while never persisting raw URL/code data."""
    if isinstance(source, Mapping):
        kind = str(source.get("kind") or source.get("type") or "screenshot").lower()
        value = source.get("location", source.get("path", source.get("value")))
        confidence = float(source.get("confidence", 0.8))
        precedence = int(source.get("precedence", default_precedence))
        anchors = source.get("anchors")
    else:
        kind, value, confidence, precedence, anchors = "screenshot", source, 0.8, default_precedence, None
    if not isinstance(value, (str, Path)) or not value:
        raise ValueError("source descriptor requires a location or value")
    if kind == "url":
        return _url_source(str(value), confidence=confidence, precedence=precedence, anchors=anchors)
    if kind not in {"screenshot", "code"}:
        raise ValueError(f"unsupported source kind: {kind}")
    return _file_source(value, kind, confidence=confidence, precedence=precedence, anchors=anchors)


def compile_source_map(
    sources: Iterable[Mapping[str, Any] | str | Path] | None = None,
    *, url: str | None = None, screenshot: str | Path | None = None,
    code: str | Path | None = None, output: str | Path | None = None,
    relationships: Iterable[Mapping[str, Any]] | None = None,
    conflicts: Iterable[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Compile URL/screenshot/code provenance into one traceable map."""
    descriptors: list[Mapping[str, Any] | str | Path] = list(sources or [])
    if url is not None:
        descriptors.append({"kind": "url", "location": url, "precedence": 1, "confidence": 0.9})
    if screenshot is not None:
        descriptors.append({"kind": "screenshot", "location": screenshot, "precedence": 2, "confidence": 0.95})
    if code is not None:
        descriptors.append({"kind": "code", "location": code, "precedence": 3, "confidence": 0.85})
    compiled: list[dict[str, Any]] = []
    conflicts_out = list(conflicts or [])
    seen: dict[str, dict[str, Any]] = {}
    for index, descriptor in enumerate(descriptors, start=1):
        item = _normalize_source(descriptor, default_precedence=index)
        previous = seen.get(item["source_id"])
        if previous is not None and previous != item:
            conflict = {"source_id": item["source_id"], "reason": "metadata-mismatch",
                        "sources": [previous["location"], item["location"]]}
            conflicts_out.append(conflict)
            previous.setdefault("conflicts", []).append(conflict)
        elif previous is None:
            seen[item["source_id"]] = item
            compiled.append(item)
    compiled.sort(key=lambda item: (item["precedence"], item["source_id"]))
    ids = [item["source_id"] for item in compiled]
    relation_list = [dict(item) for item in (relationships or [])]
    for left, right in zip(compiled, compiled[1:]):
        relation = {"from": left["source_id"], "to": right["source_id"], "kind": "derived-from"}
        relation_list.append(relation)
        left["relationships"].append(relation)
    result = {"version": "1.0", "mapped_at": _utc(), "sources": compiled,
              "precedence": ids, "relationships": relation_list, "conflicts": conflicts_out}
    if output is not None:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("x", encoding="utf-8") as handle:
            json.dump(result, handle, ensure_ascii=False, indent=2)
    return result


def map_screenshot(path: str | Path, output: str | Path, *, threshold: int = 12,
                   viewport: tuple[int, int] | None = None,
                   capture_mode: str = "viewport") -> dict[str, Any]:
    """Map a screenshot and include its traceable source descriptor."""
    if capture_mode not in {"viewport", "full_page", "bounded_state"}:
        raise ValueError("capture_mode must be viewport, full_page, or bounded_state")
    if capture_mode != "viewport" and viewport is None:
        raise ValueError("full_page and bounded_state screenshots require their observation viewport")
    if viewport is not None and (viewport[0] <= 0 or viewport[1] <= 0):
        raise ValueError("viewport dimensions must be positive")
    image = read_png(str(path))
    observation_viewport = viewport or (image.width, image.height)
    background = image.pixel(0, 0)
    points: list[tuple[int, int]] = []
    colors = Counter()
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.pixel(x, y)
            quantized = tuple((value // 16) * 16 for value in pixel)
            colors[quantized] += 1
            if max(abs(pixel[i] - background[i]) for i in range(3)) > threshold:
                points.append((x, y))
    if points:
        xs, ys = zip(*points)
        content = {"x": min(xs), "y": min(ys), "width": max(xs) - min(xs) + 1, "height": max(ys) - min(ys) + 1}
    else:
        content = {"x": 0, "y": 0, "width": image.width, "height": image.height}
    descriptor = _file_source(path, "screenshot", confidence=0.95, precedence=1,
                              anchors=[{"type": "viewport", "bounds": {"x": 0, "y": 0, "width": observation_viewport[0], "height": observation_viewport[1]}},
                                       {"type": "capture-bounds", "bounds": {"x": 0, "y": 0, "width": image.width, "height": image.height}},
                                       {"type": "content-bounds", "bounds": content}])
    safe_location = descriptor["location"]
    result = {"version": "1.0", "mapped_at": _utc(), "source": safe_location,
              "location": safe_location, "source_id": descriptor["source_id"],
              "source_type": "screenshot", "sha256": sha256(image),
              "file_sha256": descriptor["sha256"], "confidence": descriptor["confidence"],
              "anchors": descriptor["anchors"], "precedence": [descriptor["source_id"]],
              "relationships": [], "conflicts": [],
              "capture_mode": capture_mode,
              "viewport": {"width": observation_viewport[0], "height": observation_viewport[1]},
              "screenshot_dimensions": {"width": image.width, "height": image.height},
              "background": list(background), "content_bounds": content,
              "dominant_colors": [{"rgb": list(color), "pixels": count} for color, count in colors.most_common(12)],
              "regions": [{"id": "viewport", "kind": "viewport", "bounds": {"x": 0, "y": 0, "width": observation_viewport[0], "height": observation_viewport[1]}},
                          {"id": "capture", "kind": "capture-bounds", "bounds": {"x": 0, "y": 0, "width": image.width, "height": image.height}},
                          {"id": "content", "kind": "content-bounds", "bounds": content}],
              "mapping_notes": ["Heuristic bounds use the top-left pixel as background; review against DOM/component metadata when available."]}
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, ensure_ascii=False, indent=2)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile a privacy-safe Penpot source map")
    parser.add_argument("--image", help="Map one screenshot (legacy mode)")
    parser.add_argument("--url")
    parser.add_argument("--screenshot")
    parser.add_argument("--code")
    parser.add_argument("--output", required=True)
    parser.add_argument("--threshold", type=int, default=12)
    parser.add_argument("--viewport", help="Observation viewport WxH for full_page/bounded_state screenshots")
    parser.add_argument("--capture-mode", choices=("viewport", "full_page", "bounded_state"), default="viewport")
    args = parser.parse_args(argv)
    from scripts.workflow_guard import require
    require("design")
    if args.image:
        viewport = tuple(int(value) for value in args.viewport.lower().split("x", 1)) if args.viewport else None
        map_screenshot(args.image, args.output, threshold=args.threshold, viewport=viewport,
                       capture_mode=args.capture_mode)
    elif not any((args.url, args.screenshot, args.code)):
        parser.error("provide --url, --screenshot, --code, or --image")
    else:
        compile_source_map(url=args.url, screenshot=args.screenshot, code=args.code, output=args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
