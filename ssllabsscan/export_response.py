"""
Helper script for exporting a response from a request to https://api.ssllabs.com/api/v3/analyze
"""

import json

import requests

API_URL = "https://api.ssllabs.com/api/v3/analyze"


def export_response(host, output_file):
    """
    Export SSL Labs API response to a JSON file.

    Args:
        host: The hostname to analyze
        output_file: Path to the output JSON file
    """
    payload = {
        "host": host,
        "publish": "off",
        "startNew": "off",
        "all": "done",
        "ignoreMismatch": "on",
    }
    response = requests.get(API_URL, params=payload, verify=True)

    with open(output_file, "w") as f:
        json.dump(response.json(), f, indent=2, sort_keys=False)
