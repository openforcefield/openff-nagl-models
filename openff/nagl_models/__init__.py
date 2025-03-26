"""
OpenFF NAGL Models
Models used with NAGL
"""

from .openff_nagl_models import (
    get_nagl_model_dirs_paths,
    load_nagl_model_directory_entry_points,
    validate_nagl_model_path,
    list_available_nagl_models,
    get_models_by_type
)
from openff.nagl_models._dynamic_fetch import get_model

# Handle versioneer
from . import _version
__version__ = _version.get_versions()['version']

__all__ = (
    "get_nagl_model_dirs_paths",
    "load_nagl_model_directory_entry_points",
    "validate_nagl_model_path",
    "list_available_nagl_models",
    "get_models_by_type",
    "get_model",
)
