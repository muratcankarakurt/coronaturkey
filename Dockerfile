FROM alpine

MAINTAINER "muratcan.karakurt@gmail.com"

USER root

RUN mkdir /app
COPY src /app
ADD start.sh /
RUN chmod +x /start.sh

RUN apk add python3 && \
    apk add curl && \
    pip3.8 install flask gunicorn requests

EXPOSE 30001
ENTRYPOINT ["/bin/sh", "+x", "/start.sh"]