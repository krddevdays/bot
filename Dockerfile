# Первый этап: сборщик
FROM python:3.11-slim AS builder

WORKDIR /app

# Копируем файлы, необходимые для установки зависимостей
COPY pyproject.toml pdm.lock /app/

# Устанавливаем PDM и зависимости проекта
RUN pip install --no-cache-dir pdm \
    && pdm install --prod --no-lock --no-editable

# Второй этап: финальный образ
FROM python:3.11-slim

WORKDIR /app

# Копируем файлы приложения
COPY . /app

# Копируем установленные зависимости из этапа сборки
COPY --from=builder /app/__pypackages__/ /app/__pypackages__/

# Устанавливаем переменную окружения PDM для использования установленных зависимостей
ENV PDM_IGNORE_SAVED_PYTHON=1

# Устанавливаем точку входа или CMD, если необходимо
CMD ["pdm", "run", "python", "your_main_script.py"]
