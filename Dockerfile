FROM python:3.11-slim as builder
WORKDIR /app
COPY pyproject.toml pdm.lock ./
RUN pip install --no-cache-dir pdm
RUN which pdm
COPY . /app
RUN mkdir __pypackages__ && /usr/local/bin/pdm install --prod --no-lock --no-editable -g

FROM python:3.11-slim
ENV PYTHONPATH=/app/pkgs
COPY --from=builder /app/__pypackages__/3.11/lib /app/pkgs