import os
import shutil

import platformdirs
import pytest

from openff.nagl_models import (
    get_models_by_type,
    list_available_nagl_models,
    validate_nagl_model_path,
)
from openff.nagl_models._dynamic_fetch import (
    BadFileSuffixError,
    HashComparisonFailedException,
    UnableToParseDOIException,
    get_model,
)


@pytest.fixture
def hide_cache():
    cache_dir = platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS"
    alt_dir = str(cache_dir) + "_temp"

    if os.path.exists(alt_dir):
        raise FileExistsError(f"Temporary directory already exists: {alt_dir}")

    if os.path.exists(cache_dir):
        shutil.move(cache_dir, alt_dir)

    yield

    if os.path.exists(alt_dir):
        if os.path.exists(cache_dir):
            shutil.rmtree(cache_dir)
        shutil.move(alt_dir, cache_dir)


def test_zenodo_fetching_and_caching(hide_cache):
    """
    All of the tests that rely on remote fetching into the cache
    and checking whether something is in the cache need to be run in
    serial, otherwise they'll interfere with each other, so they're
    all consolidated into this one test.
    """

    # This test uses a Zenodo sandbox DOI (10.5072 prefix) and the corresponding
    # SHA256 hash of the test file "my_favorite_model.pt" (which is a copy of
    # openff-gnn-am1bcc-0.1.0-rc.3.pt) uploaded to that sandbox record

    from pytest_socket import SocketBlockedError, disable_socket, enable_socket

    from openff.nagl_models import get_nagl_model_dirs_paths
    from openff.nagl_models._dynamic_fetch import CACHE_DIR

    disable_socket()

    # Ensure that the cache is hidden,
    with pytest.raises(FileNotFoundError):
        get_model(
            "my_favorite_model.pt",
        )

    # Ensure the test file isn't in the cache or the nagl_models package
    assert not (os.path.exists(CACHE_DIR / "my_favorite_model.pt"))
    for dir_path in get_nagl_model_dirs_paths():
        assert not (os.path.exists(dir_path / "my_favorite_model.pt"))

    # Ensure that trying to fetch a
    # model fails due to lack of internet access
    with pytest.raises(
        SocketBlockedError,
    ):
        get_model(
            "my_favorite_model.pt",
            doi="10.5072/zenodo.278300",
            file_hash="127eb0b9512f22546f8b455582bcd85b2521866d32b86d231fee26d4771b1d81",
        )

    # Ensure that the file can actually be fetched
    enable_socket()
    get_model(
        "my_favorite_model.pt",
        doi="10.5072/zenodo.278300",
    )

    # Ensure that the file is really in the cache
    assert os.path.exists(CACHE_DIR / "my_favorite_model.pt")
    # Ensure that, once fetched, the file can be gotten without accessing the internet.
    disable_socket()
    # Ensure that cached files can be accessed when no optional arguments are provided
    get_model(
        "my_favorite_model.pt",
    )

    # Ensure that a network call is not made if the requested file is in the cache
    get_model(
        "my_favorite_model.pt",
        doi="10.5072/zenodo.278300",
    )

    # Ensure that cached files can be accessed when all optional arguments are provided
    get_model(
        "my_favorite_model.pt",
        doi="10.5072/zenodo.278300",
        file_hash="127eb0b9512f22546f8b455582bcd85b2521866d32b86d231fee26d4771b1d81",
    )

    # Ensure that cached files can be accessed when only hash is provided
    get_model(
        "my_favorite_model.pt",
        file_hash="127eb0b9512f22546f8b455582bcd85b2521866d32b86d231fee26d4771b1d81",
    )

    # Ensure that cached files raise hash comparison errors
    with pytest.raises(HashComparisonFailedException):
        get_model(
            "my_favorite_model.pt",
            doi="10.5072/zenodo.278300",
            file_hash="wrong_hash",
        )


def test_error_on_missing_file():
    with pytest.raises(FileNotFoundError, match="Could not find asset with name 'FOOBAR"):
        get_model("FOOBAR.pt")


def test_error_on_bad_file_suffix():
    with pytest.raises(
        BadFileSuffixError,
        match="Found an unrecognized file path extension on filename='FOOBAR.txt'",
    ):
        get_model("FOOBAR.txt")


@pytest.mark.parametrize(
    "model",
    [
        "openff-gnn-am1bcc-0.0.1-alpha.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.2.pt",
        "openff-gnn-am1bcc-0.1.0-rc.3.pt",
        "openff-gnn-am1bcc-1.0.0.pt",
    ],
)
def test_all_models_loadable(model):
    pytest.importorskip("openff.nagl")

    from openff.nagl.nn._models import GNNModel

    GNNModel.load(get_model(model), eval_mode=True)


def test_user_provided_hash_conflicts_with_known_hash():
    with pytest.raises(HashComparisonFailedException):
        get_model("openff-gnn-am1bcc-0.1.0-rc.3.pt", file_hash="wrong_hash")


def test_malformed_doi():
    with pytest.raises(UnableToParseDOIException):
        get_model("nonexistent.pt", doi="zenodo.278300")


def test_no_matching_file_at_doi():
    with pytest.raises(FileNotFoundError, match="sandbox.zenodo"):
        get_model("file_that_doesnt_exist.pt", doi="10.5072/zenodo.278300")


# Test to ensure that an unsupported behavior needed by OpenFE remains functional
# This is temporary, if this test fails please update on the following issues:
# https://github.com/openforcefield/openff-toolkit/issues/2095
# https://github.com/openforcefield/openff-nagl-models/issues/68
@pytest.mark.parametrize("list_method_output", list_available_nagl_models() + get_models_by_type("am1bcc"))
@pytest.mark.parametrize("get_method", [get_model, validate_nagl_model_path])
def test_output_of_list_models_is_input_to_model_use(list_method_output, get_method):
    get_method(list_method_output)
