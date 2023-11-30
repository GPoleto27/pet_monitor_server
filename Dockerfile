FROM python:3.8-slim-buster

COPY requirements.txt /app/requirements.txt

RUN apt update -y
RUN apt install -y pkg-config gcc

RUN pip install -r /app/requirements.txt
