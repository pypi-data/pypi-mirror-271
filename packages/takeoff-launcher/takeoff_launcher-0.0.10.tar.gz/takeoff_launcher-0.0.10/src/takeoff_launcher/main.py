"""Takeoff CLI for starting and managing Takeoff servers."""

# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import os

import typer
from loguru import logger
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table

from .conf_mgr import conf_mgr
from .sdk.takeoff import Takeoff
from .utils import (
    check_docker_environment,
    check_license_key_format,
    get_model_from_user,
    get_system_info,
    pull_image,
    run_license_validator,
)

# ───────────────────────────────────────────────── Global Settings ────────────────────────────────────────────────── #
main = typer.Typer(no_args_is_help=True)
console = Console()

# remove default logger to avoid logs in takeoff-sdk
logger.remove()


DEFAULT_MODELS = [
    "HuggingFaceH4/zephyr-7b-gemma-v0.1",
    "HuggingFaceH4/zephyr-7b-beta",
    "NousResearch/Llama-2-7b-chat-hf",
    "TitanML/llama2-7b-base-4bit-AWQ",
    "TheBloke/CodeLlama-7B-AWQ",
    "TheBloke/Mistral-7B-Instruct-v0.2-AWQ",
    "Others",
]

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                Takeoff Start Command                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


