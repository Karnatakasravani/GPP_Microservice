FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
ENV TZ=UTC
WORKDIR /app
RUN apt-get update && apt-get install -y cron tzdata && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY . .

VOLUME ["/data", "/cron"]
EXPOSE 8080

RUN crontab cron/2fa-cron

CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8080