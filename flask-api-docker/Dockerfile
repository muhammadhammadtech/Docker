FROM python:3.11-slim

LABEL maintainer="Muhammad Hammad"
LABEL description="Containerized Flask REST API"
LABEL version="1.1"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        curl && \
    rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY app/ .

RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

HEALTHCHECK --interval=20s \
            --timeout=10s \
            --start-period=10s \
            --retries=3 \
CMD curl --fail http://localhost:5000/ || exit 1

CMD ["python", "app.py"]
