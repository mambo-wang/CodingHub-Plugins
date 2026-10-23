#!/usr/bin/env python3
"""Rasterize a screenshot/diagram HTML as a PNG element capture with Playwright."""

from __future__ import annotations

import argparse
import math
import pathlib
import sys

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

NETWORK_IDLE_TIMEOUT_MS = 15_000
FALLBACK_SETTLE_MS = 4_000


def scale_between_1_and_4(value: str) -> float:
    try:
        scale = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("scale must be a number") from exc
    if not math.isfinite(scale) or not 1 <= scale <= 4:
        raise argparse.ArgumentTypeError("scale must be between 1 and 4")
    return scale


def capture(
    src: pathlib.Path,
    out: pathlib.Path,
    selector: str,
    scale: float,
    width: int | None,
) -> None:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        try:
            page = browser.new_page(
                device_scale_factor=scale,
                viewport={"width": max(width or 1440, 1280), "height": 900},
            )
            page.goto(src.resolve().as_uri() + "?motion=static", wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=NETWORK_IDLE_TIMEOUT_MS)
            except PlaywrightTimeoutError:
                page.evaluate("window.stop()")
                page.wait_for_timeout(FALLBACK_SETTLE_MS)
                print(
                    "warning: a subrequest stalled - captured with fallback typography",
                    file=sys.stderr,
                )
            page.evaluate("document.fonts.ready")
            if width:
                page.evaluate(
                    "(px) => { document.querySelectorAll('.shot-card, .frame').forEach( "
                    "el => { el.style.setProperty('width', px + 'px', 'important'); "
                    "el.style.setProperty('max-width', 'none', 'important'); } ); }",
                    width,
                )
            target = page.locator(selector).first
            if target.count() == 0:
                raise RuntimeError(f"selector not found: {selector}")
            box = target.bounding_box()
            if box is None or box["width"] < 1 or box["height"] < 1:
                raise RuntimeError(f"selector {selector} has no visible box")
            target.screenshot(path=out)
            print(
                f"OK {out.name} {round(box['width'])}x{round(box['height'])} CSS px "
                f"@{scale}x  {out.stat().st_size:,} B"
            )
        finally:
            browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src", type=pathlib.Path, help="HTML input")
    parser.add_argument("out", type=pathlib.Path, help="PNG output")
    parser.add_argument("scale", nargs="?", type=scale_between_1_and_4, default=2)
    parser.add_argument(
        "--selector",
        default=".shot-card",
        help="CSS selector to capture (default .shot-card; use svg for diagrams)",
    )
    parser.add_argument("--width", type=int, help="force the card to this CSS width first")
    args = parser.parse_args()
    capture(args.src, args.out, args.selector, args.scale, args.width)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