@main.command()
def start():
    """Quickly start command. Type `takeoff start` to prompt the user for a quick start."""

    # ─────────────────────────────────── check docker environment ─────────────────────────────────── #
    docker_installed = check_docker_environment()
    if not docker_installed:
        console.print(
            "[bold red]:x: Docker environment check failed. Please make sure Docker is installed and running.[/]"
        )
        return
    console.print("[bold green]:heavy_check_mark: Docker environment check passed[/]")

    # Create a Docker client
    import docker

    client = docker.from_env()

    # ─────────────────────────────────── check system environment ─────────────────────────────────── #
    sys_info = get_system_info()
    _, gpu_info = sys_info["CPU Info"], sys_info["GPU Info"]

    if isinstance(gpu_info, str):
        has_gpu = False
        # no gpu detected, we warn the user
        console.print(
            "[bold yellow]:warning: No Nvidia GPU detected. We recommend using a GPU for optimal performance.[/]"
        )
    else:
        has_gpu = True
        # gpu detected, we can print the gpu name and memory
        gpu_name = gpu_info["GPU 0"]["name"]
        gpu_memory = gpu_info["GPU 0"]["memory"]
        console.print(
            f"[bold green]:heavy_check_mark: Nvidia GPU detected:[/] [bold blue]{gpu_name}[/] with [bold blue]{gpu_memory}GB[/] memory."
        )

    # ────────────────────────────────────── check license key ─────────────────────────────────────── #

    # check if the user has a license key
    license_res_cache = run_license_validator("TEST")
    exit_code = license_res_cache["exit_code"]

    license_key = ""

    if exit_code == 0:
        console.print("[bold green]:heavy_check_mark: License key found[/]")
    else:
        console.print(
            "[bold yellow]:warning: No license key found. If you do not receive a license key, or if your existing license key has expired, please do not hesitate to reach out for support at hello@titanml.co.[/]"
        )

        # ask the user to enter the license key
        license_key = Prompt.ask("[bold]Please enter your license key: [/]", default="")
        if license_key == "":
            console.print("[bold red]:x: License key is required to start the server.[/]")
            return

        if not check_license_key_format(license_key):
            console.print("[bold red]:x: Invalid license key format. Please enter a valid license key.[/]")
            return

        license_res = run_license_validator(license_key)
        exit_code = license_res["exit_code"]
        if exit_code == 0:
            console.print("[bold green]:heavy_check_mark: License key validated successfully.[/]")
        else:
            console.print("[bold red]:x: License key validation failed.[/] Please enter a valid license key.")
            return

    console.print(
        Panel(
            "Welcome to Takeoff CLI! :rocket:\n\n"
            "Takeoff is a tool to deploy and manage any open source LLM models in a Docker container.\n"
            "You can use this CLI to start and manage Takeoff servers.\n\n"
            "Let's get started! :point_right:",
            title="Takeoff CLI",
            border_style="green",
            expand=False,
        )
    )

    # ──────────────────────────────── ask for model name and device ───────────────────────────────── #
    console.print("[bold]⚙ Please select a model to use:[/bold]", style="bold")
    model_name = get_model_from_user(DEFAULT_MODELS)

    if model_name == "Others":
        model_name = Prompt.ask("[bold]⚙ Please enter the model name: [/]", default="", show_default=False)
        if model_name == "":
            console.print("[bold red]:x: Model name is required to start the server.[/]")
            return

    device = Prompt.ask("[bold]⚙ Please enter the device to use: [/]", choices=["cpu", "gpu"], default="gpu")

    if device == "gpu":
        if not has_gpu:
            console.print(
                "[bold yellow]:warning: You have chosen to use a GPU, but no Nvidia GPU is detected. We recommend using a GPU for optimal performance."
            )
            confirm = Prompt.ask(
                "[bold]Are you sure you want to continue with a CPU?[/] (y/n)", choices=["y", "n"], default="n"
            )
            if confirm == "n":
                return
            else:
                device = "cpu"
                tag = conf_mgr.image_tag_cpu
                console.print(f"Starting Takeoff server with [bold blue]{model_name}[/] on [bold blue]CPU[/]...\n")
        else:
            device = "cuda"
            tag = conf_mgr.image_tag_gpu

            console.print(f"Starting Takeoff server with [bold blue]{model_name}[/] on [bold blue]{gpu_name}[/]...\n")
    elif device == "cpu":
        tag = conf_mgr.image_tag_cpu
        # warn the user about using cpu
        console.print(
            "[yellow]:warning: You have chosen to use a CPU. We will deploy the model on a CPU, but we [bold]strongly[/] recommend using a GPU for optimal performance."
        )
        console.print(f"Starting Takeoff server with [bold blue]{model_name}[/] on [bold blue]CPU[/]...\n")

    # ────────────────────────────────────── pull takeoff image ────────────────────────────────────── #

    images = client.images.list(name=f"{conf_mgr.image_name}:{tag}")
    if images:
        console.print(
            f"[bold green]:heavy_check_mark:[/] Image found: [bold blue]{conf_mgr.image_name}:{tag}[/] locally.\n"
        )
        os.environ["TAKEOFF_IMAGE"] = f"{conf_mgr.image_name}:{tag}"
    else:
        with Progress(
            SpinnerColumn(finished_text="[bold green]✔[/]"),
            TextColumn(
                f"Pulling latest takeoff container [bold blue]{conf_mgr.image_name}:{tag}[/] from Docker Hub..."
            ),
            transient=True,
        ) as progress:
            try:
                task1 = progress.add_task("Pulling image...", model=model_name, device=device)
                pull_image(conf_mgr.image_name, tag)
                progress.update(task1, completed=True)
                progress.console.print("[bold green]:heavy_check_mark:[/] Image pulled successfully.")
                os.environ["TAKEOFF_IMAGE"] = f"{conf_mgr.image_name}:{tag}"
            except Exception as e:
                progress.console.print(f"Image pull failed: {e}")
                return

    # ──────────────────────────────────── launch takeoff server ───────────────────────────────────── #
    with Progress(
        SpinnerColumn(finished_text="[bold green]✔[/]"),
        TextColumn(
            "Deploying [bold blue]{task.fields[model]}[/] on [bold blue]{task.fields[device]}[/] "
            "[yellow](This may take a few minutes depending on the model size and your internet connection.)[/]"
        ),
        transient=True,
    ) as progress:
        try:
            task1 = progress.add_task("Starting server...", model=model_name, device=device)
            takeoff = Takeoff(model_name=model_name, device=device, license_key=license_key)
            takeoff.start()
            progress.update(task1, completed=True)
            progress.console.print("[bold green]:heavy_check_mark:[/] Server deployed successfully.\n")
            progress.console.print("🚀[bold green]Takeoff Server started[/]🚀")
            progress.console.print(f"Takeoff Server running at: [bold blue]{takeoff.server_url}[/]")
            progress.console.print(f"Management server running at: [bold blue]{takeoff.management_url}[/]")
        except Exception as e:
            progress.console.print(f"Server start failed: {e}")
            return

    console.print(f"Now you can navigate to [bold blue]{takeoff.server_url}[/] to interact with the model.")
    console.print(
        f"You can access the logs inside the container by running [bold blue]`docker logs -f {takeoff.container.name}`[/]"
    )


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                 Takeoff Run Command                                                  #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


@main.command(help="Start a Takeoff server with options.")
def run(
    model_name: str = typer.Option(..., "--model", "-m", help="The models to optimize."),
    device: str = typer.Option(..., "--device", "-d", help="The device to use."),
    max_batch_size: int = typer.Option(None, "--max_batch_size", help="The maximum batch size."),
    max_seq_len: int = typer.Option(None, "--max_seq_len", help="The maximum sequence length."),
    tensor_parallel: int = typer.Option(None, "--tensor_parallel", help="The number of tensor parallelism to use"),
    access_token: str = typer.Option(None, "--hf_access_token", help="The HF Access token for gated models."),
    license_key: str = typer.Option(None, "--license_key", help="The license key."),
):
    try:
        takeoff = Takeoff(
            model_name=model_name,
            device=device,
            max_batch_size=max_batch_size,
            max_seq_len=max_seq_len,
            tensor_parallel=tensor_parallel,
            access_token=access_token,
            license_key=license_key,
        )
        takeoff.start()
    except Exception as e:
        typer.echo(f"Server start failed: {e}")


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                 Takeoff List Command                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


