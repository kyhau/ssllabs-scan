import os
from unittest.mock import Mock, patch

import pytest

from ssllabsscan.ssllabs_client import SSLLabsClient

from .conftest import MockHttpResponse

SAMPLE_UNABLE_TO_RESOLVE_DOMAIN_RESPONSE = {
    "status": "ERROR",
    "statusMessage": "Unable to resolve domain name",
}


def test_ssl_labs_client_analyze(
    sample_dns_response,
    sample_in_progress_response,
    sample_ready_response,
    email_1,
    output_summary_csv_file,
    output_server_1_json_file,
):
    mocked_request_ok_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, sample_in_progress_response),
        MockHttpResponse(200, sample_ready_response),
    ]

    client = SSLLabsClient(email=email_1, check_progress_interval_secs=1)
    with patch.object(client, "requests_get", side_effect=mocked_request_ok_response_sequence):
        client.analyze(host=sample_ready_response["host"], summary_csv_file=output_summary_csv_file)

        assert os.path.exists(output_server_1_json_file)
        assert os.path.exists(output_summary_csv_file)


def test_ssl_labs_client_start_new_scan_valid_url(
    sample_dns_response, sample_in_progress_response, sample_ready_response, email_1
):
    """Case 1: valid server url"""

    mocked_request_ok_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, sample_in_progress_response),
        MockHttpResponse(200, sample_ready_response),
    ]

    client1 = SSLLabsClient(email=email_1, check_progress_interval_secs=1)
    with patch.object(client1, "requests_get", side_effect=mocked_request_ok_response_sequence):
        ret = client1.start_new_scan(host=sample_ready_response["host"])
        assert ret["status"] == "READY"
        assert ret["host"] == sample_ready_response["host"]
        assert ret["endpoints"][0]["grade"]


def test_ssl_labs_client_start_new_scan_invalid_url(sample_dns_response, email_1):
    """Case 2: unable to resolve domain name"""
    mocked_request_err_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, SAMPLE_UNABLE_TO_RESOLVE_DOMAIN_RESPONSE),
    ]

    client2 = SSLLabsClient(email=email_1, check_progress_interval_secs=1)
    with patch.object(client2, "requests_get", side_effect=mocked_request_err_response_sequence):
        ret = client2.start_new_scan(host="example2.com")
        assert ret["status"] == "ERROR"
        assert ret["statusMessage"] == "Unable to resolve domain name"


def test_ssl_labs_client_start_new_scan_unexpected_error_code(
    sample_dns_response, sample_in_progress_response, email_1
):
    # Case 3: received error codes other than the supported one
    mocked_request_err_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, sample_in_progress_response),
        MockHttpResponse(441, {"status": "ERROR", "statusMessage": "some error"}),
    ]

    client3 = SSLLabsClient(email=email_1, check_progress_interval_secs=1)
    with patch.object(client3, "requests_get", side_effect=mocked_request_err_response_sequence):
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
def test_prepare_datetime(time):
    """Test that SSLLabsClient.prepare_datetime works as expected."""
    assert SSLLabsClient.prepare_datetime(time) == "2018-03-17"


def test_prepare_datetime_edge_cases():
    """Test edge cases for prepare_datetime function."""
    # Test with very large timestamp
    large_timestamp = 9999999999  # Year 2286
    result = SSLLabsClient.prepare_datetime(large_timestamp)
    assert result == "2286-11-20"

    # Test with very small timestamp
    small_timestamp = 1000000000  # Year 2001
    result = SSLLabsClient.prepare_datetime(small_timestamp)
    assert result == "2001-09-09"

    # Test with float timestamp
    float_timestamp = 1521257378.5
    result = SSLLabsClient.prepare_datetime(float_timestamp)
    assert result == "2018-03-17"


def test_ssl_labs_client_initialization():
    """Test SSLLabsClient initialization with different parameters."""
    # Test with email
    client1 = SSLLabsClient(email="test@example.com")
    assert client1.email == "test@example.com"
    assert client1._check_progress_interval_secs == 30  # default

    # Test with custom interval
    client2 = SSLLabsClient(email="test@example.com", check_progress_interval_secs=5)
    assert client2.email == "test@example.com"
    assert client2._check_progress_interval_secs == 5

    # Test with both parameters
    client3 = SSLLabsClient(email="test@example.com", check_progress_interval_secs=10)
    assert client3.email == "test@example.com"
    assert client3._check_progress_interval_secs == 10


