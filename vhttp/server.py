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
  # List of proxies to send requests to.
  proxies = frozenset(filter(str, os.getenv('VHTTP_PROXIES', '').split(',')))
  # Threshold for consensus to be achieved.
  threshold = decimal.Decimal(os.getenv('VHTTP_THRESHOLD', '0.5'))
  # Whether or not to perform the normal request as well.
  perform_normal = int(os.getenv('VHTTP_PERFORM_NORMAL', '1'))

  if len(proxies):
    _log.info("Vantage Points: %s.", ','.join(proxies))
  else:
    _log.warning("No proxies provided. Operating in normal proxy mode, "
      "without support for vantage points.")

  if perform_normal and len(proxies):
    # None performs a normal lookup without a proxy.
    proxies |= frozenset({None})

  # Serve all requests with the proxy handler
  handler = functools.partial(
    proxy.proxy_request,
    vantage_points=proxies,
    threshold=threshold)

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
