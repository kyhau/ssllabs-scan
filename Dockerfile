FROM python:3.13-slim
LABEL maintainer="virtualda@gmail.com"

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry==1.8.5

# Copy dependency files first for better layer caching
COPY pyproject.toml poetry.lock ./

# Install dependencies only (without the package itself)
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-interaction --no-ansi && \
    rm -rf /root/.cache/pip

# Copy application code
COPY ssllabsscan/ ./ssllabsscan/
COPY sample/ ./sample/

# Install the package itself
RUN poetry install --only-root

# Copy styles.css to the correct location for runtime
RUN cp sample/styles.css /usr/local/lib/python3.13/site-packages/ssllabsscan/styles.css

ENTRYPOINT ["ssllabs-scan"]
