FROM ubuntu:bionic
LABEL maintainer="3vilpenguin@gmail.com"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    python-bluez \
    python-pip \
    python-setuptools \
  && rm -rf /var/lib/apt/lists/*

COPY . /src
WORKDIR /src
RUN pip install .

COPY entrypoint.sh /
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
