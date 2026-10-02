# Chunkzero aqua registry

[aqua](https://aquaproj.github.io/) package definitions for Chunkzero command-line tools.

| Package                 | Platforms                                    | Status                       |
| ----------------------- | -------------------------------------------- | ---------------------------- |
| `chunkzero/maven-r2`    | Linux, macOS, Windows; amd64 and arm64       | Available at `v0.1.0`        |
| `chunkzero/rpp`         | Linux, macOS; amd64 and arm64; Windows amd64 | Stable and prerelease builds |
| `chunkzero/rpp-nightly` | Linux, macOS; amd64 and arm64; Windows amd64 | Nightly builds only          |

`chunk` can be added once it publishes CLI binaries with a defined asset format. Window currently ships an rpp plugin rather than a standalone CLI.

## Use

Add this registry to your project's `aqua.yaml`:

```yaml
checksum:
  enabled: true
  require_checksum: true
registries:
  - name: chunkzero-github
    type: github_content
    repo_owner: chunkzero
    repo_name: aqua-registry
    ref: v0.1.3
    path: registry.yaml
packages:
  - name: chunkzero/maven-r2@v0.1.0
    registry: chunkzero-github
  - name: chunkzero/rpp-nightly@v0.1.0-nightly.20261002.ge7fe09d0aa17
    registry: chunkzero-github
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
    registry: chunkzero-github
```

Keep the asset layout identical across stable, beta, and nightly releases. For rpp, the example beta needs `rpp-0.2.0-beta.1-linux-x64.tar.gz` and its `.sha256` file. The archive contains the matching top-level directory, the `rpp` executable, and its bundled toolchain.

Recommended publishing conventions:

- Stable: `v0.2.0`, published as a normal GitHub release.
- Beta: `v0.2.0-beta.1`, published as a prerelease.
- Nightly: `v0.2.0-nightly.20261001.ga1b2c3d4e5f6`, published as a prerelease with a unique date and commit suffix.
- Schedule nightlies daily, publish only when `main` has changed since the last successful nightly, and support manual dispatch.
- Reuse release packaging and verification; publish checksums alongside every binary.
- Use the full nightly version in the binary's version output and versioned archive names.

Avoid overwriting a rolling `nightly` tag or its assets: cached versions and committed checksums should remain reproducible. Use exact versions or a committed mise lockfile to keep installs reproducible.

For mise, use the nightly-only entry to select the newest nightly across version series:

```toml
[settings]
aqua.registries = ["https://raw.githubusercontent.com/chunkzero/aqua-registry/v0.1.3/registry.yaml"]

[tools]
"aqua:chunkzero/rpp-nightly" = { version = "latest", prerelease = true, minimum_release_age = "0s" }
```

Both RPP entries install the `rpp` executable from the same release assets. The
nightly entry filters out stable, alpha, beta, and release-candidate versions.
`prerelease = true` enables GitHub prereleases; `minimum_release_age = "0s"`
allows freshly published builds regardless of the machine's global setting.
Mise selects the native archive from the registry platform definitions.
Run `mise lock --bump aqua:chunkzero/rpp-nightly` to select a
new nightly, then commit `mise.lock`. Regular installs use the locked version.

Nightly workflows live in the tool repositories; this repository only describes installation.

## Maintain

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
npx --yes prettier@3.6.2 --check .
```

CI validates all three aqua configuration files against the pinned upstream schemas, installs the published `maven-r2` and nightly `rpp` versions on Linux x64/arm64, macOS x64/arm64, and Windows x64 with checksum verification, and type-checks a plugin with RPP’s bundled TypeScript compiler.

Nightly publishing is tracked in [rpp #76](https://github.com/chunkzero/rpp/issues/76), [chunk #317](https://github.com/chunkzero/chunk/issues/317), [maven-r2 #12](https://github.com/chunkzero/maven-r2/issues/12), and [Window #3](https://github.com/chunkzero/window/issues/3).

For new packages, inspect the published archive layout, add a definition with explicit platforms and checksum metadata, and add a pinned version to `aqua.yaml`. Tag registry changes with a new version so consumers can update their registry pin.
