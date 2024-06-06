# Используйте официальный образ Python как родительский образ
FROM python:3.8-slim

# Установите рабочий каталог в контейнере
WORKDIR /app

# Копируйте файлы проекта в контейнер
COPY . /app
COPY config.py .

# Установите любые необходимые пакеты, указанные в файле requirements.txt
RUN pip install --no-cache-dir pdm
RUN pdm install

# Сделайте порт 5000 доступным для мира снаружи контейнера
EXPOSE 5000

# Определите переменную окружения
ENV NAME World

# Запустите app.py при запуске контейнера
CMD ["pdm", "run", "bot"]
