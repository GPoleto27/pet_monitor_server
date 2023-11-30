FROM python:3.8-slim-buster

COPY requirements.txt /app/requirements.txt
COPY setup.sql /app/setup.sql

RUN apt update -y
# install mysqlclient and mariadb-client and  pkg-config
RUN apt install -y default-libmysqlclient-dev mariadb-client pkg-config gcc


RUN pip install -r /app/requirements.txt