@main.command(help="List all running takeoff server containers.")
def list():
    # ─────────────────────────────────── check docker environment ─────────────────────────────────── #
    docker_installed = check_docker_environment()
    if not docker_installed:
        console.print(
            "[bold red]:x: Docker environment check failed. Please make sure Docker is installed and running.[/]"
        )
        return
    console.print("[bold green]:heavy_check_mark: Docker environment check passed[/]")

    # Create a Docker client
    import docker

    client = docker.from_env()

    # List all running containers
    containers = client.containers.list()

    table = Table()
    table.add_column("ID", style="cyan")
    table.add_column("Container Name", style="magenta")

    # Print the list of running containers
    for container in containers:
        if "takeoff" in container.name:
            table.add_row(container.short_id, container.name)
    console.print(table)


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                 Takeoff Down Command                                                 #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


@main.command(help="Shut down a running takeoff server container.")
def down(
    id: str = typer.Option(None, "--id", "-i", help="The ID of the server to shut down."),
    is_all: bool = typer.Option(False, "--all", "-a", help="Shut down all running servers."),
):
    # ─────────────────────────────────── check docker environment ─────────────────────────────────── #
    docker_installed = check_docker_environment()
    if not docker_installed:
        console.print(
            "[bold red]:x: Docker environment check failed. Please make sure Docker is installed and running.[/]"
        )
        return
    console.print("[bold green]:heavy_check_mark: Docker environment check passed[/]")

    # Create a Docker client
    import docker

    client = docker.from_env()
    if id is None and not is_all:
        console.print(
            Panel(
                "[bold red]:x: No container ID provided.[/]\n"
                "[bold yellow]Please provide a container ID or use the --all flag to shut down all running servers.[/]\n\n"
                "[Example]: `takeoff down --id <container_id>` or `takeoff down --all`\n"
                "[Note]: You can get the server ID by running `takeoff list`\n"
                "[Help]: Run `takeoff down --help` for more information.\n",
                title="Error",
                border_style="red",
                expand=False,
            )
        )
        return

    if id is not None:
        console.print(f"Shutting down server with ID {id}...")
        try:
            client.containers.get(id).stop()
            console.print("[bold green]:heavy_check_mark: Server shut down successfully.[/]")
        except Exception as e:
            console.print(f"[bold red]:x: Server shut down failed: {e}[/]")

    if is_all:
        typer.echo("Shutting down all servers...")
        # List all running containers
        containers = client.containers.list()

        # Print the list of running containers
        for container in containers:
            if "takeoff" in container.name:
                console.print(f"Shutting down server with ID {container.short_id}, Name: {container.name}")

                client.containers.get(container.name).stop()

        console.print("[bold green]:heavy_check_mark: All servers shut down successfully.[/]")


# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                               Takeoff Version Command                                                #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


@main.command(help="Print the current version of the Takeoff Launcher CLI.")
def version(
    list: bool = typer.Option(False, "--list", "-i", help="List all available versions of the Takeoff image"),
    use_version: str = typer.Option(None, "--use", "-u", help="Change the Takeoff image version"),
):
    """Print the current version of the Takeoff Launcher CLI."""

    if list:
        console.print("[bold]Available Takeoff Image Versions:[/bold]")
        for version in conf_mgr.all_versions:
            console.print(f"[bold blue]{version}[/]")
        return

    if use_version:
        try:
            conf_mgr.change_image_version(use_version)
            console.print(f"[bold green]Takeoff image version changed to {use_version} successfully.[/]")
        except ValueError as e:
            console.print(f"[bold red]:x: Error changing the image version: {e}[/]")
        return

    table = Table(title="Takeoff Version Information", title_style="bold")
    table.add_column("Information", style="green")
    table.add_column("Value", style="bold blue")
    table.add_row("Takeoff Launcher CLI Version", conf_mgr.current_cli_version)
    table.add_row("Takeoff Image Version", conf_mgr.current_takeoff_version)
    table.add_row("Takeoff Image Name", conf_mgr.image_name)
    table.add_row("Takeoff Image Tag (GPU)", conf_mgr.image_tag_gpu)
    table.add_row("Takeoff Image Tag (CPU)", conf_mgr.image_tag_cpu)
    console.print(table)


if __name__ == "__main__":
    main()
