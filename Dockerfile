# ------------------- Stage 1: Build Stage ------------------------------
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    # Устанавливаем PDM глобально
    RUN pip install --no-cache-dir pdm
    
    # Копируем только необходимые файлы для сборки зависимостей
    COPY pyproject.toml pdm.lock /app/
    
    # Создаем виртуальное окружение, устанавливаем зависимости и проверяем PDM 
    RUN python -m venv /app/.venv \
        && /app/.venv/bin/python -m pip install --upgrade pip \
        && /app/.venv/bin/pip install --no-cache-dir pdm \
        && /app/.venv/bin/python -m pdm install --no-self \
        && /app/.venv/bin/pdm --version 
    
    # ------------------- Stage 2: Final Stage ------------------------------
    FROM python:3.11-slim

    WORKDIR /app

    # Копируем виртуальное окружение из стадии сборки
    COPY --from=builder /app/.venv /app/.venv

    # Проверяем содержимое директории bin виртуального окружения
    RUN ls -al /app/.venv/bin

    #  Устанавливаем права на выполнение для всех файлов в /app/.venv/bin
    RUN chmod -R +x /app/.venv/bin

    # Копируем код приложения
    COPY . /app

    # Устанавливаем переменные окружения для PDM
    ENV VIRTUAL_ENV=/app/.venv
    ENV PATH="$VIRTUAL_ENV/bin:$PATH"

    # Выводим PATH для отладки
    RUN echo "Current PATH: $PATH"

    # Объявляем порт, который будет прослушивать бот
    EXPOSE 8080

    # Создаем скрипт для запуска с абсолютным путём к Python
    #  Используем python из виртуального окружения
    RUN echo '#!/bin/sh\n/app/.venv/bin/python -m pdm run bot' > /app/start.sh && chmod +x /app/start.sh

    # Используем скрипт для запуска бота
    CMD ["/app/start.sh"]