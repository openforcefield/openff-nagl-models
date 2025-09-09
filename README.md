# OpenFF NAGL Models

| **Latest release** | [![Last release tag](https://img.shields.io/github/release-pre/openforcefield/openff-nagl-models.svg)](https://github.com/openforcefield/openff-nagl-models/releases) ![GitHub commits since latest release (by date) for a branch](https://img.shields.io/github/commits-since/openforcefield/openff-nagl-models/latest)  [![Documentation Status](https://readthedocs.org/projects/openff-nagl-models/badge/?version=latest)](https://openff-nagl-models.readthedocs.io/en/latest/)                                                                                                        |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**         | [![GH Actions Status](https://github.com/openforcefield/openff-nagl-models/actions/workflows/CI.yml/badge.svg)](https://github.com/openforcefield/openff-nagl-models/actions?query=branch%3Amain+workflow%3ACI) |
| **Community**      | [![License: CC-BY 4.0](https://img.shields.io/badge/license-CC--BY--NC--SA--4.0-yellow)](https://creativecommons.org/licenses/by/4.0/deed.en) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13119685.svg)](https://doi.org/10.5281/zenodo.13119685) |

This repository contains NAGL models released by the [Open Force Field Initiative](https://openforcefield.org). They are intended to be used by [OpenFF NAGL](https://github.com/openforcefield/openff-nagl).

## Models

| Model name | Introduced in `openff-nagl-models` version | Release state | Further notes |
|---|---|---|---|
| `openff-gnn-am1bcc-1.0.0.pt` | [v2025.09.0](https://github.com/openforcefield/openff-nagl-models/releases/tag/v2025.09.0) | Production | [Link](docs/models/openff-gnn-am1bcc-1.0.0/index.md)
| `openff-gnn-am1bcc-0.1.0-rc.3.pt` | [v0.3.0](https://github.com/openforcefield/openff-nagl-models/releases/tag/v0.3.0) | pre-production | [Link](docs/models/openff-gnn-am1bcc-0.1.0-rc3/index.md)
| `openff-gnn-am1bcc-0.1.0-rc.1.pt` | [v0.2.0](https://github.com/openforcefield/openff-nagl-models/releases/tag/v0.2.0) | pre-production | [Link](docs/models/openff-gnn-am1bcc-0.1.0-rc2/index.md)
| `openff-gnn-am1bcc-0.1.0-rc.1.pt` | [v0.1.0](https://github.com/openforcefield/openff-nagl-models/releases/tag/v0.1.0) | pre-production | [Link](docs/models/openff-gnn-am1bcc-0.1.0-rc1/index.md)
| `openff-gnn-am1bcc-0.0.1-alpha.1.pt` $^1$ | [v0.0.1](https://github.com/openforcefield/openff-nagl-models/releases/tag/v0.0.1) | pre-production/experimental $^1$ | [Link](docs/models/openff-gnn-am1bcc-0.0.1-alpha.1/index.md) |

$^1$ We do *not* recommend using this model to assign charges in scientific work.

## Usage

Installing this package exposes an entry point that makes it easy to access models installed in this package.

A convenience function is provided to wrap this for you:

```python
>>> from openff.nagl_models import load_nagl_model_directory_entry_points
>>> load_nagl_model_directory_entry_points()
[PosixPath('/home/.../openff-nagl-models/openff/nagl_models/models/am1bcc')]
```

You can also list all available models **from all entry points**:

```python
>>> from openff.nagl_models import list_available_nagl_models
>>> list_available_nagl_models()
[PosixPath('/home/.../openff-nagl-models/openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.0.1-alpha.1.pt'), PosixPath('/home/.../openff-nagl-models/openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.1.pt')]
```

Or validate if a model name is found in the local directory, or an entry point directory:

```python
>>> from openff.nagl_models import validate_nagl_model_path
>>> validate_nagl_model_path("openff-gnn-am1bcc-0.0.1-alpha.1.pt")
PosixPath('/home/.../openff-nagl-models/openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.0.1-alpha.1.pt')
```

Finally, if you want to find all models for a particular type, use `get_models_by type`.
These will come sorted according to semantic versioning, where the latest release is last:

```python
>>> from openff.nagl_models import get_models_by_type
>>> get_models_by_type("am1bcc")
[PosixPath('/home/.../openff-nagl-models/openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.0.1-alpha.1.pt'), PosixPath('/home/.../openff-nagl-models/openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.1.pt')]
```

#### Acknowledgements

Project based on the
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.0.
