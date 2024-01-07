"""
This module only contains the function that will be the entry point that
will be used to find the model files.
"""
import glob
import os
import pathlib
from pkg_resources import resource_filename
from typing import Optional, Union, List
import warnings


def get_nagl_model_dirs_paths() -> List[str]:
    """
    Return the paths to the directories including the NAGL model files.

    This function is set as an entry point in setup.py. It will be called
    by OpenFF NAGL when discovering the installed folders
    including NAGL model files.

    Returns
    -------
    dir_paths : List[str]
        The list of directory paths containing the NAGL model files.
    """
    model_types = ["am1bcc"]
    return [
        resource_filename("openff.nagl_models", f"models/{model_type}")
        for model_type in model_types
    ]


def load_nagl_model_directory_entry_points() -> List[str]:
    """
    Load the entry points for the NAGL model directories.

    Returns
    -------
    List[str]
        The list of directory paths containing the NAGL model files.
    """
    from pkg_resources import iter_entry_points

    dir_paths = []
    for entry_point in iter_entry_points(group='openforcefield.nagl_model_directory'):
        dir_paths.extend(entry_point.load()())

    return dir_paths


def search_file_path(
    file_name: str,
    search_paths: Optional[Union[str, List[str]]] = None,
) -> Optional[str]:
    """
    Search for a file in a list of paths.

    Parameters
    ----------
    file_name : str
        The name of the file to search for.
    search_paths : Optional[Union[str, List[str]]], optional
        The paths to search for the file, by default None

    Returns
    -------
    Optional[str]
        The path to the file if it was found, otherwise None.
    """
    if search_paths is None:
        search_paths = []

    if isinstance(search_paths, str):
        search_paths = [search_paths]

    search_paths.insert(0, ".")

    for path in search_paths:
        file_path = os.path.join(path, file_name)
        if os.path.exists(file_path):
            return os.path.abspath(file_path)

    return None


def validate_nagl_model_path(model: str) -> str:
    """
    Validate and return the absolute path to a NAGL model file.

    Parameters
    ----------
    model : str
        The name or path of the model file to search for.
        This function searches for model files either in the
        current working directory or in the directories
        found in the ``openforcefield.nagl_model_directory`` entry point.

    Returns
    -------
    str
        The absolute path to the model file.

    Raises
    ------
    FileNotFoundError
        If the model file could not be found.

    Examples
    --------

    Loading a file from the installed openff_nagl_models package::

        >>> from openff.nagl_models import validate_nagl_model_path
        >>> validate_nagl_model_path("openff-gnn-am1bcc-0.0.1-alpha.1.pt")
        '/home/.../openff-nagl-models/openff/nagl_models/models/openff-gnn-am1bcc-0.0.1-alpha.1.pt'

    Loading a file from the current working directory::

        >>> from openff.nagl_models import validate_nagl_model_path
        >>> validate_nagl_model_path("my-local-gnn.pt")
        '/home/.../my-local-gnn.pt'

    """
    model_paths = load_nagl_model_directory_entry_points()
    full_path = search_file_path(model, model_paths)
    if full_path is None:
        raise FileNotFoundError(f"Could not find {model}")
    return full_path


def list_available_nagl_models() -> List[str]:
    """
    List the available NAGL models.

    Returns
    -------
    List[str]
        The list of available NAGL models.

    Examples
    --------
    ::

        >>> from openff.nagl_models import list_available_nagl_models
        >>> list_available_nagl_models()
        ['/Users/lily/pydev/openff-nagl-models/openff/nagl_models/models/openff-gnn-am1bcc-0.0.1-alpha.1.pt']

    """
    model_paths = load_nagl_model_directory_entry_points()
    model_files = []
    for path in model_paths:
        model_files.extend(glob.glob(os.path.join(path, "*.pt")))
    return sorted([os.path.abspath(f) for f in model_files])


def get_models_by_type(
    model_type: str,
    production_only: bool = False,
) -> list[pathlib.Path]:
    """
    Get all models of a given type released by OpenFF. This will not
    search for custom models that are not included in the openff-nagl-models
    package. Results will be sorted by version number, with the latest
    version last.

    Parameters
    ----------
    model_type : str
        The type of model to search for.
    production_only : bool, optional
        Whether to only search for production models, by default False.

    Returns
    -------
    list[pathlib.Path]
        The paths to the model files. Results are sorted from earliest
        to latest version.

    Raises
    ------
    ValueError
        If the model type is not found.

    Examples
    --------

    Getting the latest pre-release model for am1bcc::
    
        >>> from openff.nagl_models.openff_nagl_models import get_models_by_type
        >>> get_models_by_type(model_type="am1bcc")
        [PosixPath('/.../openff-nagl-models/openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.0.1-alpha.1.pt'),
        PosixPath('/.../openff-nagl-models/openff/nagl_models/models/am1bcc/openff-gnn-am1bcc-0.1.0-rc.1.pt')]
    
    """
    from packaging.version import Version

    base_dir = resource_filename("openff.nagl_models", f"models/{model_type}")
    if not os.path.isdir(base_dir):
        raise ValueError(
            f"Model type {model_type} not found in openff-nagl-models. "
            "If you are using a custom model, "
            "please manually specify the path to the model file."
        )
    
    model_files = pathlib.Path(base_dir).glob("*.pt")
    
    # assume everything follows the openff-gnn-<model_type>-<version>.pt format
    n_name = len(f"openff-gnn-{model_type}-")
    versions_to_paths = {
        Version(f.stem[n_name:]): f for f in model_files
    }
    versions = sorted(versions_to_paths.keys())
    if production_only:
        versions = [v for v in versions if not v.is_prerelease]
    return [versions_to_paths[v] for v in versions]
