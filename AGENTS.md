# Chunkzero aqua registry

Reusable aqua package definitions for Chunkzero CLIs.

## Guidelines

- Keep package definitions in registry.yaml and match actual release assets.
- Preserve bundled runtime files when exposing executables from archives.
- Declare supported platforms explicitly and verify published SHA-256 checksums.
- Do not edit AGENTS.md or CLAUDE.md unless explicitly asked.
- Use Conventional Commits and avoid unrelated changes.

## Tooling

- Install development dependencies with `python -m pip install -r requirements-dev.txt` in a virtual environment.
- Run `python scripts/validate.py` to validate the registry, consumer config, and policy.
- Use two-space indentation in YAML.
- With aqua installed, run `AQUA_POLICY_CONFIG="$PWD/aqua-policy.yaml" aqua install` to check published packages.
- Add packages to aqua.yaml only after an installable release exists.

## Glossary

- Registry: reusable package metadata describing release assets and executable paths.
- Consumer config: aqua.yaml, which pins package versions for installation checks.
- Policy: aqua's allowlist for custom registries.