def test_ssl_labs_client_append_summary_csv():
    """Test append_summary_csv method."""
    import os
    import tempfile

    client = SSLLabsClient(email="test@example.com")

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_file:
        temp_file_path = temp_file.name

    try:
        # Test data with all required fields
        host = "example.com"
        data = {
            "certs": [{"notAfter": 1521257378}],
            "endpoints": [
                {
                    "grade": "A",
                    "ipAddress": "1.2.3.4",
                    "hasWarnings": False,
                    "details": {
                        "certChains": [{"issues": 0}],
                        "forwardSecrecy": 4,
                        "heartbeat": True,
                        "vulnBeast": False,
                        "drownVulnerable": False,
                        "heartbleed": False,
                        "freak": False,
                        "openSslCcs": 0,
                        "openSSLLuckyMinus20": 0,
                        "poodle": False,
                        "poodleTls": 0,
                        "supportsRc4": False,
                        "rc4WithModern": False,
                        "rc4Only": False,
                        "protocols": [
                            {"name": "TLS", "version": "1.3"},
                            {"name": "TLS", "version": "1.2"},
                        ],
                    },
                }
            ],
        }

        # Call the method
        client.append_summary_csv(temp_file_path, host, data)

        # Verify file was created and contains expected content
        assert os.path.exists(temp_file_path)
        with open(temp_file_path, "r") as f:
            content = f.read()
            assert host in content
            assert "2018-03-17" in content  # from prepare_datetime
            assert "A" in content
            assert "1.2.3.4" in content

    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_ssl_labs_client_requests_get_with_email():
    """Test requests_get method with email (API v4)."""
    client = SSLLabsClient(email="test@example.com")

    with patch.object(client, "requests_get") as mock_requests_get:
        mock_response = Mock()
        mock_response.json.return_value = {"status": "READY"}
        mock_requests_get.return_value = mock_response

        payload = {"host": "example.com"}
        client.requests_get(payload)

        # Verify the method was called with the payload
        mock_requests_get.assert_called_once_with(payload)


def test_ssl_labs_client_requests_get_without_email():
    """Test requests_get method without email (API v3)."""
    client = SSLLabsClient(email=None)

    with patch.object(client, "requests_get") as mock_requests_get:
        mock_response = Mock()
        mock_response.json.return_value = {"status": "READY"}
        mock_requests_get.return_value = mock_response

        payload = {"host": "example.com"}
        client.requests_get(payload)

        # Verify the method was called with the payload
        mock_requests_get.assert_called_once_with(payload)


def test_ssl_labs_client_analyze_with_error_status(email_1, output_summary_csv_file):
    """Test analyze() when start_new_scan returns ERROR status."""
    client = SSLLabsClient(email=email_1, check_progress_interval_secs=1)

    error_response = {"status": "ERROR", "statusMessage": "Unable to resolve domain name"}

    with patch.object(client, "start_new_scan", return_value=error_response):
        # analyze() should return early without creating files
        client.analyze(host="bad-domain.com", summary_csv_file=output_summary_csv_file)

        # Verify no JSON file was created
        assert not os.path.exists(
            os.path.join(os.path.dirname(output_summary_csv_file), "bad-domain.com.json")
        )


def test_ssl_labs_client_request_api_retry_429():
    """Test request_api() retry logic for 429 status code."""
    client = SSLLabsClient(email="test@example.com", check_progress_interval_secs=1, max_attempts=3)

    # First two requests return 429, third returns 200
    mock_responses = [
        MockHttpResponse(429, {"status": "ERROR", "statusMessage": "Rate limit exceeded"}),
        MockHttpResponse(429, {"status": "ERROR", "statusMessage": "Rate limit exceeded"}),
        MockHttpResponse(200, {"status": "READY", "statusMessage": "Ready"}),
    ]

    with patch.object(client, "requests_get", side_effect=mock_responses):
        payload = {"host": "example.com"}
        response = client.request_api(payload)

        # Should return the successful response after retries
        assert response.status_code == 200
        assert response.json()["status"] == "READY"


def test_ssl_labs_client_request_api_retry_529():
    """Test request_api() retry logic for 529 status code."""
    client = SSLLabsClient(email="test@example.com", check_progress_interval_secs=1, max_attempts=3)

    # First request returns 529, second returns 200
    mock_responses = [
        MockHttpResponse(529, {"status": "ERROR", "statusMessage": "Service overloaded"}),
        MockHttpResponse(200, {"status": "READY", "statusMessage": "Ready"}),
    ]

    with patch.object(client, "requests_get", side_effect=mock_responses):
        payload = {"host": "example.com"}
        response = client.request_api(payload)

        # Should return the successful response after retry
        assert response.status_code == 200
        assert response.json()["status"] == "READY"


def test_ssl_labs_client_request_api_max_attempts_exceeded():
    """Test request_api() when max attempts are exceeded."""
    client = SSLLabsClient(email="test@example.com", check_progress_interval_secs=1, max_attempts=2)

    # All requests return 429
    mock_responses = [
        MockHttpResponse(429, {"status": "ERROR", "statusMessage": "Rate limit exceeded"}),
        MockHttpResponse(429, {"status": "ERROR", "statusMessage": "Rate limit exceeded"}),
        MockHttpResponse(429, {"status": "ERROR", "statusMessage": "Rate limit exceeded"}),
    ]

    with patch.object(client, "requests_get", side_effect=mock_responses):
        payload = {"host": "example.com"}
        response = client.request_api(payload)

        # Should return the error response after max attempts
        assert response.status_code == 429


