"""Takeoff Object SDK"""

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import os
import time

import yaml
from loguru import logger

from .schema import TakeoffEnvSetting
from .utils import is_docker_logs_error, is_takeoff_loading, start_takeoff, start_takeoff_with_manifest

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                       Takeoff                                                        #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


class Takeoff:
    def __init__(self, model_name=None, device=None, use_manifest=False, **kwargs):
        self.model_name = model_name
        self.device = device

        self.models = []
        self.consumer_groups = {}
        self.server_url = None
        self.management_url = None
        self.openai_url = None
        self.container = None

        self.use_manifest = use_manifest

        if not self.use_manifest:
            self.takeoff_config = TakeoffEnvSetting(model_name=model_name, device=device, **kwargs)
            self.num_readers = 1

    def cleanup(self):
        """Remove the Takeoff container if it exists"""
        if self.container:
            self.container.remove(force=True)

    @classmethod
    def from_config(cls, takeoff_config: TakeoffEnvSetting):
        """Create a Takeoff object from a TakeoffEnvSetting object

        Args:
            takeoff_config (TakeoffEnvSetting): Takeoff configuration

        Returns:
            Takeoff: Takeoff object
        """

        takeoff_args = takeoff_config.model_dump()
        return cls(**takeoff_args)

    @classmethod
    def from_manifest(cls, manifest_path: str, device: str = "cuda"):
        """Create a Takeoff object from a manifest file

        Args:
            manifest_path (str): path to the manifest file
            device (str, optional): device choice. Defaults to "cuda".

        Raises:
            FileNotFoundError: if the manifest file is not found

        Returns:
            Takeoff: Takeoff object
        """

        # turns the user input manifest path into an absolute path
        manifest_path = os.path.abspath(manifest_path)

        if not os.path.exists(manifest_path):
            raise FileNotFoundError(f"Manifest file not found at {manifest_path}")

        yaml_file = yaml.safe_load(open(manifest_path, "r"))

        cls.num_readers = len(yaml_file["takeoff"]["readers_config"].keys())
        cls.manifest_path = manifest_path

        return cls(device=device, use_manifest=True)

    def start(self):
        """Start the Takeoff server and add the model to the primary consumer group"""

        logger.info("Starting Takeoff server...")
        if self.use_manifest:
            logger.info(f"Using manifest file: {self.manifest_path}")
            (
                self.takeoff_port,
                self.management_port,
                self.openai_port,
                self.prometheus_port,
                self.container,
            ) = start_takeoff_with_manifest(self.manifest_path, self.device)
        else:
            (
                self.takeoff_port,
                self.management_port,
                self.openai_port,
                self.prometheus_port,
                self.container,
            ) = start_takeoff(self.takeoff_config)

        self.server_url = f"http://localhost:{self.takeoff_port}"
        self.management_url = f"http://localhost:{self.management_port}"
        self.openai_url = f"http://localhost:{self.openai_port}"
        self.prometheus_url = f"http://localhost:{self.prometheus_port}"

        logger.info(f"Takeoff server running at: {self.server_url}")
        logger.info(f"Takeoff management server running at: {self.management_url}")
        logger.info(f"Takeoff openai compatible server running at: {self.openai_url}")
        logger.info(f"Takeoff prometheus server running at: {self.prometheus_url}")

        for _ in range(200):  # Some models take a while to download
            if not is_takeoff_loading(self.server_url, self.num_readers):
                break

            error_message = is_docker_logs_error(self.container)

            if error_message is not None:
                logger.error("Takeoff server failed to start. Error in docker logs. Cleaning up...")
                self.cleanup()
                raise Exception(
                    "Takeoff server failed to start due to error in docker logs. See below for details. \n"
                    + error_message
                )
            logger.info("building...")
            time.sleep(3)
        else:
            raise Exception("Takeoff server build timed out")

        logger.info("server ready!")
