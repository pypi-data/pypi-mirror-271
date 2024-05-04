"""Utility functions for the Takeoff Cli."""

import platform
import re
from pathlib import Path

import psutil
import requests
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator


def check_docker_environment():
    """Check if Docker is installed and running."""

    try:
        import docker

        client = docker.from_env()
        client.containers.list()
        return True
    except Exception:
        return False


def check_device_environment():
    """Check system device information."""

    return get_system_info()


def check_license_key_format(license_key: str) -> bool:
    """Check if the license key format is valid.

    Args:
        license_key (str): Input license key.

    Returns:
        bool: True if the license key format is valid, False otherwise.
    """
    pattern = r"^[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}$"
    return bool(re.match(pattern, license_key))


def bytes_to_gb(bytes: int) -> float:
    """Convert bytes to gigabytes."""
    return bytes / (1024**3)


def get_system_info() -> dict:
    try:
        import pynvml

        pynvml.nvmlInit()
        gpu_info = {}
        device_count = pynvml.nvmlDeviceGetCount()
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)

            gpu_info[f"GPU {i}"] = {
                "name": pynvml.nvmlDeviceGetName(handle),
                "memory": round(bytes_to_gb(memory_info.total), 2),
                "memory_unit": "GB",
                "driver": pynvml.nvmlSystemGetDriverVersion(),
            }
        pynvml.nvmlShutdown()
    except ImportError:
        gpu_info = "NVIDIA library (pynvml) not installed or no NVIDIA GPU detected."  # type: ignore
    except pynvml.NVMLError:
        gpu_info = "no NVIDIA GPU detected."
    except Exception as e:
        gpu_info = f"Error getting GPU information: {e}"

    cpu_info = {
        "processor": platform.processor(),
        "architecture": platform.machine(),
        "physical_cores": psutil.cpu_count(logical=False),
        "total_cores": psutil.cpu_count(logical=True),
    }

    return {"CPU Info": cpu_info, "GPU Info": gpu_info}


def pull_image(image_name: str, tag: str = "latest") -> None:
    import docker

    client = docker.from_env()
    try:
        client.images.pull(image_name, tag=tag)
    except docker.errors.APIError as e:
        raise Exception(f"Error pulling image {image_name}:{tag}. {e}")


def get_model_from_user(models):
    """
    Show a selection list to the user with the models available.

    :param models: A list of model names (strings) available for selection.
    :return: The name of the model selected by the user.
    """
    model_name = inquirer.select(
        message="We provide a list of models to choose from. If you want to use a model that is not listed, please choose 'Others' and provide the model name in HF repo format.\n",
        choices=models,
        validate=EmptyInputValidator("A selection is required."),
        vi_mode=False,
        cycle=True,
    ).execute()

    return model_name


def run_license_validator(license_key) -> dict:
    """Run the license validator in a Docker container and return the results.

    Args:
        license_key (str): The license key to validate.

    Returns:
        dict: The results of the license validation, including the exit code and output.
    """
    import docker

    # Initialize a Docker client
    client = docker.from_env()

    volumes = [f"{Path.home()}/.takeoff_cache:/code/models"]

    # Run the container with the license key as a command-line argument
    container = client.containers.run(
        "tytn/license-validation:latest", command=["22918", license_key], remove=False, detach=True, volumes=volumes
    )

    # Wait for the container to finish running
    result = container.wait()

    # Retrieve the exit code and output
    exit_code = result["StatusCode"]
    output = container.logs().decode("utf-8")

    container.remove()

    # Return the results
    return {"exit_code": exit_code, "output": output}


def get_filtered_tags(repository_name) -> list:
    """
    Retrieves and filters tags for a given repository on Docker Hub using a regex pattern.

    Args:
        repository_name (str): The full name of the repository (e.g., 'tytn/takeoff').

    Returns:
        list: A list of filtered tag names.
    """

    registry_url = f"https://registry.hub.docker.com/v2/repositories/{repository_name}/tags"
    tags = []
    pattern = re.compile(r"\d+\.\d+\.\d+-(gpu|cpu)")

    try:
        while registry_url:
            # List tags
            tags_response = requests.get(registry_url)
            tags_response.raise_for_status()
            response_json = tags_response.json()

            # Filter tags based on the regex pattern
            tags.extend([tag["name"] for tag in response_json["results"] if pattern.match(tag["name"])])

            # Prepare for next page, if any
            registry_url = response_json["next"]
    except Exception as e:
        print(f"Error fetching tags for {repository_name}: {e}")

    return tags
