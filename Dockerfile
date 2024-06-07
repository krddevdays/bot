# ------------------- Stage 1: Build Stage ------------------------------
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    # Устанавливаем PDM глобально
    RUN pip install --no-cache-dir pdm
    
    # Копируем только необходимые файлы для сборки зависимостей
    COPY pyproject.toml pdm.lock /app/
    
    # Создаем виртуальное окружение, устанавливаем зависимости и проверяем PDM 
    RUN python -m venv /app/.venv --copies \
        && /app/.venv/bin/python -m pip install --upgrade pip \
        && /app/.venv/bin/pip install --no-cache-dir pdm \
        && /app/.venv/bin/python -m pdm install --no-self \
        && /app/.venv/bin/pdm --version 
    
    # ------------------- Stage 2: Final Stage ------------------------------
    FROM python:3.11-slim
    
    WORKDIR /app
    
    # Копируем виртуальное окружение из стадии сборки
    COPY --from=builder /app/.venv /app/.venv
    
    # Копируем код приложения
    COPY . /app
    
    # Устанавливаем права на выполнение для всех файлов в /app/.venv/bin
    RUN chmod -R +x /app/.venv/bin
    
    # Проверяем, существует ли символическая ссылка, прежде чем создавать её
    RUN if [ ! -f /app/.venv/bin/python ]; then ln -s /usr/local/bin/python /app/.venv/bin/python; fi
    
    # Устанавливаем переменные окружения для PDM
    ENV VIRTUAL_ENV=/app/.venv
    ENV PATH="$VIRTUAL_ENV/bin:$PATH"
    
    # Выводим PATH для отладки
    RUN echo "Current PATH: $PATH"
    
    # Выводим содержимое /app/.venv/bin для отладки
    RUN ls -la /app/.venv/bin
    
    # Объявляем порт, который будет прослушивать бот
    EXPOSE 8080
    
    # Запускаем бота напрямую, используя python из виртуального окружения
    CMD ["/app/.venv/bin/python", "-m", "pdm", "run", "bot"]
    