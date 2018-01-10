#!/bin/sh
# bin/proxy.sh
# http-mitm
# Author: Rushy Panchal
# Date: December 22nd, 2017
# Description: Run an HTTP Proxy using mitmproxy.

if command -v docker; then
  docker build mitm -f mitm/Dockerfile -t http-mitm:latest
  docker run --rm -p 8080:8080 http-mitm:latest
else
  if command -v mitmdump; then
    echo "Please install mitmproxy and mitmdump: https://mitmproxy.org."
    echo "Alternatively, Docker is also supported."
    exit 1
  fi

  mitmdump -s rewrite_payload.py
fi
