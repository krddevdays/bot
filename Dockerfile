FROM python:3.11-slim as builder
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir pdm
RUN pdm install

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app /app

COPY --from=builder /usr/local/lib/python3.11/site-packages/packaging /usr/local/lib/python3.11/site-packages/packaging
COPY --from=builder /usr/local/lib/python3.11/site-packages/packaging-24.0.dist-info /usr/local/lib/python3.11/site-packages/packaging-24.0.dist-info
COPY --from=builder /usr/local/lib/python3.11/site-packages/pdm /usr/local/lib/python3.11/site-packages/pdm
COPY --from=builder /usr/local/lib/python3.11/site-packages/pdm-2.15.4.dist-info /usr/local/lib/python3.11/site-packages/pdm-2.15.4.dist-info
COPY --from=builder /usr/local/lib/python3.11/site-packages/resolvelib /usr/local/lib/python3.11/site-packages/resolvelib
COPY --from=builder /usr/local/lib/python3.11/site-packages/resolvelib-1.0.1.dist-info /usr/local/lib/python3.11/site-packages/resolvelib-1.0.1.dist-info

COPY --from=builder /usr/local/bin /usr/local/bin

# Выводим содержимое /app/.venv/bin для отладки
RUN ls -la /usr/local/lib/python3.11/site-packages
RUN ls -la /usr/local/bin