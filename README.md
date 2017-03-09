# SSL Labs Scan #

[![Build Status](https://travis-ci.org/kyhau/ssllabs-scan.svg?branch=master)](https://travis-ci.org/kyhau/ssllabs-scan)
[![codecov](https://codecov.io/gh/kyhau/ssllabs-scan/branch/master/graph/badge.svg)](https://codecov.io/gh/kyhau/ssllabs-scan)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](http://en.wikipedia.org/wiki/MIT_License)

Call SSL Labs [API](https://github.com/ssllabs/ssllabs-scan/blob/stable/ssllabs-api-docs.md) to do SSL testings on servers.

## Build

### Linux
```bash
virtualenv env
. env/bin/activate
pip install -e .
python ssllabsscan/main.py SampleServerList.txt
```

### Windows
```
virtualenv env
env\Scripts\activate
pip install -e .
python ssllabsscan/main.py SampleServerList.txt
```

## Tox Tests and Build the Wheels

```
pip install -r requirements-build.txt
tox -r
```
