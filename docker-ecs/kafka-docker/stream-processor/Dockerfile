FROM python:3.9-slim
WORKDIR /app
RUN pip install kafka-python
COPY stream_processor.py alert_consumer.py ./
CMD ["python", "stream_processor.py"]
