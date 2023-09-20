FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -qy install python3-dev default-libmysqlclient-dev build-essential dos2unix

RUN pip install --upgrade pip && pip install "setuptools<58.0.0" && pip install pip-tools

RUN mkdir /LongevityInTimeTestTask
RUN mkdir /LongevityInTimeTestTask/static
WORKDIR /LongevityInTimeTestTask

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN dos2unix manage.py
RUN chmod +x manage.py
