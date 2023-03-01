"""
This module only contains the function that will be the entry point that
will be used to find the model files.
"""
import os
from pkg_resources import resource_filename
from typing import Optional, Union, List


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
    return [resource_filename('openff.nagl_models', 'models')]


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
        ['openff-gnn-am1bcc-0.0.1-alpha.1.pt']

    """
    import glob
    model_paths = load_nagl_model_directory_entry_points()
    model_files = []
    for path in model_paths:
        model_files.extend(glob.glob(os.path.join(path, "*.pt")))
    return sorted([os.path.basename(f) for f in model_files])
