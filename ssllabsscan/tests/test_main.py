from mock import Mock
import os

from ssllabsscan.main import process
from ssllabsscan.ssllabs_client import SSLLabsClient


def test_process(
        sample_server_list_file, sample_ok_response,
        output_summary_csv_file, output_summary_html_file, output_server_1_json_file
):
    mocked_request_ok_response_sequence = [
        {"status": "DNS"},
        {"status": "IN_PROGRESS"},
        sample_ok_response,
    ]

    SSLLabsClient.request_api = Mock(side_effect=mocked_request_ok_response_sequence)

    assert 0==process(
        sample_server_list_file,
        check_progress_interval_secs=1,
        summary_csv=output_summary_csv_file,
        summary_html=output_summary_html_file
    )

    assert os.path.exists(output_server_1_json_file)
    assert os.path.exists(output_summary_csv_file)
    assert os.path.exists(output_summary_html_file)
