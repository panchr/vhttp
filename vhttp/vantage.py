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
import random

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

  # Separator used must be random and unpredictable by a malicious agent.
  # However, the same separator must be used across all of the requests.
  separator = '{:f}'.format(random.random()).encode('utf8')

  for r in responses:
    resp_hash = hash_response(r, separator)
    frequencies[resp_hash] += 1

    if frequencies[resp_hash] >= max_frequency:
      max_frequency = frequencies[resp_hash]
      possible_resp = r

  max_agreement = max_frequency / total_responses
  if max_agreement >= threshold and not isinstance(possible_resp, Exception):
    _log.info('Consensus Achieved (%f).' % max_agreement)
    return possible_resp

  return None

def hash_response(
    r: typing.Union[aiohttp.web.Response, Exception],
    sep: bytes
    ) -> str:
  '''
  Hash the response into a single string. Currently, the components used are
  the status code, headers, and the body.

  :param r: response to hash

  :return: hash of response
  '''
  if isinstance(r, Exception):
    return None

  resp_hash = hashlib.sha256()
  resp_hash.update('{:03d}'.format(r.status).encode('utf8'))

  for header in HASHED_HEADERS:
    if header in r.headers:
      resp_hash.update(header.encode('utf8'))
      resp_hash.update(r.headers[header].encode('utf8'))

  # Adding a mandatory separator prevents the body from "mimicking" headers
  # that are not actually present. Otherwise, a malicious agent could create a
  # body that looks like headers (i.e. a body of "Content-Length: 100\n"),
  # which would result in the same hash as if those headers were used instead.
  resp_hash.update(sep)
  resp_hash.update(r.body)

  return resp_hash.hexdigest()
