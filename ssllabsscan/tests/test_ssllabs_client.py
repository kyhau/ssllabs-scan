from mock import Mock
import os

from ssllabsscan.ssllabs_client import SSLLabsClient


def test_ssl_labs_client_analyze(sample_ok_response, output_summary_csv_file, output_server_1_json_file):
    mocked_request_ok_response_sequence = [
        {"status": "DNS"},
        {"status": "IN_PROGRESS"},
        sample_ok_response,
    ]

    client = SSLLabsClient(check_progress_interval_secs=1)
    client.request_api = Mock(side_effect=mocked_request_ok_response_sequence)

    client.analyze(host=sample_ok_response["host"], summary_csv_file=output_summary_csv_file)

    assert os.path.exists(output_server_1_json_file)
    assert os.path.exists(output_summary_csv_file)


def test_ssl_labs_client_start_new_scan(sample_ok_response):

    # Case 1: valid server url
    mocked_request_ok_response_sequence = [
        {"status": "DNS"},
        {"status": "IN_PROGRESS"},
        sample_ok_response,
    ]

    client1 = SSLLabsClient(check_progress_interval_secs=1)
    client1.request_api = Mock(side_effect=mocked_request_ok_response_sequence)

    ret = client1.start_new_scan(host=sample_ok_response["host"])
    assert ret["status"] == "READY"
    assert ret["host"] == sample_ok_response["host"]
    assert ret["endpoints"][0]["grade"]

    # Case 2: invalid server url
    mocked_request_err_response_sequence = [
        {"status": "DNS"},
        {"status": "ERROR"},
    ]

    client2 = SSLLabsClient(check_progress_interval_secs=1)
    client2.request_api = Mock(side_effect=mocked_request_err_response_sequence)

    ret = client2.start_new_scan(host="example2.com")
    assert ret["status"] == "ERROR"
