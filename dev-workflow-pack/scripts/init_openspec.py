#!/usr/bin/env python3
"""Copy the plugin-shipped openspec/ directory into a project root.

The plugin bundles an OpenSpec directory (config.yaml, specs/, schemas/,
changes/) for the OpenSpec workflow. CodeBuddy loads plugin components from
the install directory, so this payload never reaches a project by itself —
this script is the explicit entry point used by the /init-openspec command.

Target resolution (first hit wins):
  1. --target <dir>
  2. $CODEBUDDY_PROJECT_DIR (or $CLAUDE_PROJECT_DIR)
  3. current working directory

Plugin root resolution:
  1. $CODEBUDDY_PLUGIN_ROOT (or $CLAUDE_PLUGIN_ROOT)
  2. this script's location: <plugin>/scripts/init_openspec.py

Idempotent by default: if <target>/openspec already exists, the script skips
(exit 0, "already initialized"). Use --force to merge: existing files are
overwritten by the shipped copies, files only present in the target are kept.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path


def _resolve_plugin_root() -> Path | None:
    for var in ("CODEBUDDY_PLUGIN_ROOT", "CLAUDE_PLUGIN_ROOT"):
        val = os.environ.get(var, "").strip()
        if val:
            p = Path(val)
            if (p / "openspec").is_dir():
                return p
    # Fallback: <plugin>/scripts/init_openspec.py
    here = Path(__file__).resolve()
    if (here.parents[1] / "openspec").is_dir():
        return here.parents[1]
    return None


def _resolve_target(args) -> Path:
    if args.target:
        return Path(args.target).expanduser().resolve()
    for var in ("CODEBUDDY_PROJECT_DIR", "CLAUDE_PROJECT_DIR"):
        val = os.environ.get(var, "").strip()
        if val and os.path.isdir(val):
            return Path(val)
    return Path.cwd().resolve()


def _merge_copy(src: Path, dst: Path) -> int:
    """Copy src tree into dst tree, overwriting same-name files.

    Returns the number of files copied. Files only present in dst are kept.
    """
    copied = 0
    for s in src.rglob("*"):
        if not s.is_file():
            continue
        rel = s.relative_to(src)
        d = dst / rel
        if not d.parent.is_dir():
            d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(s, d)
        copied += 1
    return copied


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize the plugin-shipped openspec/ into a project root."
    )
    parser.add_argument("--target", help="target project root (default: env/current dir)")
    parser.add_argument(
        "--force",
        action="store_true",
        help="merge over an existing openspec/ (overwrite same-name files)",
    )
    args = parser.parse_args()

    plugin_root = _resolve_plugin_root()
    if plugin_root is None:
        print("[init-openspec] plugin openspec/ directory not found", file=sys.stderr)
        return 1

    src = plugin_root / "openspec"
    target = _resolve_target(args)
    dst = target / "openspec"

    if dst.is_dir():
        if not args.force:
            print(f"[init-openspec] {dst} already exists — nothing to do (use --force to merge)")
            return 0
        copied = _merge_copy(src, dst)
        print(f"[init-openspec] merged {copied} files into {dst}")
        return 0

    try:
        shutil.copytree(src, dst)
    except OSError as e:  # noqa: BLE001
        print(f"[init-openspec] failed: {e}", file=sys.stderr)
        return 1

    print(f"[init-openspec] initialized OpenSpec directory at {dst}")
    print("[init-openspec] you can now use openspec-new-change / propose / apply / verify / archive")
    return 0


if __name__ == "__main__":
    sys.exit(main())
