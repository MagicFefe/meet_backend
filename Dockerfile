FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update -q -y \
    && apt-get install -y libmagic-dev  \
    && pip install -r /app/requirements.txt \
    && set -xe \
    && apt-get install python3-pip postgresql-client -q -y

COPY . .

EXPOSE 8000
