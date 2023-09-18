FROM python:3.10-slim-buster

WORKDIR /app

LABEL maintainer='mukeshkumarbairwa5686@gmail.com'
LABEL website='https://www.capitalsscope.com'
LABEL description='Development image for django celery project'


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    # dependices for building python packages
    && apt-get install -y build-essential \ 
    # psycopg2 dependices
    && apt-get install -y libpq-dev \
    # mysql dependices 
    && apt-get install -y python3-dev default-libmysqlclient-dev build-essential \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/list/*

RUN pip install --upgrade pip 
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./docker/local/django/entrypoint /entrypoint  
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start  
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./docker/local/django/celery/worker/start /start-celeryworker  
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./docker/local/django/celery/beat/start /start-celerybeat  
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./docker/local/django/celery/flower/start /start-flower  
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

ENTRYPOINT [ "/entrypoint" ]


