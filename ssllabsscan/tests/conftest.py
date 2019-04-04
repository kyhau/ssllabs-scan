"""
conftest.py for testing
"""
import os
import pytest
from shutil import rmtree
from tempfile import mkdtemp


SAMPLE_OK_RESPONSE = {
    "status": "READY",
    "protocol": "HTTP",
    "host": "example.com",
    "endpoints": [
        {
            "grade": "A+",
            "hasWarnings": False,
            "details": {
                "freak": False,
                "poodleTls": 1,
                "openSSLLuckyMinus20": 1,
                "openSslCcs": 1,
                "chain": {
                    "issues": 16,
                },
                "poodle": False,
                "drownVulnerable": False,
                "vulnBeast": False,
                "heartbleed": False,
                "supportsRc4": False,
                "protocols": [
                    {
                        "version": "1.2",
                        "id": 771,
                        "name": "TLS"
                    }
                ],
                "forwardSecrecy": 4,
                "heartbeat": True,
                "cert": {
                    "notAfter": 1521257378000,
                }
            },
        }
    ],
    "port": 443
}


@pytest.fixture(scope="function")
def sample_ok_response():
    return SAMPLE_OK_RESPONSE


@pytest.fixture(scope='session')
def unit_tests_tmp_output_dir(request):
    """
    Create a tmp directory for running tests and will be deleted at the end of the testing.
    Return the full path dirname
    """
    t = mkdtemp(prefix='test_ssl_labs_scan')
    print('Created tmp test dir {}.'.format(t))

    def teardown():
        # delete tmp test dir
        if os.path.exists(t):
            rmtree(t)
            print('Deleted tmp test dir {}.'.format(t))

    request.addfinalizer(teardown)
    return t


@pytest.fixture(scope='session')
def sample_server_list_file(unit_tests_tmp_output_dir):
    """
    Create a sample server_list file in the tmp unit tests file.
    Return the full path filename
    """
    server_list_file = os.path.join(unit_tests_tmp_output_dir, "test_server_list.txt")
    with open(server_list_file, 'w') as outfile:
        outfile.write("example.com\n")
    return server_list_file


@pytest.fixture(scope='session')
def output_summary_csv_file(unit_tests_tmp_output_dir):
    return os.path.join(unit_tests_tmp_output_dir, 'test_summary.csv')


@pytest.fixture(scope='session')
def output_summary_html_file(unit_tests_tmp_output_dir):
    return os.path.join(unit_tests_tmp_output_dir, 'test_summary.html')

@pytest.fixture(scope='session')
def output_server_1_json_file(unit_tests_tmp_output_dir):
    return os.path.join(unit_tests_tmp_output_dir, 'example.com.json')
