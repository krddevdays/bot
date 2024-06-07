# ------------------- Stage 1: Build Stage ------------------------------
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    # Устанавливаем PDM глобально
    RUN pip install --no-cache-dir pdm
    
    # Копируем только необходимые файлы для сборки зависимостей
    COPY pyproject.toml pdm.lock /app/
    
    # Создаем виртуальное окружение, устанавливаем зависимости через PDM
    RUN python -m venv /app/.venv \
        && /app/.venv/bin/pip install --upgrade pip \
        && /app/.venv/bin/pip install pdm \
        && /app/.venv/bin/pdm install --no-self
    
    # ------------------- Stage 2: Final Stage ------------------------------
    FROM python:3.11-slim
    
    WORKDIR /app
    
    # Копируем виртуальное окружение из стадии сборки
    COPY --from=builder /app/.venv /app/.venv
    
    # Копируем код приложения
    COPY . /app
    
    # Устанавливаем переменные окружения для PDM
    ENV VIRTUAL_ENV=/app/.venv
    ENV PATH="$VIRTUAL_ENV/bin:$PATH"
    
    # Проверяем наличие исполняемого файла pdm
    RUN ls -al /app/.venv/bin \
        && echo $PATH
    
    # Объявляем порт, который будет прослушивать бот
    EXPOSE 8080
    
    # Создаем скрипт для запуска
    RUN echo '#!/bin/sh\n/app/.venv/bin/python -m pdm run bot' > /app/start.sh && chmod +x /app/start.sh
    
    # Используем скрипт для запуска бота
    CMD ["/app/start.sh"]
    