FROM golang:alpine AS builder
ENV CGO_ENABLED=0
ENV CGO_CHECK=0
RUN apk update && \
  apk add --no-cache git=2.36.2-r0
WORKDIR $GOPATH/src/mypackage/myapp/
COPY . .
RUN go build -o /usr/local/bin/tilty main.go


FROM alpine:3.16
LABEL maintainer="3vilpenguin@gmail.com"

RUN apk add -U --no-cache bluez

COPY --from=builder /usr/local/bin/tilty /usr/local/bin/tilty
VOLUME "/etc/tilty"
ENTRYPOINT ["/usr/local/bin/tilty"]
CMD ["--config-file", "/etc/tilty/config.ini"]
