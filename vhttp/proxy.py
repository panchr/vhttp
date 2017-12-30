# vhttp/proxy.py
# vhttp
# Author: Rushy Panchal
# Date: December 29th, 2017
# Description: SOCKS5 proxy for HTTP.

import typing
import asyncio
import logging
import decimal
import functools

import aiohttp
import aiohttp.web

_log = logging.getLogger('vhttp')

async def proxy_request(
    request: aiohttp.web.Request,
    vantage_points: typing.Optional[typing.List[str]] = None,
    quorum: typing.Optional[decimal.Decimal] = None,
    ) -> aiohttp.web.Response:
  '''
  Proxy a request to the destination, potentially through vantage points.
  If vantage points are defined, a quorum of them must have equivalent content.
  Otherwise, the response is rejected and an error is returned.

  :param request: request to proxy
  :param vantange_points: list of proxies to use as vantage points
  :param quorum: percentage of vantage points required to pass
  '''
  session = aiohttp.ClientSession(
    version=request.version,
    read_timeout=120,
    conn_timeout=60,
    skip_auto_headers=frozenset({'User-Agent'}))

  # No proxies defined, so forward the request as normal. No vantage-points.
  if vantage_points is None or not len(vantage_points):
    response = await perform_client_request(session, request)
    return await make_response(response)

  resp_futures = [
    asyncio.ensure_future(perform_client_request(session, request, proxy))
    for proxy in vantage_points
  ]
  responses = await asyncio.gather(*resp_futures)
  assumed_correct = await make_response(responses[0])
  return assumed_correct

async def perform_client_request(
    session: aiohttp.ClientSession,
    request: aiohttp.web.Request,
    proxy: typing.Optional[str] = None
    ) -> aiohttp.ClientResponse:
  '''
  Perform a client request.
  
  :param session: session to perform requests with
  :param request: request to perform
  :param proxy: proxy to use, if any
  '''
  http_kwargs = {}
  http_headers = {}

  if request.can_read_body:
    http_kwargs['body'] = await request.read()

  http_headers = dict(request.headers)
  http_headers['Content-Type'] = request.content_type

  return session.request(
    request.method,
    request.url,
    headers=http_headers,
    params=request.query,
    proxy=proxy,
    **http_kwargs)

async def make_response(
    # TODO: this type is wrong, should be a context manager
    response_ctx: aiohttp.ClientResponse
    ) -> aiohttp.web.Response:
  '''
  Turn a response context into a response.
  '''

  async with response_ctx as response:
    data = await response.read()

    resp = aiohttp.web.Response(
      status=response.status,
      body=data,
      headers=response.headers)

    return resp
