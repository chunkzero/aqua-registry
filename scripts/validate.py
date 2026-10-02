#!/usr/bin/env python3
"""Validate configuration against the schemas shipped with the pinned aqua version."""

import json
from pathlib import Path
from urllib.request import urlopen

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = "https://raw.githubusercontent.com/aquaproj/aqua/v2.63.0/json-schema"

for filename, schema_name in (
    ("registry.yaml", "registry.json"),
    ("aqua.yaml", "aqua-yaml.json"),
    ("aqua-policy.yaml", "policy.json"),
):
    with urlopen(f"{SCHEMAS}/{schema_name}", timeout=30) as response:
        schema = json.load(response)
    document = yaml.safe_load((ROOT / filename).read_text())
    jsonschema.validate(document, schema)
    print(f"Validated {filename}")
