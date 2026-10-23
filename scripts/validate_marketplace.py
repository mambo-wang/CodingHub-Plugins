#!/usr/bin/env python3
"""Validate marketplace.json against actual plugin directories.

Checks:
1. Every index entry's path exists and is a directory.
2. Each path has .codebuddy-plugin/plugin.json (client manifest).
3. Manifest name/version match the index entry.
4. name is kebab-case, version is semver.
5. No commands/skills fields declared in manifests.
6. Every top-level dir with plugin.json is listed in the index.

Exit 0 = OK, 1 = validation failure.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "marketplace.json")

KEBAB = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(-[a-zA-Z0-9]+)?$")

errors = []

with open(INDEX, encoding="utf-8") as f:
    index = json.load(f)

indexed = set()
for entry in index.get("plugins", []):
    name = entry.get("name", "")
    version = entry.get("version", "")
    path = entry.get("path", "")

    if not KEBAB.match(name):
        errors.append(f"{name}: name not kebab-case")
    if not SEMVER.match(version):
        errors.append(f"{name}: version '{version}' not semver")

    pdir = os.path.normpath(os.path.join(ROOT, path))
    if not os.path.isdir(pdir):
        errors.append(f"{name}: path '{path}' not a directory")
        continue
    indexed.add(os.path.basename(pdir))

    manifest = os.path.join(pdir, ".codebuddy-plugin", "plugin.json")
    if not os.path.isfile(manifest):
        errors.append(f"{name}: missing .codebuddy-plugin/plugin.json")
        continue

    with open(manifest, encoding="utf-8") as f:
        m = json.load(f)

    if m.get("name") != name:
        errors.append(f"{name}: manifest name '{m.get('name')}' != index name")
    if m.get("version") != version:
        errors.append(f"{name}: manifest version '{m.get('version')}' != index version '{version}'")
    for field in ("commands", "skills"):
        if field in m:
            errors.append(f"{name}: manifest declares forbidden field '{field}'")

# reverse check: dirs with plugin.json but not indexed
for d in sorted(os.listdir(ROOT)):
    dpath = os.path.join(ROOT, d)
    if not os.path.isdir(dpath) or d.startswith("."):
        continue
    if os.path.isfile(os.path.join(dpath, "plugin.json")) and d not in indexed:
        errors.append(f"{d}: has plugin.json but missing from marketplace.json index")

if errors:
    print("VALIDATION FAILED:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print(f"OK: {len(indexed)} plugins validated")
