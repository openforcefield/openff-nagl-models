import hashlib
import json
import pathlib
import re
import urllib.request

import platformdirs

from openff.nagl_models import validate_nagl_model_path

RELEASES_URL = "https://api.github.com/repos/openforcefield/openff-nagl-models/releases"

KNOWN_HASHES = {
    "openff-gnn-am1bcc-0.0.1-alpha.1.pt": "a0fcf53feab7182ea53aecec994bb6dba0833b0468a59392551c817cb7acb51a",
    "openff-gnn-am1bcc-0.1.0-rc.1.pt": "ee2dd8123f4b231d5de26bd63f47be94332a99d58095945a68e81b2efdcdfceb",
    "openff-gnn-am1bcc-0.1.0-rc.2.pt": "648b2636580f49f882591aedcc5c404a9cbbecb9ca1e082d98ccd71301db917f",
    "openff-gnn-am1bcc-0.1.0-rc.3.pt": "144ed56e46c5b3ad80157b342c8c0f8f7340e4d382a678e30dd300c811646bd0",
    "openff-gnn-am1bcc-1.0.0.pt": "7981e7f5b0b1e424c9e10a40d9e7606d96dcd3dd2b095cb4eeff6829f92238ee",
}

CACHE_DIR = platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS"


class HashComparisonFailedException(Exception):
    """Exception raised when a NAGL file being loaded fails a comparison to a known or user-provided hash."""


class UnableToParseDOIException(Exception):
    """Exception raised when a Zenodo DOI is unable to be parsed according to the expected pattern."""


class BadFileSuffixError(Exception):
    """Exception raised when a model file with an incorrect suffix is requested (this will happen a
    lot with the current working of the ToolkitRegistry.call method, where things like "am1bcc" will
    be requested from get_model due to toolkit precedence."""


def get_release_metadata() -> list[dict]:
    return json.loads(urllib.request.urlopen(RELEASES_URL).read().decode("utf-8"))


def get_model(
    filename: str,
    doi: None | str = None,
    file_hash: None | str = None,
) -> str:
    """
    Return the path of a model as cached on disk, downloading if necessary. The lookup order of this implementation is:
    1. Try to retrieve the file from the installed `openff-nagl-models` python package on disk
    2. Try to retrieve the file from the local cache
    3. Try to fetch the file from the Zenodo DOI, if provided

    This method will raise an HashComparisonFailedException as soon as a hash mismatch is encountered. So if
    there's a file with a matching name but a non-matching hash in the local cache, an exception will be raised
    immediately, even if a file with a matching name that WOULD satisfy the hash check exists in release
    metadata or at a provided Zenodo DOI.

    Parameters
    ----------
    filename
        The name of the file to search for.
    doi
        The Zenodo DOI to use as a backup location for fetching the model file if it's not found in the local cache
        or in the
        [release metadata of an openff-nagl-models release](https://github.com/openforcefield/openff-nagl-models/releases)
        on GitHub. For example: "10.5072/zenodo.278300"
    file_hash
        The sha256 hash of the model file to verify the correct contents. Hash checks are automatically performed
        on some OpenFF-released NAGL models. But if the model isn't released by OpenFF and this argument is
        not provided or has a value of `None`, then no hash check is performed. Raises HashComparisonFailedException
        if unsuccessful. If a user provides a hash value here that disagrees with the known hash for the same file
        name, the user-provided hash takes precedence.

    Returns
    -------
    str
        The path to the file if it was found. If the file wasn't found then a FileNotFoundError is raised.

    Raises
    ------
    HashComparisonFailedException
    FileNotFoundError
    """
    # Cast to str to temporarily preserve old behavior, see https://github.com/openforcefield/openff-toolkit/issues/2095
    if not (str(filename).endswith(".pt")):
        raise BadFileSuffixError(
            f"OpenFF NAGL models are based on PyTorch files and expect a `.pt` suffix. Found an "
            f"unrecognized file path extension on {filename=}"
        )
    pathlib.Path(CACHE_DIR).mkdir(exist_ok=True)

    # See if the file has a known hash
    if file_hash is None and filename in KNOWN_HASHES:
        file_hash = KNOWN_HASHES[filename]

    # See if it's available in the openff-nagl-models python package
    try:
        file_path = validate_nagl_model_path(filename)
        # If filename happens to be an absolute path (not guaranteed this is in scope, but is temporarily supported,
        # see https://github.com/openforcefield/openff-nagl-models/issues/68) the hash check will be skipped.
        # This isn't a final decision on any behaviors, just a temporary workaround.
        if file_hash is not None:
            assert_hash_equal(file_path, file_hash)
        return file_path.as_posix()
    except FileNotFoundError:
        pass

    # Then check if it's in the cache
    cached_path = CACHE_DIR / filename
    if cached_path.exists():
        if file_hash:
            assert_hash_equal(cached_path, file_hash)

        return cached_path.as_posix()

    # Otherwise try to fetch from DOI
    if doi:
        try:
            match = re.search(r"10\.(5072|5281)/zenodo\.([0-9]+)", doi)
            if not match:
                raise IndexError
            prefix, zenodo_id = match.groups()
        except (IndexError, AttributeError):
            raise UnableToParseDOIException(
                f"Unable to parse Zenodo DOI {doi}. DOI values are expected to look "
                f"like '10.5281/zenodo.278300' (production) or '10.5072/zenodo.278300' (sandbox)"
            )

        if prefix == "5072":
            file_url = f"https://sandbox.zenodo.org/api/records/{zenodo_id}/files/{filename}"
        else:
            file_url = f"https://zenodo.org/api/records/{zenodo_id}/files/{filename}"

        try:
            return _download_and_verify_file(file_url, cached_path, file_hash)
        except urllib.error.HTTPError:
            raise FileNotFoundError(f"No file at {file_url}")

    raise FileNotFoundError(f"Could not find asset with name '{filename}' in any release")


def assert_hash_equal(cached_path, expected_hash):
    actual_hash = _get_sha256(cached_path)
    if actual_hash != expected_hash:
        raise HashComparisonFailedException(
            f"NAGL model file hash check failed. Expected hash is {expected_hash} but actual hash is {actual_hash}"
        )


def _download_and_verify_file(url: str, cached_path: pathlib.Path, file_hash: None | str = None) -> str:
    """Download a file from URL to cached_path and optionally verify its hash."""
    path_to_file, _ = urllib.request.urlretrieve(url, filename=cached_path.as_posix())

    assert cached_path.exists()
    assert path_to_file == cached_path.as_posix()

    if file_hash:
        assert_hash_equal(cached_path, file_hash)

    return cached_path.as_posix()


def _get_sha256(filename: str) -> str:
    """Get the SHA256 hash of a file from its path, assuming it's a binary file like a PyTorch model."""
    hash = hashlib.sha256()

    hash.update(open(filename, "rb").read())

    return hash.hexdigest()
