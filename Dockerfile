FROM python:3.7.6-slim-buster
RUN apt-get update && apt-get install git -y

ENV PORT 8100

RUN mkdir -p /soft/app
RUN mkdir -p /soft/log

COPY *.py /soft/app/
COPY *.txt /soft/app/
COPY ./tests /soft/app/tests
COPY ./requirements /soft/app/requirements

WORKDIR /soft/app

RUN pip install -r requirements.txt

EXPOSE $PORT
CMD gunicorn tts-service:app -b 0.0.0.0:$PORT --error-logfile /soft/log/gnuicorn.log
