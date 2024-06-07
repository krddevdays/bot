# ------------------- Stage 1: Build Stage ------------------------------
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    # Устанавливаем PDM глобально
    RUN pip install --no-cache-dir pdm
    
    # Копируем только необходимые файлы для сборки зависимостей
    COPY pyproject.toml pdm.lock /app/
    
    # Устанавливаем зависимости с помощью PDM
    RUN pdm install --no-self
    
    # ------------------- Stage 2: Final Stage ------------------------------
    FROM python:3.11-slim
    
    WORKDIR /app
    
    # Копируем виртуальное окружение и PDM из стадии сборки
    COPY --from=builder /app/.venv /app/.venv
    COPY --from=builder /app /app
    
    # Устанавливаем переменные окружения для PDM
    ENV PATH="/app/.venv/bin:$PATH"
    ENV VIRTUAL_ENV="/app/.venv"
    
    # Объявляем порт, который будет прослушивать бот
    EXPOSE 8080
    
    # Запускаем бота
    CMD ["pdm", "run", "bot"]
    