"""Versioned deterministic visual metrics.

These metrics are intentionally image-only heuristics. They are useful as a
repeatable gate, but cannot prove semantic typography, editable Penpot
structure, or asset identity without DOM/Penpot metadata. The report records
that limitation next to every score.
"""

from __future__ import annotations

from collections import Counter
from typing import Any

from .images import Image, connected_components, resize_nearest


METRIC_TABLE_VERSION = "penpot-visual-v1"
METRIC_TABLE = {
    "geometry_alignment": {"weight": 30, "label": "Geometry/alignment", "limit": "Image bounds and content bounding-box alignment."},
    "spacing_grid": {"weight": 20, "label": "Spacing/grid", "limit": "Row/column occupancy profiles; not a substitute for measured design tokens."},
    "typography": {"weight": 15, "label": "Typography", "limit": "Dark-pixel density and row distribution; font family and text semantics are not observable from pixels."},
    "color_border_shadow": {"weight": 15, "label": "Color/border/shadow", "limit": "Quantized color histogram; subtle border and shadow semantics may be ambiguous."},
    "content_density": {"weight": 10, "label": "Content/density", "limit": "Foreground occupancy ratio and mask coverage; cannot verify copy correctness."},
    "assets": {"weight": 10, "label": "Assets", "limit": "Connected-component count/area signature; cannot prove asset provenance or vector editability."},
}


def _mask(image: Image, threshold: int = 12) -> list[bool]:
    bg = image.pixel(0, 0)
    return [max(abs(image.pixels[i + c] - bg[c]) for c in range(3)) > threshold for i in range(0, len(image.pixels), 3)]


