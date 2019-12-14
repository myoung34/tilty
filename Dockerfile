FROM ubuntu:bionic
LABEL maintainer="3vilpenguin@gmail.com"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    build-essential \
    libbluetooth-dev \
    python3-dev \
    python3-pip \
    python3-setuptools \
    locales \
  && rm -rf /var/lib/apt/lists/*
RUN echo "LC_ALL=en_US.UTF-8" >> /etc/environment \
  && echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
  && echo "LANG=en_US.UTF-8" > /etc/locale.conf \
  && locale-gen en_US.UTF-8

COPY . /src
WORKDIR /src
RUN pip3 install .

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
