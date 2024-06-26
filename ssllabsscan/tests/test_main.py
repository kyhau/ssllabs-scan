import os

from mock import Mock

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
    output_server_1_json_file
):
    mocked_request_ok_response_sequence = [
        MockHttpResponse(200, sample_dns_response),
        MockHttpResponse(200, sample_in_progress_response),
        MockHttpResponse(200, sample_ready_response)
    ]

    SSLLabsClient.requests_get = Mock(side_effect=mocked_request_ok_response_sequence)

    assert 0 == process(
        sample_input_file,
        email,
        check_progress_interval_secs=1,
        summary_csv=output_summary_csv_file,
        summary_html=output_summary_html_file
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
    output_server_1_json_file
):
    common_tests(
        sample_server_list_file,
        sample_dns_response,
        sample_in_progress_response,
        sample_ready_response,
        email_1,
        output_summary_csv_file,
        output_summary_html_file,
        output_server_1_json_file
    )


def test_main_process_2(
    sample_server_list_file_2,  # input file with empty newlines
    sample_dns_response,
    sample_in_progress_response,
    sample_ready_response,
    email_2,
    output_summary_csv_file,
    output_summary_html_file,
    output_server_1_json_file
):
    common_tests(
        sample_server_list_file_2,
        sample_dns_response,
        sample_in_progress_response,
        sample_ready_response,
        email_2,
        output_summary_csv_file,
        output_summary_html_file,
        output_server_1_json_file
    )
