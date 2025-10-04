FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

ENV AWS_REGION=ap-northeast-2
ENV TABLE_NAME=product

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
