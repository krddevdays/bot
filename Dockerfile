FROM python:3.11-slim as builder

WORKDIR /app
COPY pyproject.toml pdm.lock /app/ 

RUN pip install --no-cache-dir pdm
RUN pdm install --prod --download

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv 
COPY . /app 

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH" 