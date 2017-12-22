# tests/Dockerfile
# http-mitm
# Author: Rushy Panchal
# Date: December 22nd, 2017
# Description: Dockerfile for running tests.

FROM mitmproxy/mitmproxy:latest
MAINTAINER Rushy Panchal <rpanchal@princeton.edu>

RUN apk add --update python

ENV MALICIOUS_SCRIPT "/opt/mitm/malicious.sh"
COPY . /opt/

WORKDIR /opt/
CMD ["sh", "/opt/bin/test.sh"]
