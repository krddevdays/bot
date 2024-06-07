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
    
    # Копируем виртуальное окружение из стадии сборки
    COPY --from=builder /app/__pypackages__ /app/__pypackages__
    COPY --from=builder /app/.venv /app/.venv
    COPY --from=builder /usr/local/bin/pdm /usr/local/bin/pdm
    
    # Копируем код приложения
    COPY . /app
    
    # Устанавливаем переменные окружения для PDM
    ENV PATH="/app/.venv/bin:/app/__pypackages__/3.11/bin:$PATH"
    
    # Объявляем порт, который будет прослушивать бот
    EXPOSE 8080
    
    # Запускаем бота
    CMD ["pdm", "run", "bot"]
    