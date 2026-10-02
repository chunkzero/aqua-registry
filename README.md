# Chunkzero aqua registry

[aqua](https://aquaproj.github.io/) package definitions for Chunkzero command-line tools.

| Package              | Platforms                              | Status                                |
| -------------------- | -------------------------------------- | ------------------------------------- |
| `chunkzero/maven-r2` | Linux, macOS, Windows; amd64 and arm64 | Available at `v0.1.0`                 |
| `chunkzero/rpp`      | Linux amd64                            | Prepared for the first binary release |

`chunk` can be added once it publishes CLI binaries with a defined asset format. Window currently ships an rpp plugin rather than a standalone CLI.

## Use

Add this registry to your project's `aqua.yaml`:

```yaml
checksum:
  enabled: true
  require_checksum: true
registries:
  - name: chunkzero
    type: github_content
    repo_owner: chunkzero
    repo_name: aqua-registry
    ref: v0.1.0
    path: registry.yaml
packages:
  - name: chunkzero/maven-r2@v0.1.0
    registry: chunkzero
```

Pin the registry to a release tag or commit SHA. Aqua treats refs as immutable, so do not use `main` or a moving tag.

Custom registries need an [aqua policy](https://aquaproj.github.io/docs/guides/policy-as-code/). Copy `aqua-policy.yaml` into your project, review it, then run:

```sh
export AQUA_POLICY_CONFIG="$PWD/aqua-policy.yaml"
aqua policy allow "$AQUA_POLICY_CONFIG"
aqua update-checksum
aqua install
aqua exec -- maven-r2 --version
```

For local development, this repository's `aqua.yaml` uses the local registry and only includes published packages.

## Beta and nightly releases

Aqua installs a pinned GitHub prerelease just like a stable release. Build and publish the binaries in each tool's repository; aqua downloads them. For example, after publishing an rpp beta:

```yaml
packages:
  - name: chunkzero/rpp@v0.2.0-beta.1
    registry: chunkzero
```

Keep the asset layout identical across stable, beta, and nightly releases. For rpp, the example beta needs `rpp-0.2.0-beta.1-linux-x64.tar.gz` and its `.sha256` file. The archive contains the matching top-level directory, the `rpp` executable, and its bundled toolchain.

Recommended publishing conventions:

- Stable: `v0.2.0`, published as a normal GitHub release.
- Beta: `v0.2.0-beta.1`, published as a prerelease.
- Nightly: `v0.2.0-nightly.20261001.a1b2c3d`, published as a prerelease with a unique date and commit suffix.
- Schedule nightlies daily, publish only when `main` has changed since the last successful nightly, and support manual dispatch.
- Reuse release packaging and verification; publish checksums alongside every binary.
- Use the full nightly version in the binary's version output and versioned archive names.

Avoid overwriting a rolling `nightly` tag or its assets: cached versions and committed checksums should remain reproducible. Pin beta/nightly versions explicitly rather than relying on automatic latest-version selection.

Nightly workflows live in the tool repositories; this repository only describes installation.

## Maintain

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
npx --yes prettier@3.6.2 --check .
```

CI validates all three aqua configuration files against the pinned upstream schemas and installs the published `maven-r2` version with checksum verification. Unreleased package definitions receive schema validation until releases are available.

Nightly publishing is tracked in [rpp #76](https://github.com/chunkzero/rpp/issues/76), [chunk #317](https://github.com/chunkzero/chunk/issues/317), [maven-r2 #12](https://github.com/chunkzero/maven-r2/issues/12), and [Window #3](https://github.com/chunkzero/window/issues/3).

For new packages, inspect the published archive layout, add a definition with explicit platforms and checksum metadata, and add a pinned version to `aqua.yaml`. Tag registry changes with a new version so consumers can update their registry pin.
