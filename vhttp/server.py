# vhttp/server.py
# vhttp
# Author: Rushy Panchal
# Date: December 29th, 2017
# Description: HTTP Server that proxies all requests.

import asyncio
import os
import functools
import decimal
import logging

import aiohttp
import aiohttp.web

import proxy

_log = logging.getLogger('vhttp')

def get_proxy_server():
  '''
  Get a proxy server to proxy all requests.

  :return: proxy server
  :rtype: asyncio.Server
  '''
  proxy_host = os.getenv('VHTTP_PROXY_HOST', 'localhost')
  proxy_port = int(os.getenv('VHTTP_PROXY_PORT', '7777'))
  proxies = frozenset(filter(str, os.getenv('VHTTP_PROXIES', '').split(',')))
  required_quorum = decimal.Decimal(os.getenv('VHTTP_QUORUM', '0.5'))

  if len(proxies):
    _log.info("Vantage Points: %s.", ','.join(proxies))
  else:
    _log.warning("No proxies provided. Operating in normal proxy mode, "
      "without support for vantage points.")

  # Serve all requests with the proxy handler
  handler = functools.partial(
    proxy.proxy_request,
    vantage_points=proxies,
    quorum=required_quorum)

  proxy_server = aiohttp.web.Server(handler)
  loop = asyncio.get_event_loop()
  return loop.create_server(proxy_server, proxy_host, proxy_port)

if __name__ == '__main__':
  logging.root.setLevel(logging.INFO)
  logging.root.addHandler(logging.StreamHandler())

  loop = asyncio.get_event_loop()
  server = get_proxy_server()
  loop.run_until_complete(server)
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    pass
