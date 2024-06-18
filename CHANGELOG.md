# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]
### Added
- add switch for verbosity of output
- allow to pipe text into the CLI via stdin
### Changed
- rename transformation 'i' (imitation) to 'p' (persona), for consistency with -p flag

## [0.3.0] - 2024-02-20
### Added
- add transformation for imitation
### Changed
- use structural pattern matching at applying transformations

## [0.2.0] - 2024-02-11
### Added
- make URL to model API configurable
- make configurable which LLM to use
### Fixed
- fix and document tests
- complete docstrings

## [0.1.0] - 2024-02-11
### Added
- first MVP with fixed model, transformations 'thesaurus' and 'simplify'
