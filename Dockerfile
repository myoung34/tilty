FROM alpine:3.16

LABEL maintainer="3vilpenguin@gmail.com"

RUN apk add -U --no-cache python3 bluez-dev && \
  apk add --no-cache --virtual .build-deps py3-setuptools py3-pip python3-dev alpine-sdk && \
  pip3 --no-cache-dir install -U setuptools pip

COPY . /src
WORKDIR /src
RUN python3 setup.py install && \
  apk del .build-deps

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
VOLUME "/etc/tilty"
CMD ["-r", "--config-file", "/etc/tilty/config.ini"]
