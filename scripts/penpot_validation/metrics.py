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


METRIC_TABLE_VERSION = "penpot-visual-v2"
METRIC_TABLE = {
    "geometry_alignment": {"weight": 25, "label": "Geometry/alignment", "limit": "Tile occupancy and edge alignment; semantic hierarchy still requires review."},
    "spacing_grid": {"weight": 15, "label": "Spacing/grid", "limit": "Local row/column and edge profiles; not a substitute for measured design tokens."},
    "typography": {"weight": 15, "label": "Typography", "limit": "Local dark-pixel and edge density; font identity and copy require metadata."},
    "color_border_shadow": {"weight": 15, "label": "Color/border/shadow", "limit": "Per-region RGB similarity and histogram evidence; subtle semantics may remain ambiguous."},
    "content_density": {"weight": 15, "label": "Content/density", "limit": "Foreground agreement is evaluated per region so blank canvas cannot dominate."},
    "assets": {"weight": 15, "label": "Assets", "limit": "Local pixel/edge agreement helps detect wrong imagery but provenance still requires a manifest."},
}

TILE_SIZE = 120
MAX_ANALYSIS_WIDTH = 480


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


def _percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, int((len(ordered) - 1) * fraction)))]


def _luminance(image: Image, x: int, y: int) -> float:
    r, g, b = image.pixel(x, y)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _tile_evidence(source: Image, target: Image) -> dict[str, Any]:
    """Compare local regions so a large blank background cannot hide bad UI.

    Every tile gets a floor weight and gains importance from foreground and
    edges in either image. The lower-quartile penalty makes repeated weak
    sections visible on long pages instead of averaging them away.
    """
    source_mask, target_mask = _mask(source), _mask(target)
    tiles: list[dict[str, Any]] = []
    for y0 in range(0, source.height, TILE_SIZE):
        for x0 in range(0, source.width, TILE_SIZE):
            x1, y1 = min(source.width, x0 + TILE_SIZE), min(source.height, y0 + TILE_SIZE)
            count = max(1, (x1 - x0) * (y1 - y0))
            absolute = active_source = active_target = overlap = union = 0
            source_edges = target_edges = edge_overlap = edge_union = 0
            dark_source = dark_target = 0
            for y in range(y0, y1):
                for x in range(x0, x1):
                    pos = y * source.width + x
                    i = pos * 3
                    absolute += sum(abs(source.pixels[i + c] - target.pixels[i + c]) for c in range(3))
                    sa, ta = source_mask[pos], target_mask[pos]
                    active_source += int(sa)
                    active_target += int(ta)
                    overlap += int(sa and ta)
                    union += int(sa or ta)
                    dark_source += int(_luminance(source, x, y) < 170)
                    dark_target += int(_luminance(target, x, y) < 170)
                    if x + 1 < x1 and y + 1 < y1:
                        se = abs(_luminance(source, x + 1, y) - _luminance(source, x, y)) > 20 or abs(_luminance(source, x, y + 1) - _luminance(source, x, y)) > 20
                        te = abs(_luminance(target, x + 1, y) - _luminance(target, x, y)) > 20 or abs(_luminance(target, x, y + 1) - _luminance(target, x, y)) > 20
                        source_edges += int(se)
                        target_edges += int(te)
                        edge_overlap += int(se and te)
                        edge_union += int(se or te)
            pixel_similarity = max(0.0, 1.0 - absolute / (count * 3 * 255))
            foreground_iou = overlap / union if union else 1.0
            edge_iou = edge_overlap / edge_union if edge_union else (1.0 if source_edges == target_edges else 0.0)
            density = 1.0 - min(1.0, abs(active_source - active_target) / max(1, active_source, active_target, count // 40))
            darkness = 1.0 - min(1.0, abs(dark_source - dark_target) / max(1, dark_source, dark_target, count // 40))
            score = 0.45 * pixel_similarity + 0.25 * foreground_iou + 0.20 * edge_iou + 0.10 * density
            importance = 0.20 + 2.5 * max(active_source, active_target) / count + 3.0 * max(source_edges, target_edges) / count
            tiles.append({
                "bounds": {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0},
                "score": score,
                "pixel_similarity": pixel_similarity,
                "foreground_iou": foreground_iou,
                "edge_iou": edge_iou,
                "density_similarity": density,
                "dark_similarity": darkness,
                "importance": importance,
            })
    weight = sum(tile["importance"] for tile in tiles) or 1.0
    weighted = lambda key: sum(tile[key] * tile["importance"] for tile in tiles) / weight
    local_scores = [tile["score"] for tile in tiles]
    worst = sorted(tiles, key=lambda tile: tile["score"])[: min(8, len(tiles))]
    return {
        "weighted_score": 0.75 * weighted("score") + 0.25 * _percentile(local_scores, 0.20),
        "pixel_similarity": weighted("pixel_similarity"),
        "foreground_iou": weighted("foreground_iou"),
        "edge_iou": weighted("edge_iou"),
        "density_similarity": weighted("density_similarity"),
        "dark_similarity": weighted("dark_similarity"),
        "regional_floor": _percentile(local_scores, 0.20),
        "worst_regions": [{**tile["bounds"], "score": round(tile["score"] * 100, 2)} for tile in worst],
        "tile_count": len(tiles),
    }


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
    viewport_match = int(source.width == exported.width and source.height == exported.height)
    target = resize_nearest(exported, source.width, source.height)
    if source.width > MAX_ANALYSIS_WIDTH:
        analysis_height = max(1, round(source.height * MAX_ANALYSIS_WIDTH / source.width))
        source = resize_nearest(source, MAX_ANALYSIS_WIDTH, analysis_height)
        target = resize_nearest(target, MAX_ANALYSIS_WIDTH, analysis_height)
    local = _tile_evidence(source, target)
    source_mask, target_mask = _mask(source), _mask(target)
    source_box, target_box = _bbox(source_mask, source.width, source.height), _bbox(target_mask, target.width, target.height)

    geometry_iou = _iou(source_box, target_box)
    source_area = source_box[2] * source_box[3]
    target_area = target_box[2] * target_box[3]
    area_similarity = 1.0 - min(1.0, abs(source_area - target_area) / max(1, source_area, target_area))
    geometry = (0.25 * geometry_iou + 0.15 * area_similarity + 0.10 * viewport_match + 0.30 * local["foreground_iou"] + 0.20 * local["edge_iou"]) * 100

    row_mae = _mae(_profile(source_mask, source.width, source.height, "rows"), _profile(target_mask, target.width, target.height, "rows"))
    col_mae = _mae(_profile(source_mask, source.width, source.height, "cols"), _profile(target_mask, target.width, target.height, "cols"))
    spacing = max(0.0, 0.35 * (1.0 - (row_mae + col_mae) / 2.0) + 0.40 * local["edge_iou"] + 0.25 * local["regional_floor"]) * 100

    dark_ratio_a = sum(_dark_profile(source)) / source.height
    dark_ratio_b = sum(_dark_profile(target)) / target.height
    typography_density = 1.0 - min(1.0, abs(dark_ratio_a - dark_ratio_b) / max(0.05, dark_ratio_a, dark_ratio_b))
    typography_rows = 1.0 - _mae(_dark_profile(source), _dark_profile(target))
    typography = max(0.0, (0.25 * typography_density + 0.25 * typography_rows + 0.35 * local["dark_similarity"] + 0.15 * local["edge_iou"])) * 100

    color = (0.35 * _histogram_similarity(source, target) + 0.45 * local["pixel_similarity"] + 0.20 * local["regional_floor"]) * 100
    source_density, target_density = sum(source_mask) / len(source_mask), sum(target_mask) / len(target_mask)
    content_coverage = sum(a == b for a, b in zip(source_mask, target_mask)) / len(source_mask)
    density_similarity = 1.0 - min(1.0, abs(source_density - target_density) / max(0.05, source_density, target_density))
    content = (0.15 * content_coverage + 0.20 * density_similarity + 0.40 * local["foreground_iou"] + 0.25 * local["regional_floor"]) * 100

    components_a, area_a = _component_signature(source_mask, source.width, source.height)
    components_b, area_b = _component_signature(target_mask, target.width, target.height)
    count_similarity = 1.0 - min(1.0, abs(components_a - components_b) / max(1, components_a, components_b))
    component_area_similarity = 1.0 - min(1.0, abs(area_a - area_b) / max(0.05, area_a, area_b))
    assets = (0.15 * count_similarity + 0.10 * component_area_similarity + 0.45 * local["pixel_similarity"] + 0.30 * local["edge_iou"]) * 100

    raw = {
        "geometry_alignment": (geometry, f"local foreground IoU={local['foreground_iou']:.3f}, edge IoU={local['edge_iou']:.3f}, bbox IoU={geometry_iou:.3f}", {"source_bbox": source_box, "export_bbox": target_box, "iou": round(geometry_iou, 6), "tile_count": local["tile_count"]}),
        "spacing_grid": (spacing, f"edge IoU={local['edge_iou']:.3f}, regional floor={local['regional_floor']:.3f}, row/column MAE={row_mae:.3f}/{col_mae:.3f}", {"row_mae": round(row_mae, 6), "column_mae": round(col_mae, 6), "regional_floor": round(local["regional_floor"], 6)}),
        "typography": (typography, f"local dark similarity={local['dark_similarity']:.3f}, edge IoU={local['edge_iou']:.3f}; image-only heuristic", {"source_dark_ratio": round(dark_ratio_a, 6), "export_dark_ratio": round(dark_ratio_b, 6)}),
        "color_border_shadow": (color, f"local pixel similarity={local['pixel_similarity']:.3f}, regional floor={local['regional_floor']:.3f}", {"histogram_bins": 32}),
        "content_density": (content, f"local foreground IoU={local['foreground_iou']:.3f}, regional floor={local['regional_floor']:.3f}", {"source_density": round(source_density, 6), "export_density": round(target_density, 6)}),
        "assets": (assets, f"local pixel similarity={local['pixel_similarity']:.3f}, edge IoU={local['edge_iou']:.3f}; image-only heuristic", {"source_components": components_a, "export_components": components_b}),
    }
    metrics: dict[str, Any] = {}
    weighted_total = 0.0
    for key, (score, explanation, evidence) in raw.items():
        definition = METRIC_TABLE[key]
        score = round(max(0.0, min(100.0, score)), 2)
        contribution = score * definition["weight"] / 100
        weighted_total += contribution
        metrics[key] = {"label": definition["label"], "weight": definition["weight"], "score": score, "weighted_contribution": round(contribution, 2), "explanation": explanation, "evidence": evidence, "limit": definition["limit"]}
    calibrated = min(weighted_total, local["weighted_score"] * 100 + 8.0)
    return {"version": METRIC_TABLE_VERSION, "metrics": metrics, "weighted_score": round(calibrated, 2), "table": METRIC_TABLE,
            "regional": {"score": round(local["weighted_score"] * 100, 2), "floor": round(local["regional_floor"] * 100, 2), "worst_regions": local["worst_regions"]}}
