"""
See APi doc: https://github.com/ssllabs/ssllabs-scan/blob/stable/ssllabs-api-docs.md
"""
from __future__ import print_function
import json
import os
import requests
import time


API_URL = "https://api.ssllabs.com/api/v2/analyze"

CHAIN_ISSUES = {
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

PROTOCOLS = ["TLS 1.2", "TLS 1.1", "TLS 1.0", "SSL 3.0 INSECURE", "SSL 2.0 INSECURE"]

VULNERABLES = ["Vuln Beast", "Vuln Drown", "Vuln Heartbleed", "Vuln FREAK",
               "Vuln openSsl Ccs", "Vuln openSSL LuckyMinus20", "Vuln POODLE", "Vuln POODLE TLS"]

SUMMARY_COL_NAMES = ["Host", "Grade", "HasWarnings", "Chain Status", "Forward Secrecy", "Heartbeat ext"] + VULNERABLES + PROTOCOLS


class SSLLabsClient():
    def __init__(self, check_progress_interval_secs=30):
        self.__check_progress_interval_secs = check_progress_interval_secs

    def analyze(self, host, summary_csv_file):
        data = self.start_new_scan(host=host)

        # write the output to file
        json_file = os.path.join(os.path.dirname(summary_csv_file), '{}.json'.format(host))
        with open(json_file, 'w') as outfile:
            json.dump(data, outfile, indent=2)

        # write the summary to file
        self.append_summary_csv(summary_csv_file, host, data)

    def start_new_scan(self, host, publish='off', startNew='on', all='done', ignoreMismatch='on'):
        path = API_URL
        payload = {
            'host': host,
            'publish': publish,
            'startNew': startNew,
            'all': all,
            'ignoreMismatch': ignoreMismatch
        }
        results = self.request_api(path, payload)
        payload.pop('startNew')

        while results['status'] != 'READY' and results['status'] != 'ERROR':
            time.sleep(self.__check_progress_interval_secs)
            results = self.request_api(path, payload)
        return results

    @staticmethod
    def request_api(url, payload):
        response = requests.get(url, params=payload)
        return response.json()

    def append_summary_csv(self, summary_file, host, data):
        # write the summary to file
        with open(summary_file, 'a') as outfile:
            for ep in data["endpoints"]:
                # see SUMMARY_COL_NAMES
                summary = [
                    host,
                    ep["grade"],
                    ep["hasWarnings"],
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
                ]
                for protocol in PROTOCOLS:
                    found = False
                    for p in ep["details"]["protocols"]:
                        if protocol.startswith('{} {}'.format(p['name'], p['version'])):
                            found = True
                            break
                    summary += ["Yes" if found is True else "No"]

                outfile.write(",".join(str(s) for s in summary) + '\n')

