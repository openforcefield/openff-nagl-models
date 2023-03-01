# Open NAGL Models

[![Build Status](https://github.com/openforcefield/openff-nagl-models/workflows/CI/badge.svg)](https://github.com/openforcefield/openff-nagl-models/actions?query=branch%main+workflow%3ACI)


This repository contains NAGL models released by the [Open Force Field Initiative](https://openforcefield.org). They are intended to be used by [OpenFF NAGL](https://github.com/openforcefield/openff-nagl).

## Use
Installing this package exposes an entry point that makes it easy to access models installed in this package:

```python
>>> from pkg_resources import iter_entry_points
>>> for entry_point in iter_entry_points(group='openforcefield.nagl_model_directory'):
...     paths = entry_point.load()()
...     print(paths)
...
['/home/.../openff-nagl-models/openff/nagl_models/models']
```

A convenience function is provided to wrap this for you:

```python
>>> from openff.nagl_models import load_nagl_model_directory_entry_points
>>> load_nagl_model_directory_entry_points()
['/home/.../openff-nagl-models/openff/nagl_models/models']
```

You can also list all available models **from all entry points**:

```python
>>> from openff.nagl_models import list_available_nagl_models
>>> list_available_nagl_models()
['openff-gnn-am1bcc-0.0.1-alpha.1.pt']
```

Or validate if a model name is found in the local directory, or an entry point directory:

```python
>>> from openff.nagl_models import validate_nagl_model_path
>>> validate_nagl_model_path("openff-gnn-am1bcc-0.0.1-alpha.1.pt")
'/home/.../openff-nagl-models/openff/nagl_models/models/openff-gnn-am1bcc-0.0.1-alpha.1.pt'
```

## Versions
- `v0.0.1-alpha.1`: a pre-production model to use for experimentation. We do *not* recommend using this model to assign charges in scientific work.


#### Acknowledgements

Project based on the
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.0.
