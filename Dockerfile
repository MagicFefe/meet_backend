FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update -y \
    && apt-get install -y libmagic-dev  \
    && pip install -r /app/requirements.txt \
    && set -xe \
    && apt-get install python3-pip postgresql-client -y

COPY . .

EXPOSE 8000

CMD uvicorn main:app --host 0.0.0.0 --port 8000
