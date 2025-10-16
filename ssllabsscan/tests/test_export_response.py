import json
import os
import tempfile
from unittest.mock import Mock, patch

import pytest
import requests

from ssllabsscan.export_response import export_response


class TestExportResponse:
    """Test cases for export_response module."""

    def test_export_response_success(self):
        """Test successful response export."""
        mock_response_data = {
            "host": "example.com",
            "status": "READY",
            "endpoints": [{"grade": "A"}]
        }

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data

        with patch('ssllabsscan.export_response.requests.get') as mock_get:
            mock_get.return_value = mock_response

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                temp_file_path = temp_file.name

            try:
                export_response("example.com", temp_file_path)

                # Verify requests.get was called with correct parameters
                mock_get.assert_called_once()
                call_args = mock_get.call_args
                assert call_args[0][0] == "https://api.ssllabs.com/api/v3/analyze"
                assert call_args[1]['params']['host'] == "example.com"
                assert call_args[1]['params']['publish'] == "off"
                assert call_args[1]['params']['startNew'] == "off"
                assert call_args[1]['params']['all'] == "done"
                assert call_args[1]['params']['ignoreMismatch'] == "on"
                assert call_args[1]['verify'] is True

                # Verify file was created and contains correct data
                assert os.path.exists(temp_file_path)
                with open(temp_file_path, 'r') as f:
                    saved_data = json.load(f)
                assert saved_data == mock_response_data

            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

    def test_export_response_file_creation(self):
        """Test that export_response creates the file correctly."""
        mock_response_data = {"test": "data"}
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data

        with patch('ssllabsscan.export_response.requests.get') as mock_get:
            mock_get.return_value = mock_response

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                temp_file_path = temp_file.name

            try:
                export_response("test.com", temp_file_path)

                # Verify file exists and has correct content
                assert os.path.exists(temp_file_path)
                with open(temp_file_path, 'r') as f:
                    content = f.read()
                assert '"test": "data"' in content

            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

    def test_export_response_json_formatting(self):
        """Test that JSON is properly formatted with indent and sort_keys=False."""
        mock_response_data = {"z": 1, "a": 2}
        mock_response = Mock()
        mock_response.json.return_value = mock_response_data

        with patch('ssllabsscan.export_response.requests.get') as mock_get:
            mock_get.return_value = mock_response

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                temp_file_path = temp_file.name

            try:
                export_response("test.com", temp_file_path)

                with open(temp_file_path, 'r') as f:
                    content = f.read()

                # Should have indentation (spaces)
                assert '  ' in content
                # Should preserve original key order (z before a)
                assert content.find('"z"') < content.find('"a"')

            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

    def test_export_response_requests_exception(self):
        """Test handling of requests exceptions."""
        with patch('ssllabsscan.export_response.requests.get') as mock_get:
            mock_get.side_effect = requests.RequestException("Network error")

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                temp_file_path = temp_file.name

            try:
                with pytest.raises(requests.RequestException):
                    export_response("test.com", temp_file_path)

            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)

    def test_export_response_json_exception(self):
        """Test handling of JSON parsing exceptions."""
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

        with patch('ssllabsscan.export_response.requests.get') as mock_get:
            mock_get.return_value = mock_response

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
                temp_file_path = temp_file.name

            try:
                with pytest.raises(json.JSONDecodeError):
                    export_response("test.com", temp_file_path)

            finally:
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