def test_ssl_labs_client_append_summary_csv_skip_unable_endpoints():
    """Test append_summary_csv() skips endpoints with 'Unable' in statusMessage."""
    import tempfile

    client = SSLLabsClient(email="test@example.com")

    # Create a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_file:
        temp_file_path = temp_file.name

    try:
        host = "example.com"
        data = {
            "certs": [{"notAfter": 1521257378}],
            "endpoints": [
                {
                    "ipAddress": "1.2.3.4",
                    "statusMessage": "Unable to connect to the server",
                    "grade": "A",
                    "hasWarnings": False,
                    "details": {
                        "certChains": [{"issues": 0}],
                        "forwardSecrecy": 4,
                        "heartbeat": True,
                        "vulnBeast": False,
                        "drownVulnerable": False,
                        "heartbleed": False,
                        "freak": False,
                        "openSslCcs": 0,
                        "openSSLLuckyMinus20": 0,
                        "poodle": False,
                        "poodleTls": 0,
                        "supportsRc4": False,
                        "rc4WithModern": False,
                        "rc4Only": False,
                        "protocols": [{"name": "TLS", "version": "1.3"}],
                    },
                },
                {
                    "ipAddress": "5.6.7.8",
                    "statusMessage": "Ready",
                    "grade": "B",
                    "hasWarnings": True,
                    "details": {
                        "certChains": [{"issues": 0}],
                        "forwardSecrecy": 2,
                        "heartbeat": False,
                        "vulnBeast": True,
                        "drownVulnerable": True,
                        "heartbleed": True,
                        "freak": True,
                        "openSslCcs": 1,
                        "openSSLLuckyMinus20": 1,
                        "poodle": True,
                        "poodleTls": 1,
                        "supportsRc4": True,
                        "rc4WithModern": True,
                        "rc4Only": True,
                        "protocols": [{"name": "TLS", "version": "1.2"}],
                    },
                },
            ],
        }

        # Call the method
        client.append_summary_csv(temp_file_path, host, data)

        # Verify file was created
        assert os.path.exists(temp_file_path)
        with open(temp_file_path, "r") as f:
            content = f.read()
            # First endpoint should be skipped (has "Unable")
            assert "1.2.3.4" not in content
            # Second endpoint should be included
            assert "5.6.7.8" in content
            assert "B" in content

    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


def test_ssl_labs_client_print_msg_debug():
    """Test print_msg() with DEBUG message type."""
    client = SSLLabsClient(email="test@example.com")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "READY", "statusMessage": "Scan complete"}

    # Capture logging output
    with patch("logging.info") as mock_logging:
        client.print_msg(mock_response, "DEBUG")
        mock_logging.assert_called_once()


def test_ssl_labs_client_print_msg_wait_for_complete():
    """Test print_msg() with WAIT_FOR_COMPLETE message type."""
    client = SSLLabsClient(email="test@example.com", check_progress_interval_secs=5)

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "IN_PROGRESS", "statusMessage": "Processing"}

    # Capture print output
    with patch("builtins.print") as mock_print:
        client.print_msg(mock_response, "WAIT_FOR_COMPLETE")
        mock_print.assert_called_once()
        # Check that interval is mentioned in message
        assert "5 secs" in mock_print.call_args[0][0]


def test_ssl_labs_client_print_msg_wait_for_retry():
    """Test print_msg() with WAIT_FOR_RETRY message type."""
    client = SSLLabsClient(email="test@example.com")

    mock_response = Mock()
    mock_response.status_code = 429
    mock_response.json.return_value = {"status": "ERROR", "statusMessage": "Rate limit exceeded"}

    # Capture print output
    with patch("builtins.print") as mock_print:
        client.print_msg(mock_response, "WAIT_FOR_RETRY")
        mock_print.assert_called_once()
        assert "429" in mock_print.call_args[0][0]


def test_ssl_labs_client_print_msg_failed_and_skipped():
    """Test print_msg() with FAILED_AND_SKIPPED message type."""
    client = SSLLabsClient(email="test@example.com")

    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.json.return_value = {"status": "ERROR", "statusMessage": "Internal error"}

    # Capture print output
    with patch("builtins.print") as mock_print:
        client.print_msg(mock_response, "FAILED_AND_SKIPPED", host="example.com")
        mock_print.assert_called_once()
        import re

        assert re.search(
            r"(?<!\w)example\.com(?!\w)", mock_print.call_args[0][0]
        ), "example.com should appear as an exact host in output"
        assert "500" in mock_print.call_args[0][0]
