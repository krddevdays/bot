# ------------------- Stage 1: Build Stage ------------------------------
    FROM python:3.11-slim AS builder

    WORKDIR /app
    
    # Устанавливаем PDM глобально и выводим версию для проверки
    RUN pip install --no-cache-dir pdm && pdm --version
    
    # Копируем только необходимые файлы для сборки зависимостей
    COPY pyproject.toml pdm.lock /app/
    
    # Создаем виртуальное окружение, устанавливаем PDM и зависимости, выводим их версии для проверки
    RUN python -m venv /app/.venv \
        && /app/.venv/bin/python -m pip install --upgrade pip \
        && /app/.venv/bin/pip install --no-cache-dir pdm \
        && /app/.venv/bin/pdm --version \
        && /app/.venv/bin/pdm install --no-self \
        && /app/.venv/bin/pip list
    
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
    
    # Проверяем содержимое виртуального окружения и наличие pdm
    RUN ls -al /app/.venv/bin
    