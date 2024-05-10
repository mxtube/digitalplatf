FROM python:3.12.3-alpine3.19

MAINTAINER Kirill Kuznetsov <kafomin@yandex.ru>

COPY src/requirements.txt /temp/requirements.txt
COPY src /opt/digitalplatform
WORKDIR /opt/digitalplatform
EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password mxtube

RUN chown mxtube /opt/

USER mxtube