# vhttp/Dockerfile
# vhttp
# Author: Rushy Panchal
# Date: January 10th, 2018
# Description: Dockerfile for running vhttp proxy.

FROM python:3.6.4-alpine3.7
LABEL maintainer="Rushy Panchal <rpanchal@princeton.edu>"

ARG PORT=7777
ARG APP_DIR="/opt/vhttp/proxy"

RUN pip3 install --no-cache-dir pipenv

WORKDIR "$APP_DIR"
COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pipenv install --system

COPY . .

EXPOSE ${PORT}
ENV VHTTP_PROXY_HOST '0.0.0.0'
ENV VHTTP_PROXY_PORT ${PORT}
ENV PYTHONPATH "/opt/vhttp"

WORKDIR "/opt/vhttp"
CMD ["python", "proxy/server.py"]
