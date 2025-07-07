import functools
import hashlib
import json
import re
import pathlib
import urllib.request
from openff.utilities.exceptions import OpenFFError
import platformdirs
from packaging.version import Version


RELEASES_URL = "https://api.github.com/repos/openforcefield/openff-nagl-models/releases"

KNOWN_HASHES = {
    "openff-gnn-am1bcc-0.0.1-alpha.1.pt": "a0fcf53feab7182ea53aecec994bb6dba0833b0468a59392551c817cb7acb51a",
    "openff-gnn-am1bcc-0.1.0-rc.1.pt": "ee2dd8123f4b231d5de26bd63f47be94332a99d58095945a68e81b2efdcdfceb",
    "openff-gnn-am1bcc-0.1.0-rc.2.pt": "648b2636580f49f882591aedcc5c404a9cbbecb9ca1e082d98ccd71301db917f",
    "openff-gnn-am1bcc-0.1.0-rc.3.pt": "144ed56e46c5b3ad80157b342c8c0f8f7340e4d382a678e30dd300c811646bd0",
}

CACHE_DIR = platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS"

class HashComparisonFailedException(OpenFFError):
    """Exception raised when a NAGL file being loaded fails a comparison to a known or user-provided hash."""

def get_release_metadata() -> list[dict]:
    return json.loads(urllib.request.urlopen(RELEASES_URL).read().decode("utf-8"))


@functools.lru_cache()
def get_model(
    filename: str, doi: None | str = None, file_hash: None | str = None, _sandbox: bool = False
) -> str:
    """
    Return the path of a model as cached on disk, downloading if necessary.

    Parameters
    ----------
    filename : str
        The name of the file to search for.
    doi : typing.Optional[str], default=None
        The Zenodo DOI to use as a backup location for fetching the model file if it's not found in the local cache
        or in the
        [release metadata of an openff-nagl-models release](https://github.com/openforcefield/openff-nagl-models/releases)
        on GitHub. For example: "10.5072/zenodo.278300"
    file_hash : typing.Optional[str], default=None
        The sha256 hash of the model file to verify the correct contents. Hash checks are automatically performed
        on some OpenFF-released NAGL models. But if the model isn't released by OpenFF and this argument is
        not provided or has a value of `None`, then no hash check is performed. Raises HashComparisonFailedError if
        unsuccessful.
    _sandbox : bool, default=False
        Whether to connect to sandbox.zenodo.com instead of zenodo.com. Used for testing.

    Returns
    -------
    typing.Optional[pathlib.Path]
        The path to the file if it was found, otherwise None.


    """

    def assert_hash_equal(cached_path, expected_hash):
        actual_hash = _get_sha256(cached_path)
        if actual_hash != expected_hash:
            raise HashComparisonFailedException(f"NAGL model file hash check failed. Expected hash is "
                                                f"{expected_hash} but actual hash is {actual_hash}")

    pathlib.Path(CACHE_DIR).mkdir(exist_ok=True)

    cached_path = CACHE_DIR / filename

    check_hash = file_hash
    if check_hash is None and filename in KNOWN_HASHES:
        check_hash = KNOWN_HASHES[filename]

    if cached_path.exists():
        if check_hash:
            assert_hash_equal(cached_path, check_hash)

        return cached_path.as_posix()

    release_metadata = get_release_metadata()

    # tags with "v" prefix can't easily be sorted, but the result of passing through Version
    # are not necessarily 1:1 with the metadata in the releases, keep both and map between
    releases: dict[Version:str] = {
        Version(release["tag_name"]): release for release in release_metadata
    }

    for version in reversed(sorted(releases)):
        release = releases[version]
        for file in release["assets"]:
            if file["name"] == filename:
                path_to_file, _ = urllib.request.urlretrieve(
                    url=file["browser_download_url"],
                    filename=cached_path.as_posix(),
                )

                assert cached_path.exists()
                assert path_to_file == cached_path.as_posix()

                if check_hash:
                    assert_hash_equal(cached_path, check_hash)

                return cached_path.as_posix()

    if doi:
        zenodo_id = re.findall("10.5072/zenodo.([0-9]+)", doi)[0]

        # Remove "sandbox." to convert this to "real" zenodo before merge
        # Or keep in with a testing flag?
        file_url = (
            f"https://sandbox.zenodo.org/api/records/{zenodo_id}/files/{filename}"
        )
        path_to_file, _ = urllib.request.urlretrieve(
            file_url, filename=cached_path.as_posix()
        )
        assert cached_path.exists()
        assert path_to_file == cached_path.as_posix()

        if check_hash:
            assert_hash_equal(cached_path, check_hash)

        return cached_path.as_posix()

    raise FileNotFoundError(
        f"Could not find asset with name '{filename}' in any release"
    )


def _get_sha256(filename: str) -> str:
    """Get the SHA256 hash of a file from its path, assuming it's a binary file like a PyTorch model."""
    hash = hashlib.sha256()

    hash.update(open(filename, "rb").read())

    return hash.hexdigest()
