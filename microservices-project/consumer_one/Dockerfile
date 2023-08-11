FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install pika
RUN pip install flask
RUN pip install --no-cache-dir -r requirements.txt
COPY healthcheck.py .
CMD ["python", "healthcheck.py"]

