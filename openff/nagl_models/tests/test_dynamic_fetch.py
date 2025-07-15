import json
import os
import pathlib
import shutil
import urllib.request

import platformdirs
import pytest

import openff.nagl_models._dynamic_fetch
from openff.nagl_models import __file__ as root
from openff.nagl_models._dynamic_fetch import (
    get_model,
    HashComparisonFailedException,
    UnableToParseDOIException,
)


def mocked_urlretrieve(url, filename):
    """Mock downloading files from assets by copying from the models/ directory."""
    old = (
        pathlib.Path(root).parent / "models/am1bcc" / pathlib.Path(filename).name
    ).as_posix()
    new = (platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS" / filename).as_posix()

    shutil.copy(old, new)

    return new, None


def mocked_get_release_metadata():
    # can regenerate this file with
    # $ wget https://api.github.com/repos/openforcefield/openff-nagl-models/releases
    return json.loads(
        open(pathlib.Path(root).parent / "tests/data/releases.json").read()
    )


@pytest.mark.parametrize(
    "known_model",
    [
        "openff-gnn-am1bcc-0.0.1-alpha.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.2.pt",
        "openff-gnn-am1bcc-0.1.0-rc.3.pt",
    ],
)
def test_get_known_models(monkeypatch, known_model):
    with monkeypatch.context() as m:
        m.setattr(
            urllib.request,
            "urlretrieve",
            mocked_urlretrieve,
        )
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )

        assert get_model(known_model).endswith(known_model)

        assert "OPENFF_NAGL_MODELS" in get_model(known_model)


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


def test_access_internet_with_empty_cache(hide_cache):
    from pytest_socket import SocketBlockedError, disable_socket

    cache_path = platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS"

    disable_socket()

    # would be nice to test the FileNotFoundError, but much more difficult to get that
    # particular network failure vs. checking that the network is accessed at all
    with pytest.raises(
        SocketBlockedError,
    ):
        get_model.cache_clear()

        get_model("openff-gnn-am1bcc-0.1.0-rc.3.pt")


def test_file_exists_in_cache_without_internet(monkeypatch):
    from pytest_socket import disable_socket

    # since tests can run in different orders, make sure the file exists already
    with monkeypatch.context() as m:
        m.setattr(
            urllib.request,
            "urlretrieve",
            mocked_urlretrieve,
        )
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )

        assert get_model("openff-gnn-am1bcc-0.1.0-rc.3.pt")

        disable_socket()

        get_model("openff-gnn-am1bcc-0.1.0-rc.3.pt")


def test_error_on_missing_file(monkeypatch):
    with (
        pytest.raises(
            FileNotFoundError,
            match="Could not find asset with name 'FOOBAR",
        ),
        monkeypatch.context() as m,
    ):
        m.setattr(
            urllib.request,
            "urlretrieve",
            mocked_urlretrieve,
        )
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )

        get_model("FOOBAR.txt")


@pytest.mark.parametrize(
    "model",
    [
        "openff-gnn-am1bcc-0.0.1-alpha.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.2.pt",
        "openff-gnn-am1bcc-0.1.0-rc.3.pt",
    ],
)
def test_all_models_loadable(model, monkeypatch):
    pytest.importorskip("openff.nagl")

    from openff.nagl.nn._models import GNNModel

    with monkeypatch.context() as m:
        m.setattr(
            urllib.request,
            "urlretrieve",
            mocked_urlretrieve,
        )
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )

        GNNModel.load(get_model(model), eval_mode=True)


def test_get_model_by_doi_and_hash(hide_cache, monkeypatch):
    # This test uses a Zenodo sandbox DOI (10.5072 prefix) and the corresponding
    # SHA256 hash of the test file uploaded to that sandbox record
    with monkeypatch.context() as m:
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )

        get_model(
            "my_favorite_model.pt",
            doi="10.5072/zenodo.278300",
            file_hash="127eb0b9512f22546f8b455582bcd85b2521866d32b86d231fee26d4771b1d81",
        )

def test_get_model_by_doi_no_hash(hide_cache, monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )

        get_model("my_favorite_model.pt", doi="10.5072/zenodo.278300")


def test_get_model_hash_comparison_fails(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )

        with pytest.raises(HashComparisonFailedException):
            get_model(
                "my_favorite_model.pt",
                doi="10.5072/zenodo.278300",
                file_hash="wrong_hash",
            )

def test_user_provided_hash_conflicts_with_known_hash(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )
        with pytest.raises(HashComparisonFailedException):
            get_model("openff-gnn-am1bcc-0.1.0-rc.3.pt", file_hash="wrong_hash")


def test_malformed_doi(monkeypatch, hide_cache):
    with monkeypatch.context() as m:
        m.setattr(
            urllib.request,
            "urlretrieve",
            mocked_urlretrieve,
        )
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )

        with pytest.raises(UnableToParseDOIException):
            get_model("my_favorite_model.pt", doi="zenodo.278300")


def test_no_matching_file_at_doi(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(
            openff.nagl_models._dynamic_fetch,
            "get_release_metadata",
            mocked_get_release_metadata,
        )
        with pytest.raises(FileNotFoundError, match="sandbox.zenodo"):
            get_model("file_that_doesnt_exist.pt", doi="10.5072/zenodo.278300")
