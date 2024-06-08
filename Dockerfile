FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install --no-cache-dir pdm

COPY pyproject.toml pdm.lock /app/
COPY . /app

RUN mkdir __pypackages__ && pdm install --prod --no-lock --no-editable

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH=/app/pkgs
COPY --from=builder /app/__pypackages__/3.11/lib /app/pkgs