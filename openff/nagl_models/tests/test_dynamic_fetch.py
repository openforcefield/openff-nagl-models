import shutil
import pathlib
import pytest
from pytest_socket import disable_socket, enable_socket, SocketBlockedError
import platformdirs

from openff.nagl_models._dynamic_fetch import get_most_recent_asset_url


def test_get_known_models():
    for known_model in [
        "openff-gnn-am1bcc-0.0.1-alpha.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.2.pt",
        "openff-gnn-am1bcc-0.1.0-rc.3.pt",
    ]:
        assert get_most_recent_asset_url(known_model).endswith(known_model)

        assert "OPENFF_NAGL_MODELS" in get_most_recent_asset_url(known_model)


def test_access_interent_with_empty_cache():
    cache_path = platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS"

    if cache_path.exists():
        shutil.rmtree(cache_path)

    disable_socket()

    # would be nice to test the FileNotFoundError, but much more difficult to get that
    # particular network failure vs. checking that the network is accessed at all
    with pytest.raises(
        SocketBlockedError,
    ):
        get_most_recent_asset_url("openff-gnn-am1bcc-0.1.0-rc.3.pt")


def test_file_exists_in_cache_without_internet():
    # since tests can run in different orders, make sure the file exists already
    assert get_most_recent_asset_url("openff-gnn-am1bcc-0.1.0-rc.3.pt")

    disable_socket()

    get_most_recent_asset_url("openff-gnn-am1bcc-0.1.0-rc.3.pt")


def test_error_on_missing_file():
    with pytest.raises(
        FileNotFoundError,
        match="Could not find asset with name 'FOOBAR",
    ):
        get_most_recent_asset_url("FOOBAR.txt")
