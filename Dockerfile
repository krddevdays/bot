FROM python:3.11-slim as builder

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir pdm
RUN pdm install


FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app /app

RUN chmod +x /app/bin

ENTRYPOINT ["/app/bin"]