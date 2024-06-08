FROM python:3.11-slim as builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir pdm
RUN pdm install

FROM python:3.11-slim

WORKDIR /app

COPY . /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Выводим содержимое /app/.venv/bin для отладки
RUN ls -la /usr/local/lib/python3.11/site-packages
RUN ls -la /usr/local/lib/python3.11/site-packages