FROM python:3.10-slim

WORKDIR /app

# Копируем файл requirements.txt отдельно
COPY requirements.txt /app/

# Копируем всю папку lecture_1 и другие необходимые файлы
COPY ./lecture_1 ./lecture_1

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn fastapi

# Установка PYTHONPATH и запуск uvicorn
ENV PYTHONPATH=/app
CMD ["uvicorn", "lecture_1.hw.math_plain_asgi:app", "--host", "0.0.0.0", "--port", "8000"]
