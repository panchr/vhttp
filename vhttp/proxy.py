# vhttp/proxy.py
# vhttp
# Author: Rushy Panchal
# Date: December 29th, 2017
# Description: HTTP Proxy server that utilizes vantage points for consensus
#              when retrieving static content.

import typing
import asyncio
import logging
import decimal
import functools

import aiohttp
import aiohttp.web

import vantage

_log = logging.getLogger('vhttp')

# aiohttp automatically decompresses gzip and deflate
AIOHTTP_DECOMPRESSION_ENCODINGS = frozenset({'gzip', 'deflate'})

async def proxy_request(
    request: aiohttp.web.Request,
    vantage_points: typing.Optional[typing.List[str]] = None,
    threshold: typing.Optional[decimal.Decimal] = None,
    ) -> aiohttp.web.Response:
  '''
  Proxy a request to the destination, potentially through vantage points.
  If vantage points are defined, a threshold of them must have equivalent
  content. Otherwise, the response is rejected and an error is returned.

  :param request: request to proxy
  :param vantange_points: list of proxies to use as vantage points
  :param threshold: fraction of vantage points required to have matching
                    content

  :return: proxy response
  '''
  async with aiohttp.ClientSession(
      version=request.version,
      read_timeout=300,
      conn_timeout=60,
      auto_decompress=True,
      skip_auto_headers=frozenset({'User-Agent'})) as session:
    r = distribute_request(session, request, vantage_points, threshold)
    return await r
 
async def distribute_request(
    session: aiohttp.ClientSession,
    request: aiohttp.web.Request,
    vantage_points: typing.Optional[typing.List[str]] = None,
    threshold: typing.Optional[decimal.Decimal] = None,
    ) -> aiohttp.web.Response:
  '''
  Distribute requests across a series of vantage points and check for a
  threshold of agreement in their data. If no such threshold is met, then a
  failure response is sent.

  :param session: session to send requests with
  :param request: request to proxy
  :param vantange_points: list of proxies to use as vantage points
  :param threshold: percentage of vantage points required to pass

  :return: response from distributed request
  '''
  # No proxies defined, so forward the request as normal. No vantage-points.
  if vantage_points is None or not len(vantage_points):
    resp_future = asyncio.ensure_future(
      perform_client_request(session, request))
    try:
      await resp_future
      return resp_future.result()
    except Exception as e:
      return aiohttp.web.Response(status=404, text='Request failed.')
  elif threshold is None:
    raise ValueError('threshold must be set if vantage_points is set.')

  responses = await asyncio.gather(*[
    asyncio.ensure_future(perform_client_request(session, request, proxy))
    for proxy in vantage_points
  ], return_exceptions=True)

  # Ignore failed responses
  successful_responses = list(filter(
    lambda r: isinstance(r, aiohttp.web.Response),
    responses))

  if len(successful_responses):
    consensus = vantage.check_consensus(successful_responses, threshold)
    if consensus is None:
      return aiohttp.web.Response(status=409, text="Consensus not achieved.")

    return consensus
  else:
    _log.warning('All proxies failed for %s.' % request.url)
    return aiohttp.web.Response(status=404, text='No proxies succeeded.')

async def perform_client_request(
    session: aiohttp.ClientSession,
    request: aiohttp.web.Request,
    proxy: typing.Optional[str] = None
    ) -> aiohttp.web.Response:
  '''
  Perform a client request.
  
  :param session: session to perform requests with
  :param request: request to perform
  :param proxy: proxy to use, if any

  :return: response from client
  '''
  http_kwargs = {}

  headers = dict(request.headers)
  headers['Content-Type'] = request.content_type

  if request.can_read_body:
    http_kwargs['body'] = await request.read()
    handle_aiohttp_decompression(http_kwargs['body'], headers)

  async with session.request(
      request.method,
      request.url,
      headers=headers,
      params=request.query,
      proxy=proxy,
      **http_kwargs) as response:
    return await make_response(response)

async def make_response(
    response: aiohttp.ClientResponse,
    ) -> aiohttp.web.Response:
  '''
  Turn a ClientResponse into a server response.

  :param response: response from the aiohttp client

  :return: server response based on client data
  '''
  data = await response.read()
  headers = dict(response.headers)
  handle_aiohttp_decompression(data, headers)

  return aiohttp.web.Response(
    status=response.status,
    body=data,
    headers=headers)

def handle_aiohttp_decompression(data: bytes, headers: dict) -> None:
  '''
  Handle aiohttp's automatic decompression. Disabling auto decompression
  results in inaccurate decompression on the client side. So, we keep
  automatic decompression enabled and modify the headers appropriately to
  reflect the decompressed content.

  :param data: request data
  :param headers: request headers
  '''
  if not 'Content-Encoding' in headers:
    return

  if headers['Content-Encoding'] in AIOHTTP_DECOMPRESSION_ENCODINGS:
    # 'identity' encoding indicates no compression, which signals to the client
    # that no additional decompression is required.
    headers['Content-Encoding'] = 'identity'
    # Content-Length also has to be manually set, because the data is of a
    # different length after being processed.
    headers['Content-Length'] = str(len(data))
