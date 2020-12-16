"""
See API doc: https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs.md
"""
import json
import os
import time
from datetime import datetime

import requests

API_URL = "https://api.ssllabs.com/api/v2/analyze"

CHAIN_ISSUES = {
    "0": "none",
    "1": "unused",
    "2": "incomplete chain",
    "3": "chain contains unrelated or duplicate certificates",
    "4": "the certificates form a chain (trusted or not) but incorrect order",
    "16": "contains a self-signed root certificate",
    "32": "the certificates form a chain but cannot be validated",
}

# Forward secrecy protects past sessions against future compromises of secret keys or passwords.
FORWARD_SECRECY = {
    "1": "With some browsers WEAK",
    "2": "With modern browsers",
    "4": "Yes (with most browsers) ROBUST",
}

PROTOCOLS = [
    "TLS 1.3", "TLS 1.2", "TLS 1.1", "TLS 1.0", "SSL 3.0 INSECURE", "SSL 2.0 INSECURE"
]

RC4 = ["Support RC4", "RC4 with modern protocols", "RC4 Only"]

VULNERABLES = [
    "Vuln Beast", "Vuln Drown", "Vuln Heartbleed", "Vuln FREAK",
    "Vuln openSsl Ccs", "Vuln openSSL LuckyMinus20", "Vuln POODLE", "Vuln POODLE TLS"
]

SUMMARY_COL_NAMES = [
    "Host", "Grade", "HasWarnings", "Cert Expiry", "Chain Status", "Forward Secrecy", "Heartbeat ext"
] + VULNERABLES + RC4 + PROTOCOLS


class SSLLabsClient():
    def __init__(self, check_progress_interval_secs=30, max_attempts=100):
        self._check_progress_interval_secs = check_progress_interval_secs
        self._max_attempts = max_attempts

    def analyze(self, host, summary_csv_file):
        data = self.start_new_scan(host=host)

        # write the output to file
        json_file = os.path.join(os.path.dirname(summary_csv_file), f"{host}.json")
        with open(json_file, "w") as outfile:
            json.dump(data, outfile, indent=2)

        # write the summary to file
        self.append_summary_csv(summary_csv_file, host, data)

    def start_new_scan(self, host, publish="off", startNew="on", all="done", ignoreMismatch="on"):
        path = API_URL
        payload = {
            "host": host,
            "publish": publish,
            "startNew": startNew,
            "all": all,
            "ignoreMismatch": ignoreMismatch
        }
        results = self.request_api(path, payload)
        payload.pop("startNew")

        while results["status"] != "READY" and results["status"] != "ERROR":
            print(f"Status: {results['status']}, wait for {self._check_progress_interval_secs} seconds...")
            time.sleep(self._check_progress_interval_secs)
            results = self.request_api(path, payload)
        return results

    def request_api(self, url, payload):
        response = requests.get(url, params=payload)
        attempts = 0
        while response.status_code != 200 and attempts < self._max_attempts:
            print(f"Response code: {str(response.status_code)} - Error on requesting API. "
                  f"Waiting {str(self._check_progress_interval_secs)} sec until next retry...")
            attempts += 1
            time.sleep(self._check_progress_interval_secs)
            response = requests.get(url, params=payload)
        return response.json()

    @staticmethod
    def prepare_datetime(epoch_time):
        # SSL Labs returns an 13-digit epoch time that contains milliseconds, Python only expects 10 digits (seconds)
        return datetime.utcfromtimestamp(float(str(epoch_time)[:10])).strftime("%Y-%m-%d")

    def append_summary_csv(self, summary_file, host, data):
        # write the summary to file
        with open(summary_file, "a") as outfile:
            for ep in data["endpoints"]:
                # see SUMMARY_COL_NAMES
                summary = [
                    host,
                    ep["grade"],
                    ep["hasWarnings"],
                    self.prepare_datetime(ep["details"]["cert"]["notAfter"]),
                    CHAIN_ISSUES[str(ep["details"]["chain"]["issues"])],
                    FORWARD_SECRECY[str(ep["details"]["forwardSecrecy"])],
                    ep["details"]["heartbeat"],
                    ep["details"]["vulnBeast"],
                    ep["details"]["drownVulnerable"],
                    ep["details"]["heartbleed"],
                    ep["details"]["freak"],
                    False if ep["details"]["openSslCcs"] == 1 else True,
                    False if ep["details"]["openSSLLuckyMinus20"] == 1 else True,
                    ep["details"]["poodle"],
                    False if ep["details"]["poodleTls"] == 1 else True,
                    ep["details"]["supportsRc4"],
                    ep["details"]["rc4WithModern"],
                    ep["details"]["rc4Only"],
                ]
                for protocol in PROTOCOLS:
                    found = False
                    for p in ep["details"]["protocols"]:
                        if protocol.startswith(f"{p['name']} {p['version']}"):
                            found = True
                            break
                    summary += ["Yes" if found is True else "No"]

                outfile.write(",".join(str(s) for s in summary) + "\n")
