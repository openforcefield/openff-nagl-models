"""
OpenFF NAGL Models
Models used with NAGL
"""

from importlib.metadata import version

from .openff_nagl_models import (
    get_nagl_model_dirs_paths,
    load_nagl_model_directory_entry_points,
    validate_nagl_model_path,
    list_available_nagl_models,
    get_models_by_type
)

__version__ = version("openff.toolkit")
