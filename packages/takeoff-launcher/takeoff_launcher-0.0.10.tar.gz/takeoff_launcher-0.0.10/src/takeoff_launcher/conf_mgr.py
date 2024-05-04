"""
This module implements and instantiates the common configuration class used in the project.
"""

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import json
from pathlib import Path

from .utils import get_filtered_tags

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                           specifies all modules that shall be loaded and imported into the                           #
#                                current namespace when we use 'from package import *'                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

__all__ = ["conf_mgr"]


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Configuration Manager                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class ConfManager:
    """Configuration Manager class"""

    # paths for dev
    path_root: Path = Path(__file__).parent.parent.parent.resolve()  # takeoff_launcher/
    path_src: Path = path_root / "src"  # takeoff_launcher/src/

    # paths to the scripts
    path_package: Path = Path(__file__).parent.resolve()  # takeoff_launcher/
    path_version: Path = path_package / "version.txt"  # takeoff_launcher/version.txt

    # paths for cache
    path_cache: Path = Path.home() / ".takeoff_cache"  # ~/.takeoff_cache/
    path_cache_tags = path_cache / "versions.json"  # ~/.takeoff_cache/tags.json\

    # make sure the cache folder exist
    path_cache.mkdir(exist_ok=True, parents=True)

    # version
    current_cli_version: str = path_version.read_text().strip()

    if not path_cache_tags.exists():
        # initialize the cache data
        cache_json = {"cli_version": current_cli_version}

        # set the current takeoff version
        current_takeoff_version: str = "0.13.2"
        cache_json["takeoff_version"] = current_takeoff_version

        all_version_tags = get_filtered_tags("tytn/takeoff")

        # if the tags are not available, use the default versions
        if not all_version_tags:
            all_version_tags = ["0.13.2-cpu", "0.13.2-gpu"]

        cache_json["all_version_tags"] = all_version_tags

        # save the cache data
        with open(path_cache_tags, "w") as f:
            json.dump(cache_json, f)
    else:
        # load the cache data
        with open(path_cache_tags, "r") as f:
            cache_json = json.load(f)

            current_takeoff_version = cache_json.get("takeoff_version")
            all_version_tags = cache_json.get("all_version_tags")
            current_cli_version = cache_json.get("cli_version")

    # get unique versions. example
    all_versions = list({tag.split("-")[0] for tag in all_version_tags})
    all_versions.sort()

    # takeoff image
    image_name: str = "tytn/takeoff"
    image_tag_gpu: str = current_takeoff_version + "-gpu"
    image_tag_cpu: str = current_takeoff_version + "-cpu"

    def change_image_version(self, new_version: str):
        """Change the image version"""
        if new_version not in self.all_versions:
            raise ValueError(f"Invalid version: {new_version}. Available versions: {self.all_versions}")

        # update the cache data
        with open(self.path_cache_tags, "r") as f:
            cache_json = json.load(f)
            cache_json["takeoff_version"] = new_version

        # save the cache data
        with open(self.path_cache_tags, "w") as f:
            json.dump(cache_json, f)


# ─────────────────────────────────────────────── ConfManager Instance ─────────────────────────────────────────────── #

conf_mgr = ConfManager()
