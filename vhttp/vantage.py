# vhttp/vantage.py
# vhttp
# Author: Rushy Panchal
# Date: December 29th, 2017
# Description: Vantage-point consensus checking.

import typing
import decimal
import hashlib
import collections
import logging
import os

import aiohttp.web

_log = logging.getLogger('vhttp')

# Most headers cannot be hashed, as they will be modified by any inflight
# proxies... so we can only cache content-dependent headers, and not
# path-dependent.
HASHED_HEADERS = frozenset({
  'Content-Type',
  'Content-Language',
  'Host',
  'ETag',
  })

# Additional headers related to caching. Disabled by default as these headers
# will likely vary even if the same content is returned.
if int(os.getenv('VHTTP_HASH_CACHE_HEADERS', '0')):
  HASHED_HEADERS |= frozenset({
    'Last-Modified',
    'Cache-Control',
    })

def check_consensus(
    responses: typing.List[aiohttp.web.Response],
    threshold: decimal.Decimal,
    ) -> typing.Optional[aiohttp.web.Response]:
  '''
  Check for consensus among the responses. This words as a maximization
  procedure up to the threshold; each response is hashed according to various
  properties, described below. The frequency of each hash is counted and if any
  hash's share passes the threshold, it is considered the valid response and
  is returned. Otherwise, None is returned.

  :param responses: responses to find consensus in
  :param threshold: threshold, as a fraction between 0 and 1, for consensus

  :return: response that has consensus, if any
  '''
  total_responses = decimal.Decimal(len(responses))
  frequencies = collections.defaultdict(lambda: 0)

  max_frequency = 0
  possible_resp = None

  for r in responses:
    resp_hash = hash_response(r)
    frequencies[resp_hash] += 1

    if frequencies[resp_hash] >= max_frequency:
      max_frequency = frequencies[resp_hash]
      possible_resp = r

  max_agreement = max_frequency / total_responses
  if max_agreement >= threshold:
    _log.info('Consensus Achieved (%f).' % max_agreement)
    return possible_resp

  return None

def hash_response(r: aiohttp.web.Response) -> str:
  '''
  Hash the response into a single string. Currently, the components used are
  the status code and the body.

  :param r: response to hash

  :return: hash of response
  '''
  if not isinstance(r, aiohttp.web.Response):
    return None

  resp_hash = hashlib.sha256()
  resp_hash.update('{:03d}'.format(r.status).encode('utf8'))
  resp_hash.update(r.body)

  for header, value in r.headers.items():
    if header in HASHED_HEADERS:
      resp_hash.update(header.encode('utf8'))
      resp_hash.update(value.encode('utf8'))

  return resp_hash.hexdigest()
