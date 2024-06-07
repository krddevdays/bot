FROM python:3.11-slim as builder

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pdm
RUN pdm install

FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pdm && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app /app
