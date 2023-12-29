FROM python:3.11.7-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --user --no-cache-dir -r requirements.txt

COPY ./src ./src
COPY main.py ./
