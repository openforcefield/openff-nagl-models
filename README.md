# Open NAGL Models

| **Latest release** | [![Last release tag](https://img.shields.io/github/release-pre/openforcefield/openff-nagl-models.svg)](https://github.com/openforcefield/openff-nagl-models/releases) ![GitHub commits since latest release (by date) for a branch](https://img.shields.io/github/commits-since/openforcefield/openff-nagl-models/latest)  [![Documentation Status](https://readthedocs.org/projects/openff-nagl-models/badge/?version=latest)](https://openff-nagl-models.readthedocs.io/en/latest/)                                                                                                        |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Status**         | [![GH Actions Status](https://github.com/openforcefield/openff-nagl-models/actions/workflows/CI.yml/badge.svg)](https://github.com/openforcefield/openff-nagl-models/actions?query=branch%3Amain+workflow%3ACI) |

                                                                          

This repository contains NAGL models released by the [Open Force Field Initiative](https://openforcefield.org). They are intended to be used by [OpenFF NAGL](https://github.com/openforcefield/openff-nagl).

## Use
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

## Versions
- `v0.0.1-alpha.1`: a pre-production model to use for experimentation. We do *not* recommend using this model to assign charges in scientific work.
- `v0.1.0-rc1`: a pre-production model to use to assign AM1-BCC partial charges.


#### Acknowledgements

Project based on the
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.0.
