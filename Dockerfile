ARG PYTHON_BASE=3.13-slim

FROM python:$PYTHON_BASE AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN uv sync --frozen --no-dev --no-install-project

FROM python:$PYTHON_BASE

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"
COPY . .

CMD ["python3", "-m", "krddevbot"]
