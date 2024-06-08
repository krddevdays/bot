FROM python:3.11-slim as builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir pdm
RUN pdm install

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY --from=builder /usr/local/bin/pdm /usr/local/bin/pdm
COPY --from=builder /usr/local/bin/pip /usr/local/bin/pip
COPY --from=builder /usr/local/bin/pip3 /usr/local/bin/pip3
COPY --from=builder /usr/local/bin/virtualenv /usr/local/bin/virtualenv

RUN ls -la /usr/local/lib/python3.11/site-packages
RUN ls -la /usr/local/bin