# ------------------- Stage 1: Build Stage ------------------------------
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    # Копируем только необходимые файлы для сборки зависимостей
    COPY pyproject.toml pdm.lock /app/
    
    # Устанавливаем зависимости
    RUN pip install --no-cache-dir pdm
    RUN pdm install

    RUN pdm run -s pytest --install 
    
# ------------------- Stage 2: Final Stage ------------------------------
    FROM python:3.11-slim
    
    WORKDIR /app
    
    # Копируем зависимости из стадии сборки
    COPY --from=builder /app/.venv /app/.venv
    # Копируем код приложения
    COPY . /app
    
    # Устанавливаем переменную окружения для PDM
    ENV PYTHONPATH=/app/.venv/lib/python3.11/site-packages
    
    # Объявляем порт, который будет прослушивать бот
    EXPOSE 8080
    
    # Запускаем бота
    CMD ["pdm", "run", "bot"] 