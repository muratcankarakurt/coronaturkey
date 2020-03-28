FROM alpine

MAINTAINER "muratcan.karakurt@gmail.com"

USER root

RUN mkdir /app
COPY src /app
ADD start.sh /
RUN chmod +x /start.sh

RUN apk add python3 && \
    apk add curl && \
    pip3.8 install flask requests

RUN export FLASK_APP=/app/src/countries.py
CMD flask run --host=0.0.0.0:5000
