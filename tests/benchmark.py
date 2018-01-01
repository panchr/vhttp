# tests/benchmark.py
# vhttp
# Author: Rushy Panchal
# Date: December 31st, 2017
# Description: Benchmark vhttp.

import requests
import typing
import time
import sys

def main() -> int:
  if len(sys.argv) < 3:
    print('Usage: python benchmark.py {number} {proxy_addr} < url_file')
    return 1

  number = int(sys.argv[1])
  proxy_addr = sys.argv[2]
  urls = list(map(str.strip, sys.stdin.readlines()))
  
  with_proxy = run_benchmark(number, urls, proxy_addr)
  no_proxy = run_benchmark(number, urls)

  for url in urls:
    print("url: %s" % url)
    for n in range(number):
      print(with_proxy[url][n], no_proxy[url][n])

  return 0

def run_benchmark(
    number: int,
    urls: typing.List[str],
    proxy: typing.Optional[str] = None
    ) -> typing.Mapping[str, typing.List[int]]:
  time_data = {url: [] for url in urls}
  proxies = {}
  if proxy is not None:
    proxies['http'] = proxy

  for i in range(number):
    for url in urls:
      start_time = time.time()
      response = requests.get(url, proxies=proxies)
      end_time = time.time()
      elapsed = end_time - start_time
      time_data[url].append(elapsed)

  return time_data

if __name__ == '__main__':
  sys.exit(main())
