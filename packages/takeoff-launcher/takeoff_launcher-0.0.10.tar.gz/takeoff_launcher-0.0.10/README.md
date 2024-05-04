# Takeoff Launcher

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

Takeoff Launcher is a Python command-line tool that makes it easier to start a Takeoff server container. Think of it as a handy wrapper for the Docker API. It simplifies launching Takeoff containers by managing the license key verification and ensuring your environment is set up correctly.

## Getting Started <a name = "getting_started"></a>

### Prerequisites

Before you get started, make sure you have:

- Docker installed on your machine.
- An Nvidia GPU with CUDA support (this is optional but recommended for the best performance).
- A Takeoff License Key.


### Installing

To install Takeoff Launcher, run this command:

```bash
pip install takeoff_launcher
```

After installation, you can check if it's installed correctly by running:

```bash
takeoff
```

If everything is set up properly, you should see the Takeoff Launcher welcome message or help information.


## Usage

For detailed instructions on how to use the Takeoff Launcher, including commands and options, please see the [Usage Documentation](docs/usage.md).