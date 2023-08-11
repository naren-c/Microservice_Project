FROM python:3.9-slim-buster

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY deletion.py .

CMD [ "python", "./deletion.py" ]

