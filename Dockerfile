FROM python:3.10

WORKDIR /app

ENV PORT = 8000
ENV HOST = 0.0.0.0

COPY ./requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y libmagic-dev && pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./main.py /app/

CMD exec uvicorn main:app --host $HOST --port $PORT
