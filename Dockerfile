# Dockerfile

FROM mitmproxy/mitmproxy:latest
MAINTAINER Rushy Panchal <rpanchal@princeton.edu>

ARG SCRIPT_PATH="mitm/malicious.sh"
ARG MITM_PATH="mitm/rewrite_payload.py"

ENV MALICIOUS_SCRIPT "/opt/malicious.sh"

COPY $SCRIPT_PATH "/opt/malicious.sh"
COPY $MITM_PATH "/opt/rewrite_payload.py"
CMD ["mitmdump", "-s", "/opt/rewrite_payload.py"]
