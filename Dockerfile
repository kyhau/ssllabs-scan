# Use an official Python runtime as a parent image
FROM python:3.13.1-slim-bookworm

# Install poetry
RUN pip install --no-cache-dir poetry==1.8.5

WORKDIR /app

# Copy only dependency files first for better caching
COPY pyproject.toml poetry.lock* ./

# Install dependencies without dev dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi

# Copy the rest of the application
COPY . .

# Copy styles.css to the correct location
RUN cp sample/styles.css /usr/local/lib/python3.13/site-packages/ssllabsscan/styles.css

ENTRYPOINT [ "ssllabs-scan" ]
