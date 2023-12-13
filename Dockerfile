# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

COPY . /

# Install ssllabsscan module
RUN pip3 install .
COPY sample/styles.css /usr/local/lib/python3.11/site-packages/ssllabsscan/styles.css

ENTRYPOINT  [ "ssllabs-scan" ]