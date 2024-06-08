FROM python:3.11 as builder
WORKDIR /app
COPY pyproject.toml pdm.lock ./
RUN pip install --no-cache-dir pdm
RUN which pdm
COPY . /app
RUN mkdir -p __pypackages__/3.11/lib && /usr/local/bin/pdm install --prod --no-lock --no-editable -g
RUN ls -la /app/__pypackages__/3.11/lib

FROM python:3.11
ENV PYTHONPATH=/app/pkgs
COPY --from=builder /app/__pypackages__/3.11/lib /app/pkgs
RUN ls -la /app/pkgs