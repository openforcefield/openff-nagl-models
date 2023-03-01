"""
Unit and regression test for the openff_nagl_models package.
"""

import glob
import os
from pkg_resources import resource_filename


import pytest
from openff.nagl_models import validate_nagl_model_path, list_available_nagl_models


def find_model_files():
    pattern = resource_filename('openff.nagl_models', 'models/*.pt')
    filenames = sorted([os.path.basename(path) for path in glob.glob(pattern)])
    assert len(filenames) > 0
    return filenames


@pytest.mark.parametrize("model_name", find_model_files())
def test_validate_nagl_model_path(model_name):
    """Test that we can find files."""
    model_path = validate_nagl_model_path(model_name)
    assert os.path.exists(model_path)


def test_validate_nagl_model_path_failed():
    """Test that we cannot find false files."""
    with pytest.raises(FileNotFoundError):
        validate_nagl_model_path("does-not-exist.pt")


def test_local_validation(tmpdir):
    """Test that we can find local files."""
    with tmpdir.as_cwd():
        with pytest.raises(FileNotFoundError):
            validate_nagl_model_path("test.pt")

        with open("test.pt", "w") as f:
            f.write("test")
        model_path = validate_nagl_model_path("test.pt")
        assert os.path.exists(model_path)


def test_list_models():
    """Test that we can list models."""
    model_names = find_model_files()
    listed_model_names = list_available_nagl_models()
    assert listed_model_names == model_names


def test_entry_points():
    from pkg_resources import iter_entry_points
    for entry_point in iter_entry_points(group='openforcefield.nagl_model_directory'):
        paths = entry_point.load()()
        for path in paths:
            assert os.path.exists(path)
