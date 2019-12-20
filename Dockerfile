FROM python:3.6-alpine
LABEL maintainer="3vilpenguin@gmail.com"

RUN apk add -U --no-cache alpine-sdk bluez-dev

COPY . /src
WORKDIR /src
RUN python setup.py install

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
