FROM python:3.12

RUN mkdir /app

ENV DJANGO_SETTINGS_MODULE 'config.settings'
ENV PYTHONPATH /app

COPY .env /app/.env
COPY requirements.txt app/requirements.txt

RUN  pip install --upgrade pip \
     && pip install -r /app/requirements.txt --no-cache-dir


WORKDIR /app
COPY ../.. .
#COPY src /app/src

CMD ["bash", "deploy.sh"]