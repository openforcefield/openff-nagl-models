# Release process

## Add the new model(s)' hashes

If no models (`.pt` files) are added in the release, skip this step.

The constant `openff.nagl_models._dynamic_fetch.KNOWN_HASHES` needs to be updated for each added model. **Skipping this
may cause users to be unable to load new models.**

Add the file name and its SHA256 hash as a key-val pair to the dictionary. It was originally created by running a
`sha256` executable over all existing models:

```console
$ sha256 \
    openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.0.1-alpha.1.pt \
    openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.1.pt \
    openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.2.pt \
    openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.3.pt
SHA256 (openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.0.1-alpha.1.pt) = a0fcf53feab7182ea53aecec994bb6dba0833b0468a59392551c817cb7acb51a
SHA256 (openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.1.pt) = ee2dd8123f4b231d5de26bd63f47be94332a99d58095945a68e81b2efdcdfceb
SHA256 (openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.2.pt) = 648b2636580f49f882591aedcc5c404a9cbbecb9ca1e082d98ccd71301db917f
SHA256 (openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.3.pt) = 144ed56e46c5b3ad80157b342c8c0f8f7340e4d382a678e30dd300c811646bd0
```

These were copied into the Python code like so:

```python
KNOWN_HASHES = {
    "openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.0.1-alpha.1.pt": "a0fcf53feab7182ea53aecec994bb6dba0833b0468a59392551c817cb7acb51a",
    "openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.1.pt": "ee2dd8123f4b231d5de26bd63f47be94332a99d58095945a68e81b2efdcdfceb",
    "openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.2.pt": "648b2636580f49f882591aedcc5c404a9cbbecb9ca1e082d98ccd71301db917f",
    "openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.3.pt": "144ed56e46c5b3ad80157b342c8c0f8f7340e4d382a678e30dd300c811646bd0",
}
```

All released models should be added and follow this pattern; run `sha256` directly on the model(s) being added and
append to the `KNOWN_HASHES` dictionary.

Submit this change as a PR which **must be merged before making the release.**

## Make the release on GitHub

Use [CalVer](https://calver.org/), `YYYY.MM.MINOR` variant:
    * `YYYY` is the current year
    * `MM` is the current month, including a leading zero.
    * `MINOR` begins at 0 and increments for every release made in a given month.

Include release notes at your discretion.

## Attach the new model(s) to the GitHub Release

Do this via the web UI.

## Make the pip package and upload to pypi

```
python -m pip install pipx twine
git checkout v0.4.0
python -m pipx run build --wheel --sdist
python3 -m twine upload --repository pypi dist/openff_nagl_models-0.4.0*
```

## Make the `conda-forge` packages

Eg. [this pr](https://github.com/conda-forge/openff-nagl-models-feedstock/pull/14)
You can generate the new hash using the `dist/` folder from the last step, eg `openssl sha256 dist/openff_nagl_models-0.4.0.tar.gz`
