# OpenFF NAGL Models

This repository contains models trained and applied with
[OpenFF NAGL](https://docs.openforcefield.org/projects/nagl/en/latest/).

See the [Models](models/index.md) page for more information about the available models.

```{include} ../README.md
:start-after: <!-- models-start -->
:end-before: <!-- models-end -->
```

```{include} ../README.md
:start-after: <!-- usage-start -->
:end-before: <!-- usage-end -->
```

:::{toctree}
---
hidden: true
---

Overview <self>
models/index.md
CHANGELOG.md

:::



<!--
The autosummary directive renders to rST,
so we must use eval-rst here
-->
```{eval-rst}
.. raw:: html

    <div style="display: None">

.. autosummary::
   :recursive:
   :caption: API Reference
   :toctree: api/generated
   :nosignatures:

   openff.nagl_models

.. raw:: html

    </div>
```
