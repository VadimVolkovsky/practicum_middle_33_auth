FROM huecker.io/library/python:3.12

RUN mkdir /app

COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src

RUN  pip install --upgrade pip \
     && pip install -r /app/requirements.txt

COPY  src /app/src

WORKDIR app/src
