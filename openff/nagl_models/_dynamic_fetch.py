import urllib.request
import json
from packaging.version import Version
import platformdirs
import pathlib


RELEASES_URL = "https://api.github.com/repos/openforcefield/openff-nagl-models/releases"

release_metadata: list[dict] = json.load(urllib.request.urlopen(RELEASES_URL))

# tags with "v" prefix can't easily be sorted, but the result of passing through Version
# are not necessarily 1:1 with the metadata in the releases, keep both and map between
releases: dict[Version:str] = {
    Version(release["tag_name"]): release for release in release_metadata
}


def get_most_recent_asset_url(filename: str) -> str:
    pathlib.Path(platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS").mkdir(
        exist_ok=True
    )

    cached_path = platformdirs.user_cache_path() / "OPENFF_NAGL_MODELS" / filename

    if cached_path.exists():
        return cached_path.as_posix()

    for version in reversed(sorted(releases)):
        release = releases[version]
        for file in release["assets"]:
            if file["name"] == filename:
                urllib.request.urlretrieve(
                    file["url"],
                    cached_path,
                )

                return cached_path.as_posix()

    raise FileNotFoundError(
        f"Could not find asset with name '{filename}' in any release"
    )
