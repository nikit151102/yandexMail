FROM python:3.11-slim AS python

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
    && apt-get clean

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]