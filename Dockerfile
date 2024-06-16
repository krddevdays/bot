ARG PYTHON_BASE=3.10-slim

FROM python:$PYTHON_BASE AS builder

ENV PDM_CHECK_UPDATE=false

WORKDIR /app

RUN pip install --no-cache-dir -U pdm \
    && find /usr/local/lib -name "*.pyc" -exec rm -f {} \;

COPY pyproject.toml pdm.lock /app/

RUN pdm install --check --prod --no-editable \
    && find /usr/local/lib -name "*.pyc" -exec rm -f {} \;

RUN pdm export --dev --without-hashes > /app/.venv/requirements.txt

FROM python:$PYTHON_BASE

WORKDIR /app

COPY --from=builder /app/.venv/ /app/.venv

ENV PATH="/app/.venv/bin:$PATH"
COPY . .

CMD ["python3", "-m", "krddevbot"]
