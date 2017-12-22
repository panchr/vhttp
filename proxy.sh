#!/bin/sh
# proxy.sh
# http-mitm
# Author: Rushy Panchal
# Date: December 22nd, 2017
# Description: Run an HTTP Proxy using mitmproxy.

if command -v docker; then
  docker build . -t http-mitm:latest
  docker run --rm -p 8080:8080 http-mitm:latest
else
  if command -v mitmdump; then
    echo "Please install mitmproxy and mitmdump: https://mitmproxy.org."
    exit 1
  fi

  mitmdump -s rewrite_payload.py
fi
