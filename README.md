# SSL Labs Scan #

Calling SSL Labs API to do SSL testings on our servers.

See API doc: https://github.com/ssllabs/ssllabs-scan/blob/stable/ssllabs-api-docs.md


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
