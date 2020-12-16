# SSL Labs Scan

[![githubactions](https://github.com/kyhau/ssllabs-scan/workflows/Build-Test/badge.svg)](https://github.com/kyhau/ssllabs-scan/actions)
[![travisci](https://travis-ci.org/kyhau/ssllabs-scan.svg?branch=master)](https://travis-ci.org/kyhau/ssllabs-scan)
[![codecov](https://codecov.io/gh/kyhau/ssllabs-scan/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/ssllabs-scan)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

Support Python >= 3.6

This tool calls the SSL Labs [API v2](https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs.md) to do SSL testings on servers.

- **TODO**: use v3 instead of v2
- **NOTE**: Please note that the SSL Labs Assessment API has access rate limits. You can find more details in the sections "Error Response Status Codes" and "Access Rate and Rate Limiting" in the official [SSL Labs API Documentation](https://github.com/ssllabs/ssllabs-scan/blob/master/ssllabs-api-docs.md). Some common status codes are:
    - 400 - invocation error (e.g., invalid parameters)
    - 429 - client request rate too high or too many new assessments too fast
    - 500 - internal error
    - 503 - the service is not available (e.g., down for maintenance)
    - 529 - the service is overloaded


## Input and Output

Sample input: [sample/SampleServerList.txt](sample/SampleServerList.txt)

1. summary.html (sample output: [sample/summary.html](https://kyhau.github.io/ssllabs-scan/sample/summary.html))
1. summary.csv (sample output: [sample/summary.csv](sample/summary.csv))
1. _hostname_.json (sample output: [sample/google.com.json](sample/google.com.json))

**Sample html output:**
![alt text](sample/SampleHtmlOutput.png "Sample html output")

## Build and Run

### Linux
```
virtualenv env
. env/bin/activate
pip install -e .
ssllabs-scan sample/SampleServerList.txt
```

### Windows
```
virtualenv env
env\Scripts\activate
pip install -e .
ssllabs-scan sample\SampleServerList.txt
```

## Tox Tests and Build the Wheels

```
pip install -r requirements-build.txt
tox -r
```
