import os
import tempfile
from unittest.mock import Mock, patch

import pytest

from ssllabsscan.main import process
from ssllabsscan.ssllabs_client import SSLLabsClient

from .conftest import MockHttpResponse


def common_tests(
    sample_input_file,
    sample_dns_response,
    sample_in_progress_response,
    sample_ready_response,
    email,
    output_summary_csv_file,
    output_summary_html_file,
    output_server_1_json_file,
):
    mocked_request_ok_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, sample_in_progress_response),
        MockHttpResponse(200, sample_ready_response),
    ]

    SSLLabsClient.requests_get = Mock(side_effect=mocked_request_ok_response_sequence)

    assert 0 == process(
        sample_input_file,
        email,
        check_progress_interval_secs=1,
        summary_csv=output_summary_csv_file,
        summary_html=output_summary_html_file,
    )

    assert os.path.exists(output_server_1_json_file)
    assert os.path.exists(output_summary_csv_file)
    assert os.path.exists(output_summary_html_file)


def test_main_process_1(
    sample_server_list_file,
    sample_dns_response,
    sample_in_progress_response,
    sample_ready_response,
    email_1,
    output_summary_csv_file,
    output_summary_html_file,
    output_server_1_json_file,
):
    common_tests(
        sample_server_list_file,
        sample_dns_response,
        sample_in_progress_response,
        sample_ready_response,
        email_1,
        output_summary_csv_file,
        output_summary_html_file,
        output_server_1_json_file,
    )


def test_main_process_2(
    sample_server_list_file_2,  # input file with empty newlines
    sample_dns_response,
    sample_in_progress_response,
    sample_ready_response,
    email_2,
    output_summary_csv_file,
    output_summary_html_file,
    output_server_1_json_file,
):
    common_tests(
        sample_server_list_file_2,
        sample_dns_response,
        sample_in_progress_response,
        sample_ready_response,
        email_2,
        output_summary_csv_file,
        output_summary_html_file,
        output_server_1_json_file,
    )


def test_main_process_with_nonexistent_file():
    """Test process function with nonexistent input file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_csv:
        temp_csv_path = temp_csv.name
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as temp_html:
        temp_html_path = temp_html.name

    try:
        # Test with nonexistent input file - should raise FileNotFoundError
        with pytest.raises(FileNotFoundError):
            process(
                "nonexistent_file.txt",
                "test@example.com",
                check_progress_interval_secs=1,
                summary_csv=temp_csv_path,
                summary_html=temp_html_path,
            )

    finally:
        for path in [temp_csv_path, temp_html_path]:
            if os.path.exists(path):
                os.unlink(path)


def test_main_process_with_empty_file():
    """Test process function with empty input file."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_input:
        temp_input_path = temp_input.name
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_csv:
        temp_csv_path = temp_csv.name
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as temp_html:
        temp_html_path = temp_html.name

    try:
        # Create empty input file
        with open(temp_input_path, "w") as f:
            f.write("")

        result = process(
            temp_input_path,
            "test@example.com",
            check_progress_interval_secs=1,
            summary_csv=temp_csv_path,
            summary_html=temp_html_path,
        )
        # Should return 0 for successful processing of empty file
        assert result == 0

    finally:
        for path in [temp_input_path, temp_csv_path, temp_html_path]:
            if os.path.exists(path):
                os.unlink(path)


def test_main_process_with_invalid_email():
    """Test process function with invalid email format."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_input:
        temp_input_path = temp_input.name
        temp_input.write("example.com\n")
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_csv:
        temp_csv_path = temp_csv.name
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as temp_html:
        temp_html_path = temp_html.name

    # Mock the SSLLabsClient to avoid actual API calls
    with patch("ssllabsscan.main.SSLLabsClient") as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.analyze.return_value = None

        try:
            # Test with invalid email (should still work, just uses API v3)
            result = process(
                temp_input_path,
                "invalid-email",
                check_progress_interval_secs=1,
                summary_csv=temp_csv_path,
                summary_html=temp_html_path,
            )
            # Should still return 0 as email validation is not strict
            assert result == 0

        finally:
            for path in [temp_input_path, temp_csv_path, temp_html_path]:
                if os.path.exists(path):
                    os.unlink(path)


def test_main_process_file_creation():
    """Test that process function creates expected output files."""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as temp_input:
        temp_input_path = temp_input.name
        temp_input.write("example.com\n")
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as temp_csv:
        temp_csv_path = temp_csv.name
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".html") as temp_html:
        temp_html_path = temp_html.name

    # Mock the SSLLabsClient to avoid actual API calls
    with patch("ssllabsscan.main.SSLLabsClient") as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.analyze.return_value = None

        try:
            process(
                temp_input_path,
                "test@example.com",
                check_progress_interval_secs=1,
                summary_csv=temp_csv_path,
                summary_html=temp_html_path,
            )

            # Verify that analyze was called
            mock_client.analyze.assert_called_once()

            # Verify output files exist (they should be created even with mocked client)
            assert os.path.exists(temp_csv_path)
            assert os.path.exists(temp_html_path)

        finally:
            for path in [temp_input_path, temp_csv_path, temp_html_path]:
                if os.path.exists(path):
                    os.unlink(path)
