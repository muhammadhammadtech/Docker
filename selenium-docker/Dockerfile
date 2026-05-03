FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl wget && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tests/ ./tests/
COPY conftest.py .

RUN mkdir -p reports screenshots

ENV PYTHONPATH=/app
ENV SELENIUM_HUB_URL=http://selenium-hub:4444/wd/hub

CMD ["pytest", "tests/", "-v"]
