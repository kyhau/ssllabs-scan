import os

import pytest
from mock import Mock

from ssllabsscan.ssllabs_client import SSLLabsClient

from .conftest import MockHttpResponse

SAMPLE_UNABLE_TO_RESOLVE_DOMAIN_RESPONSE = {"status": "ERROR", "statusMessage": "Unable to resolve domain name"}


def test_ssl_labs_client_analyze(
    sample_dns_response,
    sample_in_progress_response,
    sample_ready_response,
    email_1,
    output_summary_csv_file,
    output_server_1_json_file
):
    mocked_request_ok_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, sample_in_progress_response),
        MockHttpResponse(200, sample_ready_response)
    ]

    client = SSLLabsClient(email=email_1, check_progress_interval_secs=1)
    client.requests_get = Mock(side_effect=mocked_request_ok_response_sequence)

    client.analyze(host=sample_ready_response["host"], summary_csv_file=output_summary_csv_file)

    assert os.path.exists(output_server_1_json_file)
    assert os.path.exists(output_summary_csv_file)


def test_ssl_labs_client_start_new_scan_valid_url(
    sample_dns_response,
    sample_in_progress_response,
    sample_ready_response,
    email_1
):
    """Case 1: valid server url"""

    mocked_request_ok_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, sample_in_progress_response),
        MockHttpResponse(200, sample_ready_response)
    ]

    client1 = SSLLabsClient(email=email_1, check_progress_interval_secs=1)
    client1.requests_get = Mock(side_effect=mocked_request_ok_response_sequence)

    ret = client1.start_new_scan(host=sample_ready_response["host"])
    assert ret["status"] == "READY"
    assert ret["host"] == sample_ready_response["host"]
    assert ret["endpoints"][0]["grade"]


def test_ssl_labs_client_start_new_scan_invalid_url(sample_dns_response, email_1):
    """Case 2: unable to resolve domain name"""
    mocked_request_err_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, SAMPLE_UNABLE_TO_RESOLVE_DOMAIN_RESPONSE)
    ]

    client2 = SSLLabsClient(email=email_1, check_progress_interval_secs=1)
    client2.requests_get = Mock(side_effect=mocked_request_err_response_sequence)

    ret = client2.start_new_scan(host="example2.com")
    assert ret["status"] == "ERROR"
    assert ret["statusMessage"] == "Unable to resolve domain name"


def test_ssl_labs_client_start_new_scan_unexpected_error_code(
    sample_dns_response,
    sample_in_progress_response,
    email_1
):
    # Case 3: received error codes other than the supported one
    mocked_request_err_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, sample_in_progress_response),
        MockHttpResponse(441, {"status": "ERROR", "statusMessage": "some error"})
    ]

    client3 = SSLLabsClient(email=email_1, check_progress_interval_secs=1)
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
