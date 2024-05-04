# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog],
and this project adheres to [Semantic Versioning].

## [0.0.10] - 2024-05-03

- Allow user to specify extra env variables for takeoff with the 'env' key.

## [0.0.9] - 2024-04-11

### Changed

- Removed any reference to `iris_cache` and replaced with `takeoff_cache`.

## [0.0.8] - 2024-03-26

### Added

- add the ability to switch version in `takeoff version` command. store the version information in takeoff_cache

### Fixed

- add docker error detection for takeoff custom exception checking. ie OOM

## [0.0.7] - 2024-03-21

### Fixed

- fix version.txt still not included.

## [0.0.6] - 2024-03-21

### Fixed

- fix takeoff version.txt path not found error

## [0.0.5] - 2024-03-21

### Added

- add `takeoff version` for checking current cli version and current takeoff image version

### Fixed

- fix the pynvml error is not handled correctly

## [0.0.4] - 2024-03-19

### Fixed

- fix the missing dependency yaml

## [0.0.3] - 2024-03-19

### Fixed

- fix the issue that cannot start with cached license key

## [0.0.2] - 2024-03-19

### Changed

- push takeoff_launcher to pypi

## [0.0.1] - 2024-03-19

- initial release

<!-- Links -->

[keep a changelog]: https://keepachangelog.com/en/1.0.0/
[semantic versioning]: https://semver.org/spec/v2.0.0.html
