# `takeoff`

**Usage**:

```console
$ takeoff [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `down`: Shut down a running takeoff server container.
* `list`: List all running takeoff server containers.
* `run`: Start a Takeoff server with options.
* `start`: Quickly start command.
* `version`: Print the current version of the Takeoff...

## `takeoff down`

Shut down a running takeoff server container.

**Usage**:

```console
$ takeoff down [OPTIONS]
```

**Options**:

* `-i, --id TEXT`: The ID of the server to shut down.
* `-a, --all`: Shut down all running servers.
* `--help`: Show this message and exit.

## `takeoff list`

List all running takeoff server containers.

**Usage**:

```console
$ takeoff list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `takeoff run`

Start a Takeoff server with options.

**Usage**:

```console
$ takeoff run [OPTIONS]
```

**Options**:

* `-m, --model TEXT`: The models to optimize.  [required]
* `-d, --device TEXT`: The device to use.  [required]
* `--max_batch_size INTEGER`: The maximum batch size.
* `--max_seq_len INTEGER`: The maximum sequence length.
* `--tensor_parallel INTEGER`: The number of tensor parallelism to use
* `--hf_access_token TEXT`: The HF Access token for gated models.
* `--license_key TEXT`: The license key.
* `--help`: Show this message and exit.

## `takeoff start`

Quickly start command. Type `takeoff start` to prompt the user for a quick start.

**Usage**:

```console
$ takeoff start [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `takeoff version`

Print the current version of the Takeoff Launcher CLI.

**Usage**:

```console
$ takeoff version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
* `--list`: List all available versions of the Takeoff image
* `--use`: Change the Takeoff image version.
