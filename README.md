# SSL Labs Scan #

[![Build Status](https://travis-ci.org/kyhau/ssllabs-scan.svg?branch=master)](https://travis-ci.org/kyhau/ssllabs-scan)

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

## Tox Tests

### Linux
```bash
./test.sh
```

### Windows
```
test.bat
```
