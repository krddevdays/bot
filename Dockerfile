# ------------------- Stage 1: Build Stage ------------------------------
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    # Копируем только необходимые файлы для сборки зависимостей
    COPY pyproject.toml pdm.lock /app/
    
    # Устанавливаем PDM и создаем виртуальное окружение с per-site
    RUN pip install --no-cache-dir pdm \
        && pdm install --no-self \
        && pdm venv create --force
    
    # ------------------- Stage 2: Final Stage ------------------------------
    FROM python:3.11-slim
    
    WORKDIR /app
    
    # Копируем виртуальное окружение из стадии сборки
    COPY --from=builder /app/.venv /app/.venv
    
    # Копируем код приложения
    COPY . /app
    
    # Устанавливаем переменные окружения для PDM
    ENV PYTHONPATH=/app/.venv/lib/python3.11/site-packages
    ENV PATH="/app/.venv/bin:$PATH"
    
    # Объявляем порт, который будет прослушивать бот
    EXPOSE 8080
    
    # Запускаем бота
    CMD ["/app/.venv/bin/pdm", "run", "bot"]
    