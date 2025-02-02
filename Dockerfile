FROM python:3.11-slim AS python

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    bash \
    libffi-dev \
    libssl-dev \
    python3-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем и устанавливаем Python-зависимости
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . /app/

# Открываем порт
EXPOSE 2525

# Команда для запуска приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2525", "--reload"]