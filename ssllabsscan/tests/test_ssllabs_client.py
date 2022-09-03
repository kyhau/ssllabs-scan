import os

import pytest
from mock import Mock
from ssllabsscan.ssllabs_client import SSLLabsClient

SAMPLE_DNS_RESPONSE = {"status": "DNS", "statusMessage": "Resolving domain names"}
SAMPLE_INPROGRESS_RESPONSE = {"status": "IN_PROGRESS"}
SAMPLE_UNABLE_TO_RESOLVE_DOMAIN_RESPONSE = {"status": "ERROR", "statusMessage": "Unable to resolve domain name"}


class MockHttpResponse:
    def __init__(self, status_code, data) -> None:
        self.data = data
        self.status_code = status_code

    def json(self):
        return dict(self.data)


def test_ssl_labs_client_analyze(sample_ok_response, output_summary_csv_file, output_server_1_json_file):
    mocked_request_ok_response_sequence = [
        MockHttpResponse(200, SAMPLE_DNS_RESPONSE),
        MockHttpResponse(200, SAMPLE_INPROGRESS_RESPONSE),
        MockHttpResponse(200, sample_ok_response)
    ]

    client = SSLLabsClient(check_progress_interval_secs=1)
    client.request_api = Mock(side_effect=mocked_request_ok_response_sequence)

    client.analyze(host=sample_ok_response["host"], summary_csv_file=output_summary_csv_file)

    assert os.path.exists(output_server_1_json_file)
    assert os.path.exists(output_summary_csv_file)


def test_ssl_labs_client_start_new_scan_valid_url(sample_ok_response):
    """Case 1: valid server url"""

    mocked_request_ok_response_sequence = [
        MockHttpResponse(200, SAMPLE_DNS_RESPONSE),
        MockHttpResponse(200, SAMPLE_INPROGRESS_RESPONSE),
        MockHttpResponse(200, sample_ok_response)
    ]

    client1 = SSLLabsClient(check_progress_interval_secs=1)
    client1.request_api = Mock(side_effect=mocked_request_ok_response_sequence)

    ret = client1.start_new_scan(host=sample_ok_response["host"])
    assert ret["status"] == "READY"
    assert ret["host"] == sample_ok_response["host"]
    assert ret["endpoints"][0]["grade"]


def test_ssl_labs_client_start_new_scan_invalid_url(sample_ok_response):
    """Case 2: unable to resolve domain name"""
    mocked_request_err_response_sequence = [
        MockHttpResponse(200, SAMPLE_DNS_RESPONSE),
        MockHttpResponse(200, SAMPLE_UNABLE_TO_RESOLVE_DOMAIN_RESPONSE)
    ]

    client2 = SSLLabsClient(check_progress_interval_secs=1)
    client2.request_api = Mock(side_effect=mocked_request_err_response_sequence)

    ret = client2.start_new_scan(host="example2.com")
    assert ret["status"] == "ERROR"
    assert ret["statusMessage"] == "Unable to resolve domain name"


def test_ssl_labs_client_start_new_scan_unexpected_error_code():
    # Case 3: received error codes other than the supported one
    mocked_request_err_response_sequence = [
        MockHttpResponse(200, SAMPLE_DNS_RESPONSE),
        MockHttpResponse(200, SAMPLE_INPROGRESS_RESPONSE),
        MockHttpResponse(441, {"status": "ERROR", "statusMessage": "some error"})
    ]

    client3 = SSLLabsClient(check_progress_interval_secs=1)
    client3.requests_get = Mock(side_effect=mocked_request_err_response_sequence)

    ret = client3.start_new_scan(host="example3.com")
    assert ret["status"] == "ERROR"
    assert ret["statusMessage"] == "some error"


@pytest.mark.parametrize(
    ("time"),
    [
        # 10 digit epoch timestamp
        1521257378,
        # 13 digit epoch timestamp with milliseconds
        1521257378000,
        # 10 digit epoch timestamp string
        "1521257378",
    ],
    ids=[
        "10_digit_timestamp",
        "13_digit_timestamp",
        "10_digit_timestamp_string",
    ],
)
def a_test_prepare_datetime(time):
    """Test that SSLLabsClient.prepare_datetime works as expected."""
    assert SSLLabsClient().prepare_datetime(time) == "2018-03-17"
