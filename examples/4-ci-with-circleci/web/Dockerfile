FROM python:2.7
MAINTAINER Marteinn
LABEL version="v1.0.1"

RUN apt-get update && apt-get install netcat -y

ENV PYTHONUNBUFFERED 1
ENV RUN_TYPE wsgi

RUN mkdir /web
WORKDIR /web
ADD . /web/

RUN pip install -r requirements/prod.txt

EXPOSE 8080

COPY ./docker-entrypoint.sh /web/
ENTRYPOINT ["/web/docker-entrypoint.sh"]
