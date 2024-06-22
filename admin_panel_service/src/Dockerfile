FROM python:3.10

#WORKDIR /opt/app
RUN mkdir /app

ENV DJANGO_SETTINGS_MODULE 'config.settings'
#ENV DJANGO_SETTINGS_MODULE 'src.config.settings'
ENV PYTHONPATH /app
#ENV PYTHONPATH /app/src
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

COPY .env /app/.env
COPY requirements.txt app/requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r /app/requirements.txt --no-cache-dir


WORKDIR /app
COPY ../.. .
#COPY src /app/src

CMD ["bash", "deploy.sh"]