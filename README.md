# SSL Labs Scan

[![githubactions](https://github.com/kyhau/ssllabs-scan/actions/workflows/ci-workflow.yaml/badge.svg)](https://github.com/kyhau/ssllabs-scan/actions/workflows/ci-workflow.yaml)
[![codecov](https://codecov.io/gh/kyhau/ssllabs-scan/branch/main/graph/badge.svg)](https://app.codecov.io/gh/kyhau/ssllabs-scan/tree/main)
[![CodeQL](https://github.com/kyhau/ssllabs-scan/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kyhau/ssllabs-scan/actions/workflows/codeql-analysis.yml)
[![SecretsScan](https://github.com/kyhau/ssllabs-scan/actions/workflows/secrets-scan.yml/badge.svg)](https://github.com/kyhau/ssllabs-scan/actions/workflows/secrets-scan.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

This tool calls the SSL Labs API to do SSL testings on the given hosts, and generates csv and html reports.
- The tool uses [API v4](https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v4.md) if you provide your registered email with Qualys SSLLabs via the `--email` argument.
- The tool uses [API v3](https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v3.md) if you do not specify the `--email` argument. Note that v3 will be being deprecated in 2024 by Qualys.


All notable changes to this project will be documented in [CHANGELOG](./CHANGELOG.md).

---
## Built with
- Python - support Python 3.9, 3.10, 3.11, 3.12.
- [CodeQL](https://codeql.github.com) is [enabled](.github/workflows/codeql-analysis.yml) in this repository.
- [Dependabot](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates) is [enabled](.github/dependabot.yml) for auto dependency updates.
- [Gitleaks](https://github.com/gitleaks/gitleaks) and [TruffleHog](https://github.com/trufflesecurity/trufflehog) are enabled in this GitHub Actions [workflow](.github/workflows/secrets-scan.yml) for detecting and preventing hardcoded secrets.

---
## Input and outputs

Sample input: [sample/SampleServerList.txt](sample/SampleServerList.txt)

1. summary.html (sample output: [sample/summary.html](https://kyhau.github.io/ssllabs-scan/sample/summary.html))
1. summary.csv (sample output: [sample/summary.csv](sample/summary.csv))
1. _hostname_.json (sample output: [sample/google.com.json](sample/google.com.json))

**Sample html output:**
![alt text](sample/SampleHtmlOutput.png "Sample html output")

You can change the report template and styles in these files:
- [ssllabsscan/report_template.py](./ssllabsscan/report_template.py)
- [ssllabsscan/styles.css](./ssllabsscan/styles.css)

---
## Important Notes

ℹ️ Please note that from Qualys SSLLabs API v4, you must use a one-time registration with Qualys SSLLabs. For details see [Introduction of API v4 for Qualys SSLLabs and deprecation of API v3](https://notifications.qualys.com/api/2023/09/28/introduction-of-api-v4-for-qualys-ssllabs-and-deprecation-of-api-v3).
> The API v3 API will be available until the end of 2023 (Dec 31st 2023), and starting from 1st January 2024, we will be deprecating the API v3 support for SSL Labs. Request all customers to move to API v4.

ℹ️ Please note that the SSL Labs Assessment API has access rate limits. You can find more details in the sections "Error Response Status Codes" and "Access Rate and Rate Limiting" in the official [SSL Labs API Documentation](https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs-v3.md). Some common status codes are:
- 400 - invocation error (e.g., invalid parameters)
- 429 - client request rate too high or too many new assessments too fast
- 500 - internal error
- 503 - the service is not available (e.g., down for maintenance)
- 529 - the service is overloaded

---
## Build and run

### Linux
```
# Create and activate a new virtual env (optional)
virtualenv env
. env/bin/activate

# Install
pip install -e .

# Run with v3 (v3, which does not required a registered email, will be being deprecated in 2024)
ssllabs-scan sample/SampleServerList.txt

# Run with v4
ssllabs-scan sample/SampleServerList.txt --email <your registered email with Qualys SSLLabs>
```

### Windows
```
# Create and activate a new virtual env (optional)
virtualenv env
env\Scripts\activate

# Install
pip install -e .

# Run with v3 (v3, which does not required a registered email, will be being deprecated in 2024)
ssllabs-scan sample\SampleServerList.txt

# Run with v4
ssllabs-scan sample\SampleServerList.txt --email <your registered email with Qualys SSLLabs>
```

### Docker
```
# Build docker image
docker build . --tag=ssllabsscan
```
Running Docker from commandline:
```
# create directory for input and output
mkdir out
# put serverlist in directory
cp SampleServerlist.txt out
# Run docker image with created directory mounted as /tmp
# use -t option to prevent output buffering
docker run --mount type=bind,source=./out,target=/tmp ssllabsscan  -o /tmp/output.html -s /tmp/output.csv /tmp/SampleServerList.txt
# all html, csv, json output is in the out directory
```

### Example console output
```
$ ssllabs-scan sample/SampleServerList.txt
Start analyzing duckduckgo.com...
Status: DNS, StatusMsg(Resolving domain names): waiting 30 secs until next check...
Status: IN_PROGRESS, StatusMsg(None): waiting 30 secs until next check...
Status: IN_PROGRESS, StatusMsg(None): waiting 30 secs until next check...
Start analyzing google.com...
Status: DNS, StatusMsg(Resolving domain names): waiting 30 secs until next check...
Status: IN_PROGRESS, StatusMsg(None): waiting 30 secs until next check...
Status: IN_PROGRESS, StatusMsg(None): waiting 30 secs until next check...
Status: IN_PROGRESS, StatusMsg(None): waiting 30 secs until next check...
Status: IN_PROGRESS, StatusMsg(None): waiting 30 secs until next check...
Status: IN_PROGRESS, StatusMsg(None): waiting 30 secs until next check...
Status: IN_PROGRESS, StatusMsg(None): waiting 30 secs until next check...
Creating summary.html ...
```

## Run Tox tests and build the wheels

```
pip install -r requirements-build.txt
tox -r
```
