# Change Log
All notable changes to this project will be documented in this file.

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
