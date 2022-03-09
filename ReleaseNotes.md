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
