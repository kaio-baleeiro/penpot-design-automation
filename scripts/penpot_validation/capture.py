"""Playwright source acquisition with a provenance manifest."""

from __future__ import annotations

import argparse
import asyncio
import base64
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit, urlunsplit

from .images import read_png


MEASURE_DOCUMENT_JS = """() => {
  const root = document.documentElement;
  const body = document.body;
  const rootStyle = getComputedStyle(root);
  const bodyStyle = body ? getComputedStyle(body) : null;
  const bodyWidth = body ? Math.max(body.scrollWidth, body.offsetWidth, body.clientWidth) : 0;
  const bodyHeight = body ? Math.max(body.scrollHeight, body.offsetHeight, body.clientHeight) : 0;
  let contentLeft = 0;
  let contentRight = window.innerWidth;
  let contentBottom = window.innerHeight;
  let widestElement = null;
  const scrollContainers = [];
  const outsideViewport = [];
  for (const node of document.querySelectorAll('body *')) {
    const rect = node.getBoundingClientRect();
    if (!Number.isFinite(rect.left) || !Number.isFinite(rect.right) || !Number.isFinite(rect.bottom)) continue;
    const css = getComputedStyle(node);
    const left = rect.left + window.scrollX;
    const right = rect.right + window.scrollX;
    const bottom = rect.bottom + window.scrollY;
    contentLeft = Math.min(contentLeft, left);
    if (right > contentRight) {
      contentRight = right;
      widestElement = {tag: node.tagName.toLowerCase(), width: rect.width, right};
    }
    contentBottom = Math.max(contentBottom, bottom);
    if (node.scrollWidth > node.clientWidth + 2 || node.scrollHeight > node.clientHeight + 2) {
      if (scrollContainers.length < 50) scrollContainers.push({
        tag: node.tagName.toLowerCase(),
        rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height},
        client_width: node.clientWidth,
        client_height: node.clientHeight,
        scroll_width: node.scrollWidth,
        scroll_height: node.scrollHeight,
        overflow_x: css.overflowX,
        overflow_y: css.overflowY,
        position: css.position
      });
    }
    if ((left < -2 || rect.right > window.innerWidth + 2) && outsideViewport.length < 50) {
      outsideViewport.push({
        tag: node.tagName.toLowerCase(), left, right,
        width: rect.width, position: css.position, overflow_x: css.overflowX
      });
    }
  }
  const documentWidth = Math.ceil(Math.max(root.scrollWidth, root.offsetWidth, root.clientWidth,
    bodyWidth, contentRight) - Math.min(0, contentLeft));
  const documentHeight = Math.ceil(Math.max(root.scrollHeight, root.offsetHeight, root.clientHeight,
    bodyHeight, contentBottom));
  return {
    document_width: documentWidth,
    document_height: documentHeight,
    content_left: Math.floor(contentLeft),
    content_right: Math.ceil(contentRight),
    root_client_width: root.clientWidth,
    root_client_height: root.clientHeight,
    root_scroll_width: root.scrollWidth,
    root_scroll_height: root.scrollHeight,
    body_scroll_width: body ? body.scrollWidth : 0,
    body_scroll_height: body ? body.scrollHeight : 0,
    page_overflow: {
      horizontal: root.scrollWidth > root.clientWidth + 2 || bodyWidth > window.innerWidth + 2,
      vertical: root.scrollHeight > root.clientHeight + 2 || bodyHeight > window.innerHeight + 2,
      root_overflow_x: rootStyle.overflowX,
      root_overflow_y: rootStyle.overflowY,
      body_overflow_x: bodyStyle ? bodyStyle.overflowX : null,
      body_overflow_y: bodyStyle ? bodyStyle.overflowY : null
    },
    widest_element: widestElement,
    scroll_containers: scrollContainers,
    outside_viewport_elements: outsideViewport
  };
}"""


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def sanitize_url(url: str) -> str:
    """Return a persistable URL with credentials, query and fragment removed.

    The caller may still use the original URL for navigation.  This function
    is deliberately only used for metadata and manifests; the full URL is
    represented there by its SHA-256 digest instead of its value.
    """
    if not isinstance(url, str) or not url:
        raise ValueError("URL must be a non-empty string")
    try:
        parts = urlsplit(url)
        hostname = parts.hostname
        if parts.scheme.lower() not in {"http", "https"} or not hostname:
            raise ValueError
        # Rebuild the authority from hostname/port so userinfo can never be
        # carried into the persisted value.  IPv6 literals need brackets.
        safe_host = hostname.lower()
        if ":" in safe_host and not safe_host.startswith("["):
            safe_host = f"[{safe_host}]"
        try:
            port = parts.port
        except ValueError as exc:
            raise ValueError("URL has an invalid port") from exc
        netloc = safe_host if port is None else f"{safe_host}:{port}"
        return urlunsplit((parts.scheme.lower(), netloc, parts.path or "/", "", ""))
    except (TypeError, ValueError) as exc:
        raise ValueError("URL must be an absolute HTTP(S) URL") from exc


