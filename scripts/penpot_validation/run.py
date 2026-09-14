"""Run lifecycle and command-line entrypoint for the validation workflow."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
from typing import Any

from .capture import capture_url
from .frame import derive_frame_spec, write_frame_spec
from .source_map import map_screenshot
from .validator import validate_manifest, validate_run, _is_legacy_manifest


def start_run(run_dir: str | Path, manifest: str | Path | dict[str, Any]) -> dict[str, Any]:
    root = Path(run_dir)
    root.mkdir(parents=True, exist_ok=True)
    if isinstance(manifest, (str, Path)):
        payload = json.loads(Path(manifest).read_text(encoding="utf-8"))
    else:
        payload = dict(manifest)
    # Old callers use a deliberately small image-only fixture.  It remains
    # accepted through the Python API; the CLI always selects strict mode.
    validate_manifest(payload, strict=not _is_legacy_manifest(payload))
    payload.setdefault("run_id", root.name)
    payload.setdefault("created_at", datetime.now(timezone.utc).isoformat())
    manifest_path = root / "manifest.json"
    if manifest_path.exists():
        raise FileExistsError(f"run manifest already exists and is immutable: {manifest_path}")
    manifest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    (root / "cycles").mkdir(exist_ok=True)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Penpot source capture, mapping and validation")
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("start-run")
    start.add_argument("--run-dir", required=True)
    start.add_argument("--manifest", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--run-dir", required=True)
    validate.add_argument("--cycle", type=int, required=True)
    validate.add_argument("--baseline")
    validate.add_argument("--inventory", help="Penpot structural inventory JSON")
    capture = commands.add_parser("capture")
    capture.add_argument("--url", required=True)
    capture.add_argument("--output", required=True)
    capture.add_argument("--viewport", default="1440x900")
    capture.add_argument("--full-page", action="store_true")
    capture.add_argument("--wait-ms", type=int, default=500)
    capture.add_argument("--scroll-probes", type=int, default=2, choices=range(0, 4))
    capture.add_argument("--frame-bounds", help="Approved frame bounds WxH for capture beyond the viewport")
    capture.add_argument("--storage-state", help="Playwright storage-state JSON for private/authenticated sources")
    mapping = commands.add_parser("map-screenshot")
    mapping.add_argument("--image", required=True)
    mapping.add_argument("--output", required=True)
    mapping.add_argument("--threshold", type=int, default=12)
    mapping.add_argument("--viewport", help="Observation viewport WxH for full_page/bounded_state screenshots")
    mapping.add_argument("--capture-mode", choices=("viewport", "full_page", "bounded_state"), default="viewport")
    sizing = commands.add_parser("frame-spec")
    sizing.add_argument("--capture", required=True)
    sizing.add_argument("--screen-id", required=True)
    sizing.add_argument("--output", required=True)
    sizing.add_argument("--horizontal-policy", choices=("intentional_page", "container_overflow", "accidental_overflow"))
    sizing.add_argument("--horizontal-evidence", action="append")
    sizing.add_argument("--dynamic-boundary", type=int)
    args = parser.parse_args(argv)
    if args.command == "start-run":
        payload = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        if _is_legacy_manifest(payload):
            raise ValueError("CLI start-run requires a complete schema 1.0 manifest")
        start_run(args.run_dir, payload)
    elif args.command == "validate":
        validate_run(args.run_dir, args.cycle, args.baseline, strict=True, inventory=args.inventory)
    elif args.command == "map-screenshot":
        viewport = tuple(int(value) for value in args.viewport.lower().split("x", 1)) if args.viewport else None
        map_screenshot(args.image, args.output, threshold=args.threshold, viewport=viewport,
                       capture_mode=args.capture_mode)
    elif args.command == "capture":
        width, height = (int(value) for value in args.viewport.lower().split("x", 1))
        frame_bounds = tuple(int(value) for value in args.frame_bounds.lower().split("x", 1)) if args.frame_bounds else None
        import asyncio
        asyncio.run(capture_url(args.url, args.output, width, height, full_page=args.full_page,
                                wait_ms=args.wait_ms, storage_state=args.storage_state,
                                scroll_probes=args.scroll_probes, frame_bounds=frame_bounds))
    elif args.command == "frame-spec":
        capture_payload = json.loads(Path(args.capture).read_text(encoding="utf-8"))
        spec = derive_frame_spec(
            capture_payload,
            screen_id=args.screen_id,
            horizontal_policy=args.horizontal_policy,
            horizontal_evidence=args.horizontal_evidence,
            dynamic_boundary=args.dynamic_boundary,
        )
        write_frame_spec(spec, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
