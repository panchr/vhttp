# tests/test_matching.py
# http-mitm
# Author: Rushy Panchal
# Date: December 22nd, 2017
# Description: Test URL matching.

import unittest

from mitm.rewrite_payload import is_target

class TestIsTarget(unittest.TestCase):
  # Base URLs that match the pattern
  base_urls = [
    'http://deis.io/deisctl/install.sh',
    'http://test.com/../...../test.sh',
    'http://101.102.103.104/path/exec.sh',
    'http://101.102.103.104:8080/path/exec.sh',
    'http://2001:0db8:85a3:0000:0000:8a2e:0370:7334/path/exe.jpg.sh',
    'http://2001:0db8:85a3:0000:0000:8a2e:0370:7334:8080/path/exe.jpg.sh',
    'http://example.com/../../mitm.sh',
  ]

  matching_urls = []
  non_matching_urls = [
    'http://example.com/test.py',
    'http://example.com/test.js',
  ]

  @classmethod
  def setUpClass(cls):
    extra_urls = []
    for url in cls.non_matching_urls:
      if url.startswith('http://'):
        extra_urls.append(url.replace('http://', 'https://'))
    cls.non_matching_urls.extend(extra_urls)

    for url in cls.base_urls:
      cls.matching_urls.append(url)

      # https:// URLs should not match
      cls.non_matching_urls.append(url.replace('http://', 'https://'))

  def test_matching(self):
    for url in self.matching_urls:
      self.assertTrue(is_target(url), url)

  def test_not_matching(self):
    for url in self.non_matching_urls:
      self.assertFalse(is_target(url), url)
