FROM python:3.11.9-alpine3.19
WORKDIR /app
COPY requirements.txt .
COPY .env /app/.env

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
USER root
CMD ["python3", "reddit_to_kafka.py", "topic1"]
