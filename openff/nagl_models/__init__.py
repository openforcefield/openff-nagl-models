"""
OpenFF NAGL Models
Models used with NAGL
"""

from importlib.metadata import version

from openff.nagl_models.openff_nagl_models import (
    get_models_by_type,
    get_nagl_model_dirs_paths,
    list_available_nagl_models,
    load_nagl_model_directory_entry_points,
    validate_nagl_model_path,
)

__all__ = (
    "get_model",
    "get_models_by_type",
    "get_nagl_model_dirs_paths",
    "list_available_nagl_models",
    "load_nagl_model_directory_entry_points",
    "validate_nagl_model_path",
)

__version__ = version("openff.nagl_models")
from openff.nagl_models._dynamic_fetch import get_model
