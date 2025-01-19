# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения
COPY app.py /app/app.py

# Устанавливаем зависимости для приложения
RUN pip install flask
RUN pip install prometheus-client

# Запускаем приложение
CMD ["python", "app.py"]