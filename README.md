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
```


## Versions
- `v0.0.1-alpha.1`: a pre-production model to use for experimentation. We do *not* recommend using this model to assign charges in scientific work.


#### Acknowledgements

Project based on the
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.0.
