# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [Unreleased]

- /

## [0.3.4] - 2024-03-18

### Change

- Deprecated: Change the package name to takeoff-launcher

## [0.3.3] - 2024-03-15

### Change

- change `is_takeoff_loading` checking function from using `healthz` to `status`, for solving the problem that not checking all readers are ready when we have multiple readers in manifest mode.


## [0.3.2] - 2024-03-11

### Fix

- fixed an issue where a block of the code caused the server to start unreliably. This code has been removed.

## [0.3.1] - 2024-03-09

### Change

- add command option for start_container utils function

## [0.2.1] - 2024-03-04

### Change

- add api as one of the option of device for compatiblity with API reader integration test 

## [0.2.0] - 2024-02-26

### Feature

- Change schema.py to make it compatible with new image to text feature 

## [0.1.0] - 2024-02-11

### Feature

- Add ability to launch takeoff using manifest

### Fixed

- Fix incompatible default environment varible in takeoff sdk. Change the default value to make the takeoff gateway default value single source of truth
- Fix unit tests not picking up openai port

## [0.0.5] - 2024-02-07

### Fixed

- Change openai port forwarding behavior to make integration test run in parallel mode.

## [0.0.4] - 2024-02-07

### Added

- Added 3003 as the default port forwarding option in docker launch for openAI compatible api.

## [0.0.3] - 2024-01-16

### Fixed

- Fix typo `reill_threshold`, should be `refill_threshold`

## [0.0.2] - 2024-01-15

### Added

- add attribute `refill_threshold` into schema, which is `TAKEOFF_REFILL_THRESHOLD` Env var
- add function `cleanup()` for cleaning up the docker container
- improve error traceback message. now spining takeoff will catch error message inside the docker and print it outside.

## [0.0.1] - 2024-01-11

- initial release
- add takeoff python sdk, publishing on [PyPI](https://pypi.org/project/takeoff-sdk/)

<!-- Links -->

[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
