# Change Log
All notable changes to this project will be documented in this file.

4.1.0 - 2025-01-19
==================

### Added
- Community health files: CODE_OF_CONDUCT.md, CONTRIBUTING.md, SECURITY.md, CODEOWNERS
- Issue templates for bug reports and feature requests with structured forms
- .dockerignore for optimized Docker builds
- Snyk security scanning workflow
- Modern Makefile targets: `setup-init`, `format-python`, `lint-python`, `pre-commit`
- Black code formatter for consistent code style

### Changed
- Moved tests from `ssllabsscan/tests/` to root-level `tests/` directory (Python best practice)
- Renamed CI workflow from `build-and-test.yml` to `ci.yml` for consistency
- Updated all Makefile targets to match standard conventions across projects
- Migrated from standalone `mock` package to built-in `unittest.mock`
- Reorganized dependencies: moved flake8 from test to dev dependencies
- Cleaned up pyproject.toml: removed unused dependencies (mock, coverage, pytest-gitignore, setuptools, wheel)
- Improved Dockerfile with two-phase installation and cache cleanup
- Updated LICENSE copyright to 2017-2025 with author name
- Enhanced README with better structure, badges, and documentation
- Modernized all .github workflows with concurrency control
- Simplified .yaml-lint.yml configuration
- Updated dependabot.yml to remove redundant pip ecosystem
- Updated pull request template for better clarity

### Removed
- Unused dependencies: mock, coverage, pytest-gitignore, setuptools, wheel
- Old `ssllabsscan/tests/` directory (moved to root)
- Redundant application-specific patterns from .gitignore

4.0.0 - 2024-10-12
==================

### Added
- Support for Python 3.13
- Makefile for task automation with commands like `make test`, `make build`, `make lint`
- MIGRATION.md guide for transitioning from tox to Poetry

### Changed
- **BREAKING**: Minimum Python version is now 3.11 (dropped 3.9 and 3.10 support)
- Migrated from tox to Poetry for dependency management
- Updated CI/CD workflows to use Poetry and Make commands
- Modernized build system to use PEP 517/518 standards (pyproject.toml only)
- All project configuration consolidated in pyproject.toml
- Updated Dockerfile to use Python 3.13
- All dev dependencies now pinned to exact versions for security

### Removed
- Python 3.9 and 3.10 support (minimum version now 3.11)
- tox.ini (replaced by Poetry + Makefile)
- setup.py (replaced by pyproject.toml)
- requirements-test.txt (replaced by pyproject.toml dev dependencies)
- requirements-build.txt (no longer needed with Poetry)
- constraints.txt (replaced by poetry.lock)
- MANIFEST.in (replaced by include field in pyproject.toml)
- .travis.yml (legacy CI, now using GitHub Actions)

3.1.0 - 2024-04-10
==================

### Changed
- Add IP address to html report (column 2) (#200)


3.0.0 - 2024-04-02
==================

### Changed
- Support Qualys SSLLabs API v4 (#189)
   - The tool uses [API v4](https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v4.md) if you provide your registered email with Qualys SSLLabs via the `--email` argument.
   - The tool uses [API v3](https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v3.md) if you do not specify the `--email` argument. Note that v3 will be being deprecated in 2024 by Qualys.


2.3.0 - 2024-04-01
==================

### Added
- Support Python 3.12

### Changed
- Update code to handle [SSL Labs – Sunsetting DROWN Test](https://notifications.qualys.com/product/2024/03/28/ssl-labs-sunsetting-drown-test) (#195). Now `Vuln Drown` returns `None` in csv and html reports.

## Removed
- No longer support Python 3.8


2.2.0 - 2023-12-13
==================

### Added
- To enable isolation of the installation, a Dockerfile is added to build a container. ([#182](https://github.com/kyhau/ssllabs-scan/pull/182) @reinoud)
- Since the container runs in a different environment, command-line arguments were added to facilitate output files in a different location. The default behaviour and normal usage of the script was not changed. ([#182](https://github.com/kyhau/ssllabs-scan/pull/182) @reinoud)

2.1.0 - 2022-12-13
==================

### Added
- Support Python 3.11

## Removed
- No longer support Python 3.7


2.0.1 - 2022-11-04
==================

### Fixed
- Support empty new lines in the input file.


2.0.0 - 2022-09-03
==================

### Added
- Added a standalone script [ssllabsscan/export_response.py](./ssllabsscan/export_response.py) to export the response payload of a single request to request to https://api.ssllabs.com/api/v3/analyze for a host, in json format.
- Added pull request template [.github/pull_request_template.md](.github/pull_request_template.md).

### Changed
- Retry only for error codes 429 and 529 (https://github.com/kyhau/ssllabs-scan/issues/108)
    - This introduces a change of existing behaviour. Existing approach retries calling the SSL Labs API for a given host when the returned status_code is not 200. This change aims to retry only when errors are related to client request rate or server overloaded, and avoids unnecessary retires on other [expected errors](https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v3.md) or unexpected errors.
- Support handling error code 441 (https://github.com/kyhau/ssllabs-scan/issues/107)
- Updated unit tests to support SSL Labs API v3 (https://github.com/kyhau/ssllabs-scan/issues/109)
- Updated to build and test also with Python 3.10, drop Python 3.6 (https://github.com/kyhau/ssllabs-scan/issues/110).
- Renamed ReleaseNotes.md to CHANGELOG.md.
- Updated [README.md](./README.md) with sample console output.

### Fixed
- Fixed badge link to codecov (default branch changed from `master` to `main` previously) in [README.md](./README.md).

1.1.1 - 2022-03-09
==================
- Fixed README
- Changed the check from IPv6 address to "statusMessage" when deciding to skip uncontactable endpoints (ssllabs_client).

1.1.0 - 2020-12-16
==================
- Added "supportsRc4", "rc4WithModern" and "rc4Only" to the html summary.

1.0.1 - 2020-02-12
==================
- When the API server is overloaded with requests it returns response.status_code 529. In this case request_api()
  should not return the response before the the API accepts the request and status_code 200 is returned.
  Updated `request_api` to retry `max_attempts` at `check_progress_interval_secs` interval.
- Support building/testing with Python 3.8.

1.0.0 - 2019-03-12
==================
- Support only Python >= 3.6.
- Add report column "TLS 1.3".

0.2.0 - 2018-02-12
==================
- Add a column for certificate expiry date to the reports.


0.1.0 - 2017-02-02
==================
- Initial version of SSL Labs scanning and reporting
