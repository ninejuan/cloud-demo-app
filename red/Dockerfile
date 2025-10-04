FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

ENV DB_HOST=localhost
ENV DB_PORT=3306
ENV DB_USER=user
ENV DB_PASSWORD=password
ENV DB_NAME=red_db

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
