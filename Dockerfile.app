# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы приложения
COPY ./app /app

# Устанавливаем зависимости для приложения
RUN pip install flask

# Запускаем приложение
CMD ["python", "app.py"]