def _bbox(mask: list[bool], width: int, height: int) -> tuple[int, int, int, int]:
    points = [(i % width, i // width) for i, active in enumerate(mask) if active]
    if not points:
        return 0, 0, 0, 0
    xs, ys = zip(*points)
    return min(xs), min(ys), max(xs) - min(xs) + 1, max(ys) - min(ys) + 1


def _iou(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    if not aw or not ah or not bw or not bh:
        return 1.0 if a == b else 0.0
    x0, y0 = max(ax, bx), max(ay, by)
    x1, y1 = min(ax + aw, bx + bw), min(ay + ah, by + bh)
    intersection = max(0, x1 - x0) * max(0, y1 - y0)
    union = aw * ah + bw * bh - intersection
    return intersection / union if union else 0.0


def _mae(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    size = min(len(a), len(b))
    return sum(abs(a[i] - b[i]) for i in range(size)) / size


def _profile(mask: list[bool], width: int, height: int, axis: str) -> list[float]:
    length = height if axis == "rows" else width
    span = width if axis == "rows" else height
    values = []
    for index in range(length):
        count = 0
        for offset in range(span):
            pos = index * width + offset if axis == "rows" else offset * width + index
            count += int(mask[pos])
        values.append(count / span)
    return values


def _dark_profile(image: Image) -> list[float]:
    values = []
    for y in range(image.height):
        dark = 0
        for x in range(image.width):
            r, g, b = image.pixel(x, y)
            dark += int((r + g + b) / 3 < 170)
        values.append(dark / image.width)
    return values


def _histogram(image: Image) -> dict[tuple[int, int, int], float]:
    counts: Counter[tuple[int, int, int]] = Counter()
    for i in range(0, len(image.pixels), 3):
        counts[tuple((image.pixels[i + c] // 32) * 32 for c in range(3))] += 1
    total = image.width * image.height
    return {key: value / total for key, value in counts.items()}


def _histogram_similarity(a: Image, b: Image) -> float:
    ah, bh = _histogram(a), _histogram(b)
    keys = set(ah) | set(bh)
    return max(0.0, 1.0 - sum(abs(ah.get(key, 0.0) - bh.get(key, 0.0)) for key in keys) / 2.0)


def _component_signature(mask: list[bool], width: int, height: int) -> tuple[int, float]:
    values = [255 if active else 0 for active in mask]
    components = connected_components(values, width, height, threshold=32)
    meaningful = [component for component in components if component[4] >= max(1, width * height // 200)]
    area = sum(component[4] for component in meaningful) / (width * height)
    return len(meaningful), area


def compare_metrics(source: Image, exported: Image) -> dict[str, Any]:
    target = resize_nearest(exported, source.width, source.height)
    source_mask, target_mask = _mask(source), _mask(target)
    source_box, target_box = _bbox(source_mask, source.width, source.height), _bbox(target_mask, target.width, target.height)
    viewport_match = int(source.width == exported.width and source.height == exported.height)

    geometry_iou = _iou(source_box, target_box)
    source_area = source_box[2] * source_box[3]
    target_area = target_box[2] * target_box[3]
    area_similarity = 1.0 - min(1.0, abs(source_area - target_area) / max(1, source_area, target_area))
    geometry = (0.65 * geometry_iou + 0.25 * area_similarity + 0.10 * viewport_match) * 100

    row_mae = _mae(_profile(source_mask, source.width, source.height, "rows"), _profile(target_mask, target.width, target.height, "rows"))
    col_mae = _mae(_profile(source_mask, source.width, source.height, "cols"), _profile(target_mask, target.width, target.height, "cols"))
    spacing = max(0.0, 1.0 - (row_mae + col_mae) / 2.0) * 100

    dark_ratio_a = sum(_dark_profile(source)) / source.height
    dark_ratio_b = sum(_dark_profile(target)) / target.height
    typography_density = 1.0 - min(1.0, abs(dark_ratio_a - dark_ratio_b) / max(0.05, dark_ratio_a, dark_ratio_b))
    typography_rows = 1.0 - _mae(_dark_profile(source), _dark_profile(target))
    typography = max(0.0, (0.55 * typography_density + 0.45 * typography_rows)) * 100

    color = _histogram_similarity(source, target) * 100
    source_density, target_density = sum(source_mask) / len(source_mask), sum(target_mask) / len(target_mask)
    content_coverage = sum(a == b for a, b in zip(source_mask, target_mask)) / len(source_mask)
    density_similarity = 1.0 - min(1.0, abs(source_density - target_density) / max(0.05, source_density, target_density))
    content = (0.60 * content_coverage + 0.40 * density_similarity) * 100

    components_a, area_a = _component_signature(source_mask, source.width, source.height)
    components_b, area_b = _component_signature(target_mask, target.width, target.height)
    count_similarity = 1.0 - min(1.0, abs(components_a - components_b) / max(1, components_a, components_b))
    component_area_similarity = 1.0 - min(1.0, abs(area_a - area_b) / max(0.05, area_a, area_b))
    assets = (0.60 * count_similarity + 0.40 * component_area_similarity) * 100

    raw = {
        "geometry_alignment": (geometry, f"content bbox IoU={geometry_iou:.3f}, area similarity={area_similarity:.3f}, viewport_match={viewport_match}", {"source_bbox": source_box, "export_bbox": target_box, "iou": round(geometry_iou, 6)}),
        "spacing_grid": (spacing, f"row profile MAE={row_mae:.3f}, column profile MAE={col_mae:.3f}", {"row_mae": round(row_mae, 6), "column_mae": round(col_mae, 6)}),
        "typography": (typography, f"dark density similarity={typography_density:.3f}, row similarity={typography_rows:.3f}; image-only heuristic", {"source_dark_ratio": round(dark_ratio_a, 6), "export_dark_ratio": round(dark_ratio_b, 6)}),
        "color_border_shadow": (color, f"quantized RGB histogram similarity={color / 100:.3f}", {"histogram_bins": 32}),
        "content_density": (content, f"mask coverage={content_coverage:.3f}, density similarity={density_similarity:.3f}", {"source_density": round(source_density, 6), "export_density": round(target_density, 6)}),
        "assets": (assets, f"component count similarity={count_similarity:.3f}, area similarity={component_area_similarity:.3f}; image-only heuristic", {"source_components": components_a, "export_components": components_b}),
    }
    metrics: dict[str, Any] = {}
    weighted_total = 0.0
    for key, (score, explanation, evidence) in raw.items():
        definition = METRIC_TABLE[key]
        score = round(max(0.0, min(100.0, score)), 2)
        contribution = score * definition["weight"] / 100
        weighted_total += contribution
        metrics[key] = {"label": definition["label"], "weight": definition["weight"], "score": score, "weighted_contribution": round(contribution, 2), "explanation": explanation, "evidence": evidence, "limit": definition["limit"]}
    return {"version": METRIC_TABLE_VERSION, "metrics": metrics, "weighted_score": round(weighted_total, 2), "table": METRIC_TABLE}
