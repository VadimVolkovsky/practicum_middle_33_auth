FROM python:3.12

RUN mkdir /app

COPY requirements.txt /app/requirements.txt
COPY .env /app/.env
COPY .flake8 /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

WORKDIR app
#COPY src /src