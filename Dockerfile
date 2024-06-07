# ------------------- Stage 1: Build Stage ------------------------------
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    # Устанавливаем PDM глобально
    RUN pip install --no-cache-dir pdm
    
    # Копируем только необходимые файлы для сборки зависимостей
    COPY pyproject.toml pdm.lock /app/
    
    # Создаем виртуальное окружение вручную и устанавливаем зависимости
    RUN python -m venv /app/.venv \
        && . /app/.venv/bin/activate \
        && /app/.venv/bin/pip install --no-cache-dir pdm \
        && /app/.venv/bin/pdm install --no-self
    
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
    