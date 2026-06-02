#####################
FROM python:3.9-slim

RUN groupadd -r appuser && useradd -r -g appuser appuser
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8080
CMD ["python", "app.py"]
