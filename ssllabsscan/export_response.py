"""
Helper script for exporting a response from a request to https://api.ssllabs.com/api/v3/analyze
"""
import json
from os.path import dirname, join, realpath

import requests

API_URL = "https://api.ssllabs.com/api/v3/analyze"
OUTPUT_DIR = join(dirname(realpath(__file__)), "tests")


def export_response(host, output_file):
    payload = {
        "host": host,
        "publish": "off",
        "startNew": "off",
        "all": "done",
        "ignoreMismatch": "on"
    }
    response = requests.get(API_URL, params=payload, verify=True)

    with open(output_file, "w") as f:
        json.dump(response.json(), f, indent=2, sort_keys=False)


export_response("google.com", join(OUTPUT_DIR, "sample_response_ready.json"))
export_response("fakfhaoieunksnkadhao.com", join(OUTPUT_DIR, "sample_response_error.json"))
