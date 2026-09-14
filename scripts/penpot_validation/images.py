"""Small, dependency-free RGB PNG and comparison helpers.

Pillow is listed as an optional accelerator, but keeping the core codec here
makes CI and agent runs deterministic when dependencies are not installed.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import struct
import zlib
from typing import Iterable, Sequence


RGB = tuple[int, int, int]


@dataclass(frozen=True)
class Image:
    width: int
    height: int
    pixels: bytes  # packed RGB, three bytes per pixel

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("image dimensions must be positive")
        if len(self.pixels) != self.width * self.height * 3:
            raise ValueError("RGB pixel buffer has the wrong size")

    def pixel(self, x: int, y: int) -> RGB:
        i = (y * self.width + x) * 3
        return self.pixels[i], self.pixels[i + 1], self.pixels[i + 2]

    def with_pixels(self, pixels: bytes) -> "Image":
        return Image(self.width, self.height, pixels)


def solid(width: int, height: int, color: RGB) -> Image:
    return Image(width, height, bytes(color) * (width * height))


def draw_rect(image: Image, x: int, y: int, width: int, height: int, color: RGB) -> Image:
    """Return a copy with a clipped filled rectangle, useful for fixtures."""
    data = bytearray(image.pixels)
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(image.width, x + width), min(image.height, y + height)
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            i = (yy * image.width + xx) * 3
            data[i : i + 3] = bytes(color)
    return image.with_pixels(bytes(data))


def _chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def write_png(image: Image, path: str) -> None:
    rows = b"".join(b"\x00" + image.pixels[y * image.width * 3 : (y + 1) * image.width * 3] for y in range(image.height))
    content = b"\x89PNG\r\n\x1a\n"
    content += _chunk(b"IHDR", struct.pack(">IIBBBBB", image.width, image.height, 8, 2, 0, 0, 0))
    content += _chunk(b"IDAT", zlib.compress(rows, 9))
    content += _chunk(b"IEND", b"")
    with open(path, "wb") as handle:
        handle.write(content)


def _unfilter(raw: bytes, width: int, height: int, channels: int) -> bytes:
    stride = width * channels
    rows = []
    previous = bytearray(stride)
    pos = 0
    for _ in range(height):
        filter_type = raw[pos]
        pos += 1
        row = bytearray(raw[pos : pos + stride])
        pos += stride
        for i in range(stride):
            left = row[i - channels] if i >= channels else 0
            up = previous[i]
            up_left = previous[i - channels] if i >= channels else 0
            if filter_type == 1:
                row[i] = (row[i] + left) & 255
            elif filter_type == 2:
                row[i] = (row[i] + up) & 255
            elif filter_type == 3:
                row[i] = (row[i] + ((left + up) // 2)) & 255
            elif filter_type == 4:
                p = left + up - up_left
                pa, pb, pc = abs(p - left), abs(p - up), abs(p - up_left)
                predictor = left if pa <= pb and pa <= pc else up if pb <= pc else up_left
                row[i] = (row[i] + predictor) & 255
            elif filter_type != 0:
                raise ValueError(f"unsupported PNG filter {filter_type}")
        rows.append(bytes(row))
        previous = row
    return b"".join(rows)


def read_png(path: str) -> Image:
    with open(path, "rb") as handle:
        blob = handle.read()
    if not blob.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"not a PNG file: {path}")
    pos, idat, width, height, bit_depth, color_type = 8, bytearray(), None, None, None, None
    while pos < len(blob):
        length = struct.unpack(">I", blob[pos : pos + 4])[0]
        kind = blob[pos + 4 : pos + 8]
        payload = blob[pos + 8 : pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            width, height, bit_depth, color_type, compression, filtering, interlace = struct.unpack(">IIBBBBB", payload)
            if bit_depth != 8 or interlace != 0 or compression != 0 or filtering != 0:
                raise ValueError("only non-interlaced 8-bit PNGs are supported")
        elif kind == b"IDAT":
            idat.extend(payload)
        elif kind == b"IEND":
            break
    if width is None or height is None or bit_depth is None or color_type is None:
        raise ValueError("PNG has no IHDR")
    channels = {0: 1, 2: 3, 4: 2, 6: 4}.get(color_type)
    if channels is None:
        raise ValueError(f"unsupported PNG color type {color_type}")
    raw = _unfilter(zlib.decompress(bytes(idat)), width, height, channels)
    rgb = bytearray()
    for i in range(0, len(raw), channels):
        if color_type == 2:
            rgb.extend(raw[i : i + 3])
        elif color_type == 6:
            rgb.extend(raw[i : i + 3])
        elif color_type == 4:
            rgb.extend(raw[i : i + 1] * 3)
        else:
            rgb.extend(raw[i : i + 1] * 3)
    return Image(width, height, bytes(rgb))


def sha256(image: Image) -> str:
    return hashlib.sha256(image.pixels).hexdigest()


def resize_nearest(image: Image, width: int, height: int) -> Image:
    if image.width == width and image.height == height:
        return image
    out = bytearray(width * height * 3)
    for y in range(height):
        sy = min(image.height - 1, int(y * image.height / height))
        for x in range(width):
            sx = min(image.width - 1, int(x * image.width / width))
            source = (sy * image.width + sx) * 3
            target = (y * width + x) * 3
            out[target : target + 3] = image.pixels[source : source + 3]
    return Image(width, height, bytes(out))


def diff_values(source: Image, exported: Image) -> tuple[Image, list[int], float, float]:
    """Return visual diff, per-pixel max delta, similarity and coverage.

    Coverage means the percentage of pixels whose max channel delta is at or
    below 32. It is intentionally independent from the weighted score.
    """
    target = resize_nearest(exported, source.width, source.height)
    values: list[int] = []
    pixels = bytearray()
    total_abs = 0
    matched = 0
    for i in range(0, len(source.pixels), 3):
        deltas = [abs(source.pixels[i + c] - target.pixels[i + c]) for c in range(3)]
        maximum = max(deltas)
        values.append(maximum)
        total_abs += sum(deltas)
        if maximum <= 32:
            matched += 1
        # red heatmap, with a faint neutral background for matched pixels
        intensity = min(255, maximum * 4)
        pixels.extend((intensity, max(0, 255 - intensity), 0))
    pixel_similarity = 1.0 - (total_abs / (len(values) * 3 * 255))
    coverage = matched / len(values)
    return Image(source.width, source.height, bytes(pixels)), values, pixel_similarity, coverage


def _draw_rect(data: bytearray, width: int, height: int, box: tuple[int, int, int, int], color: RGB, thickness: int = 2) -> None:
    x, y, w, h = box
    x0, y0, x1, y1 = max(0, x), max(0, y), min(width - 1, x + max(0, w - 1)), min(height - 1, y + max(0, h - 1))
    for t in range(thickness):
        for xx in range(x0, x1 + 1):
            for yy in (y0 + t, y1 - t):
                if 0 <= yy < height:
                    i = (yy * width + xx) * 3
                    data[i : i + 3] = bytes(color)
        for yy in range(y0, y1 + 1):
            for xx in (x0 + t, x1 - t):
                if 0 <= xx < width:
                    i = (yy * width + xx) * 3
                    data[i : i + 3] = bytes(color)


def side_by_side(source: Image, exported: Image, boxes: Sequence[tuple[int, int, int, int]]) -> Image:
    height = max(source.height, exported.height)
    left, right = resize_nearest(source, source.width, height), resize_nearest(exported, exported.width, height)
    width = left.width + right.width
    data = bytearray(width * height * 3)
    for y in range(height):
        data[y * width * 3 : y * width * 3 + left.width * 3] = left.pixels[y * left.width * 3 : (y + 1) * left.width * 3]
        data[y * width * 3 + left.width * 3 : (y + 1) * width * 3] = right.pixels[y * right.width * 3 : (y + 1) * right.width * 3]
    for box in boxes:
        _draw_rect(data, width, height, box, (255, 35, 35), 2)
        _draw_rect(data, width, height, (box[0] + left.width, box[1], box[2], box[3]), (255, 35, 35), 2)
    for y in range(height):
        i = (y * width + left.width) * 3
        data[i : i + 3] = b"\xff\xff\xff"
    return Image(width, height, bytes(data))


def overlay(source: Image, exported: Image) -> Image:
    target = resize_nearest(exported, source.width, source.height)
    data = bytes((int((source.pixels[i] + target.pixels[i]) / 2) for i in range(len(source.pixels))))
    return Image(source.width, source.height, data)


def connected_components(values: Sequence[int], width: int, height: int, threshold: int = 32) -> list[tuple[int, int, int, int, int]]:
    active = [v > threshold for v in values]
    seen = bytearray(len(active))
    components: list[tuple[int, int, int, int, int]] = []
    for start, is_active in enumerate(active):
        if not is_active or seen[start]:
            continue
        stack = [start]
        seen[start] = 1
        min_x = max_x = start % width
        min_y = max_y = start // width
        area = 0
        while stack:
            current = stack.pop()
            x, y = current % width, current // width
            area += 1
            min_x, max_x = min(min_x, x), max(max_x, x)
            min_y, max_y = min(min_y, y), max(max_y, y)
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if 0 <= nx < width and 0 <= ny < height:
                    index = ny * width + nx
                    if active[index] and not seen[index]:
                        seen[index] = 1
                        stack.append(index)
        components.append((min_x, min_y, max_x - min_x + 1, max_y - min_y + 1, area))
    return sorted(components, key=lambda item: item[4], reverse=True)
