# mitm/Dockerfile
# http-mitm
# Author: Rushy Panchal
# Date: December 22nd, 2017
# Description: Dockerfile for running http-mitm attack.

FROM mitmproxy/mitmproxy:latest
MAINTAINER Rushy Panchal <rpanchal@princeton.edu>

ARG SCRIPT_PATH="malicious.sh"
ARG MITM_PATH="rewrite_payload.py"

ENV MALICIOUS_SCRIPT "/opt/malicious.sh"

COPY $SCRIPT_PATH "/opt/malicious.sh"
COPY $MITM_PATH "/opt/rewrite_payload.py"

WORKDIR /opt/
CMD ["mitmdump", "-s", "/opt/rewrite_payload.py"]
