FROM python:3.12.3-alpine3.19

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    linux-headers \
    build-base \
    libffi-dev \
    openssl-dev \
    python3-dev \
    cargo

RUN pip install --upgrade pip
COPY src/requirements.txt /temp/requirements.txt
RUN pip install --no-cache-dir -r /temp/requirements.txt

COPY src /opt/digitalplatform
WORKDIR /opt/digitalplatform
EXPOSE 8000

RUN adduser --disabled-password mxtube
RUN mkdir -p /opt/dp_data/
RUN mkdir -p /opt/dp_static/