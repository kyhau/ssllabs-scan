# SSL Labs Scan #

[![Build Status](https://travis-ci.org/kyhau/ssllabs-scan.svg?branch=master)](https://travis-ci.org/kyhau/ssllabs-scan) 
[![codecov](https://codecov.io/gh/kyhau/ssllabs-scan/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/ssllabs-scan)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

Support Python 2/3

Call SSL Labs [API](https://github.com/ssllabs/ssllabs-scan/blob/stable/ssllabs-api-docs.md) to do SSL testings on servers.

## Input and Output

Sample input: [sample/SampleServerList.txt](sample/SampleServerList.txt)

1. summary.html 
1. summary.csv 
1. _hostname_.json (sample output: [sample/google.com.json](sample/google.com.json))

**Sample html output:**
![alt text](sample/SampleHtmlOutput.png "Sample html output")

## Build and Run

### Linux
```bash
virtualenv env
. env/bin/activate
pip install -e .
. env/bin/ssllabs-scan SampleServerList.txt
```

### Windows
```
virtualenv env
env\Scripts\activate
pip install -e .
env\Scripts\ssllabs-scan SampleServerList.txt
```

## Tox Tests and Build the Wheels

```
pip install -r requirements-build.txt
tox -r
```
