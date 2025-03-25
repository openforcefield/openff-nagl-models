import shutil
import pathlib
import pytest
from pytest_socket import disable_socket, enable_socket, SocketBlockedError
import platformdirs

from openff.nagl_models._dynamic_fetch import get_model


@pytest.mark.parametrize(
    "known_model",
    [
        "openff-gnn-am1bcc-0.0.1-alpha.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.1.pt",
        "openff-gnn-am1bcc-0.1.0-rc.2.pt",
        "openff-gnn-am1bcc-0.1.0-rc.3.pt",
    ],
)
def test_get_known_models(known_model):
    assert get_model(known_model).endswith(known_model)

    assert "OPENFF_NAGL_MODELS" in get_model(known_model)


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
        get_model.cache_clear()

        get_model("openff-gnn-am1bcc-0.1.0-rc.3.pt")


def test_file_exists_in_cache_without_internet():
    # since tests can run in different orders, make sure the file exists already
    assert get_model("openff-gnn-am1bcc-0.1.0-rc.3.pt")

    disable_socket()

    get_model("openff-gnn-am1bcc-0.1.0-rc.3.pt")


def test_error_on_missing_file():
    with pytest.raises(
        FileNotFoundError,
        match="Could not find asset with name 'FOOBAR",
    ):
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
def test_all_models_loadable(model):
    pytest.importorskip("openff.nagl")

    from openff.nagl.nn._models import GNNModel

    GNNModel.load(get_model(model), eval_mode=True)
