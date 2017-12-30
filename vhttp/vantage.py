# vhttp/vantage.py
# vhttp
# Author: Rushy Panchal
# Date: December 29th, 2017
# Description: Vantage-point consensus checking.

import typing
import decimal
import hashlib
import collections

import aiohttp.web

def check_consensus(
    *responses: typing.List[aiohttp.web.Response],
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
  total = len(responses)
  hashes = {}
  frequencies = collections.defaultdict(lambda: 0)

  # NOTE: operate in multiple passes? Each pass is less granular than the
  # first.

  for r in responses:
    resp_hash = hash_response(r)
    frequencies[resp_hash] += 1
    hashes[resp_hash] = r

  for h, f in frequencies.items():
    if (f / total) >= threshold:
      return hashes[h]

  return None

def hash_response(r: aiohttp.web.Response) -> str:
  return hashlib.sha256(r.body).hexdigest()
