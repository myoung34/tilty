FROM alpine:3.12.0

LABEL maintainer="3vilpenguin@gmail.com"

RUN apk add -U --no-cache python3 python3-dev alpine-sdk bluez-dev py3-setuptools

COPY . /src
WORKDIR /src
RUN python3 setup.py install

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["-r", "--config-file", "config.ini"]