def url_sha256(url: str) -> str:
    """Hash the exact URL supplied by the caller, before sanitization."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _validate_storage_state(storage_state: str | Path | None) -> Path | None:
    """Validate a Playwright storage-state file without exposing its path/content."""
    if storage_state is None:
        return None
    candidate = Path(storage_state)
    if not candidate.is_file():
        raise ValueError("storage-state file does not exist")
    try:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("storage-state file is not valid JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError("storage-state file must contain a JSON object")
    return candidate


def _normalize_document_metrics(raw: Mapping[str, Any], width: int, height: int, *,
                                initial: Mapping[str, Any] | None = None,
                                samples: list[Mapping[str, Any]] | None = None) -> dict[str, Any]:
    """Normalize measured page extents without deciding whether overflow is intentional."""
    if width <= 0 or height <= 0:
        raise ValueError("viewport dimensions must be positive")

    def dimension(source: Mapping[str, Any], key: str, floor: int) -> int:
        value = source.get(key, floor)
        try:
            return max(floor, int(round(float(value))))
        except (TypeError, ValueError):
            return floor

    document_width = dimension(raw, "document_width", width)
    document_height = dimension(raw, "document_height", height)
    raw_samples = list(samples or ([initial, raw] if initial is not None else [raw]))
    normalized_samples = [
        {
            "width": dimension(sample, "document_width", width),
            "height": dimension(sample, "document_height", height),
        }
        for sample in raw_samples
    ]
    initial_width = normalized_samples[0]["width"]
    initial_height = normalized_samples[0]["height"]
    tail = normalized_samples[-2:] if len(normalized_samples) > 1 else normalized_samples
    stable_after_wait = len(tail) == 2 and all(
        abs(tail[1][key] - tail[0][key]) <= 2 for key in ("width", "height")
    )
    return {
        "viewport": {"width": width, "height": height},
        "document": {"width": document_width, "height": document_height},
        "overflow": {
            "horizontal": document_width > width,
            "vertical": document_height > height,
            "horizontal_px": max(0, document_width - width),
            "vertical_px": max(0, document_height - height),
        },
        "stable_after_wait": stable_after_wait,
        "samples": normalized_samples,
        "initial_document": {"width": initial_width, "height": initial_height},
        "page_overflow": raw.get("page_overflow", {}),
        "scroll_containers": list(raw.get("scroll_containers", [])),
        "outside_viewport_elements": list(raw.get("outside_viewport_elements", [])),
        "content_left": raw.get("content_left", 0),
        "content_right": raw.get("content_right", document_width),
        "widest_element": raw.get("widest_element"),
    }


def _capture_metadata(url: str, width: int, height: int, *, screenshot: str, dom: str, styles: str,
                      http_status: int | None, full_page: bool, authenticated: bool,
                      document_metrics: Mapping[str, Any] | None = None,
                      screenshot_dimensions: Mapping[str, int] | None = None,
                      capture_mode: str | None = None,
                      frame_bounds: Mapping[str, int] | None = None) -> dict[str, Any]:
    """Build the persisted manifest without URL credentials or private paths."""
    metadata = {
        "captured_at": _utc(), "source_type": "url", "url": sanitize_url(url),
        "url_sha256": url_sha256(url),
        "viewport": {"width": width, "height": height, "device_scale_factor": 1},
        "http_status": http_status, "screenshot": screenshot, "dom": dom, "styles": styles,
        "playwright": True, "full_page": full_page,
        "capture_mode": capture_mode or ("full_page" if full_page else "viewport"),
        "authenticated": authenticated,
    }
    if document_metrics is not None:
        metadata["document_metrics"] = dict(document_metrics)
    if screenshot_dimensions is not None:
        metadata["screenshot_dimensions"] = dict(screenshot_dimensions)
    if frame_bounds is not None:
        metadata["frame_bounds"] = dict(frame_bounds)
    return metadata


async def capture_url(url: str, output_dir: str | Path, width: int, height: int, *, full_page: bool = False,
                      wait_ms: int = 500, storage_state: str | Path | None = None,
                      scroll_probes: int = 2,
                      frame_bounds: tuple[int, int] | None = None) -> dict[str, Any]:
    # Validate before launching a browser, while retaining the original URL
    # for the actual request (including its query string when needed by auth).
    sanitize_url(url)
    if not 0 <= scroll_probes <= 3:
        raise ValueError("scroll_probes must be between 0 and 3")
    if frame_bounds is not None:
        if full_page:
            raise ValueError("frame_bounds and full_page are mutually exclusive")
        if frame_bounds[0] < width or frame_bounds[1] < height:
            raise ValueError("frame_bounds cannot be smaller than the observation viewport")
    state_path = _validate_storage_state(storage_state)
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise RuntimeError("Playwright não está instalado; instale scripts/requirements.txt e o navegador Chromium") from exc
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)
    screenshot = directory / "source.png"
    dom_path = directory / "dom.html"
    styles_path = directory / "styles.json"
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context_kwargs: dict[str, Any] = {"viewport": {"width": width, "height": height}, "device_scale_factor": 1}
        if state_path is not None:
            context_kwargs["storage_state"] = str(state_path)
        context = await browser.new_context(**context_kwargs)
        page = await context.new_page()
        response = await page.goto(url, wait_until="networkidle")
        metric_samples = [await page.evaluate(MEASURE_DOCUMENT_JS)]
        if wait_ms > 1:
            first_wait = wait_ms // 2
            await page.wait_for_timeout(first_wait)
            metric_samples.append(await page.evaluate(MEASURE_DOCUMENT_JS))
            await page.wait_for_timeout(wait_ms - first_wait)
        elif wait_ms:
            await page.wait_for_timeout(wait_ms)
        metric_samples.append(await page.evaluate(MEASURE_DOCUMENT_JS))
        for _ in range(scroll_probes):
            await page.evaluate("() => window.scrollTo(0, document.documentElement.scrollHeight)")
            await page.wait_for_timeout(max(100, wait_ms))
            metric_samples.append(await page.evaluate(MEASURE_DOCUMENT_JS))
        if scroll_probes:
            await page.evaluate("() => window.scrollTo(0, 0)")
        final_metrics = metric_samples[-1]
        document_metrics = _normalize_document_metrics(final_metrics, width, height, samples=metric_samples)
        if frame_bounds is not None:
            session = await context.new_cdp_session(page)
            response_payload = await session.send(
                "Page.captureScreenshot",
                {
                    "format": "png",
                    "captureBeyondViewport": True,
                    "clip": {"x": 0, "y": 0, "width": frame_bounds[0], "height": frame_bounds[1], "scale": 1},
                },
            )
            screenshot.write_bytes(base64.b64decode(response_payload["data"]))
        else:
            await page.screenshot(path=str(screenshot), full_page=full_page)
        captured_image = read_png(str(screenshot))
        dom = await page.content()
        style_rows = await page.locator("*").evaluate_all(
            """nodes => nodes.slice(0, 2000).map((node, index) => {
              const rect = node.getBoundingClientRect();
              const css = getComputedStyle(node);
              return {index, tag: node.tagName.toLowerCase(), id: node.id || null,
                className: typeof node.className === 'string' ? node.className : null,
                text: (node.innerText || '').trim().slice(0, 200),
                rect: {x: rect.x, y: rect.y, width: rect.width, height: rect.height},
                styles: {display: css.display, position: css.position, color: css.color,
                  backgroundColor: css.backgroundColor, fontFamily: css.fontFamily,
                  fontSize: css.fontSize, fontWeight: css.fontWeight, lineHeight: css.lineHeight,
                  borderRadius: css.borderRadius, padding: css.padding, margin: css.margin,
                  overflowX: css.overflowX, overflowY: css.overflowY}
              };
            })"""
        )
        dom_path.write_text(dom, encoding="utf-8")
        styles_path.write_text(json.dumps(style_rows, ensure_ascii=False, indent=2), encoding="utf-8")
        metadata = _capture_metadata(url, width, height, screenshot=screenshot.name, dom=dom_path.name,
                                     styles=styles_path.name, http_status=response.status if response else None,
                                     full_page=full_page, authenticated=state_path is not None,
                                     document_metrics=document_metrics,
                                     screenshot_dimensions={"width": captured_image.width, "height": captured_image.height},
                                     capture_mode="frame_bounds" if frame_bounds is not None else None,
                                     frame_bounds={"width": frame_bounds[0], "height": frame_bounds[1]} if frame_bounds else None)
        (directory / "capture.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        await context.close()
        await browser.close()
    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Capture a URL/app source with Playwright")
    parser.add_argument("--url", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--viewport", default="1440x900")
    parser.add_argument("--full-page", action="store_true")
    parser.add_argument("--wait-ms", type=int, default=500)
    parser.add_argument("--scroll-probes", type=int, default=2, choices=range(0, 4))
    parser.add_argument("--frame-bounds", help="Approved frame bounds WxH; captures beyond the viewport with Chromium")
    parser.add_argument("--storage-state", help="Playwright storage-state JSON for private/authenticated sources")
    args = parser.parse_args(argv)
    width, height = (int(value) for value in args.viewport.lower().split("x", 1))
    frame_bounds = tuple(int(value) for value in args.frame_bounds.lower().split("x", 1)) if args.frame_bounds else None
    try:
        asyncio.run(capture_url(args.url, args.output, width, height, full_page=args.full_page, wait_ms=args.wait_ms,
                                storage_state=args.storage_state, scroll_probes=args.scroll_probes,
                                frame_bounds=frame_bounds))
    except (RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
