"""Playwright source acquisition with a provenance manifest."""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit


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


def _capture_metadata(url: str, width: int, height: int, *, screenshot: str, dom: str, styles: str,
                      http_status: int | None, full_page: bool, authenticated: bool) -> dict[str, Any]:
    """Build the persisted manifest without URL credentials or private paths."""
    return {
        "captured_at": _utc(), "source_type": "url", "url": sanitize_url(url),
        "url_sha256": url_sha256(url),
        "viewport": {"width": width, "height": height, "device_scale_factor": 1},
        "http_status": http_status, "screenshot": screenshot, "dom": dom, "styles": styles,
        "playwright": True, "full_page": full_page, "authenticated": authenticated,
    }


async def capture_url(url: str, output_dir: str | Path, width: int, height: int, *, full_page: bool = False,
                      wait_ms: int = 500, storage_state: str | Path | None = None) -> dict[str, Any]:
    # Validate before launching a browser, while retaining the original URL
    # for the actual request (including its query string when needed by auth).
    sanitize_url(url)
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
        if wait_ms:
            await page.wait_for_timeout(wait_ms)
        await page.screenshot(path=str(screenshot), full_page=full_page)
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
                  borderRadius: css.borderRadius, padding: css.padding, margin: css.margin}
              };
            })"""
        )
        dom_path.write_text(dom, encoding="utf-8")
        styles_path.write_text(json.dumps(style_rows, ensure_ascii=False, indent=2), encoding="utf-8")
        metadata = _capture_metadata(url, width, height, screenshot=screenshot.name, dom=dom_path.name,
                                     styles=styles_path.name, http_status=response.status if response else None,
                                     full_page=full_page, authenticated=state_path is not None)
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
    parser.add_argument("--storage-state", help="Playwright storage-state JSON for private/authenticated sources")
    args = parser.parse_args(argv)
    width, height = (int(value) for value in args.viewport.lower().split("x", 1))
    try:
        asyncio.run(capture_url(args.url, args.output, width, height, full_page=args.full_page, wait_ms=args.wait_ms,
                                storage_state=args.storage_state))
    except (RuntimeError, ValueError) as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
