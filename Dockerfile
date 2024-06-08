FROM python:3.11-slim as builder

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pdm
RUN pdm install --prod

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

RUN pdm cache clear && \
    find /usr/local/lib/python3.11/site-packages -type f -name '*.pyc' -delete && \
    find /usr/local/lib/python3.11/site-packages -type d -name '__pycache__' -exec rm -r {} +
