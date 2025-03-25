import functools
import hashlib
import json
import pathlib
import urllib.request

import platformdirs
from packaging.version import Version


RELEASES_URL = "https://api.github.com/repos/openforcefield/openff-nagl-models/releases"

KNOWN_HASHES = {
    "openff-gnn-am1bcc-0.0.1-alpha.1.pt": "a0fcf53feab7182ea53aecec994bb6dba0833b0468a59392551c817cb7acb51a",
    "openff-gnn-am1bcc-0.1.0-rc.1.pt": "ee2dd8123f4b231d5de26bd63f47be94332a99d58095945a68e81b2efdcdfceb",
    "openff-gnn-am1bcc-0.1.0-rc.2.pt": "648b2636580f49f882591aedcc5c404a9cbbecb9ca1e082d98ccd71301db917f",
    "openff-gnn-am1bcc-0.1.0-rc.3.pt": "144ed56e46c5b3ad80157b342c8c0f8f7340e4d382a678e30dd300c811646bd0",
}


@functools.lru_cache()
def get_model(filename: str) -> str:
    """Return the path of a model as cached on disk, downloading if necessary."""
    pathlib.Path(platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS").mkdir(
        exist_ok=True
    )

    cached_path = platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS" / filename

    if cached_path.exists():
        assert _get_sha256(cached_path) == KNOWN_HASHES[filename]

        return cached_path.as_posix()

    release_metadata: list[dict] = json.load(urllib.request.urlopen(RELEASES_URL))

    # tags with "v" prefix can't easily be sorted, but the result of passing through Version
    # are not necessarily 1:1 with the metadata in the releases, keep both and map between
    releases: dict[Version:str] = {
        Version(release["tag_name"]): release for release in release_metadata
    }

    for version in reversed(sorted(releases)):
        release = releases[version]
        for file in release["assets"]:
            if file["name"] == filename:
                urllib.request.urlretrieve(
                    file["browser_download_url"],
                    cached_path,
                )

                assert _get_sha256(cached_path) == KNOWN_HASHES[filename], (
                    f"Hash mismatch for {filename}"
                )
                assert cached_path.exists()

                return cached_path.as_posix()

    raise FileNotFoundError(
        f"Could not find asset with name '{filename}' in any release"
    )


def _get_sha256(filename: str) -> str:
    """Get the SHA256 hash of a file from its path, assuming it's a binary file like a PyTorch model."""
    hash = hashlib.sha256()

    hash.update(open(filename, "rb").read())

    return hash.hexdigest()
