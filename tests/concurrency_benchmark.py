# tests/concurrencybenchmark.py
# vhttp
# Author: Rushy Panchal
# Date: December 31st, 2017
# Description: Benchmark with concurrent requests, using ab.

import subprocess
import sys
import csv
import time
import os
import re

REQUEST_TIME_RE = re.compile(
  r'Time per request:\s+(?P<time>[0-9\.]+) \[ms\] \(mean\)')
REQUEST_TIME_CONCURRENT_RE = re.compile(
  r'Time per request:\s+(?P<time>[0-9\.]+) \[ms\] \(mean, across all concurrent requests\)')
REQUEST_RATE_RE = re.compile(
  r'Requests per second:\s+(?P<rate>[0-9\.]+) \[#/sec\] \(mean\)')

def main():
  if len(sys.argv) < 6:
    print('Usage: python concurrency_benchmark.py {start} {end} {step} {proxy_addr} {url}')
    return 1

  con_start = int(sys.argv[1])
  con_end = int(sys.argv[2])
  con_step = int(sys.argv[3])
  proxy_addr = sys.argv[4]
  url = sys.argv[5]

  output = csv.writer(sys.stdout)

  output.writerow(['concurrency', 'mean_ms', 'mean_concurrent_ms', 'rate_req_s'])
  for i in range(con_start, con_end+1, con_step):
    num_requests = max(1000, i*5)
    cmd = [
      'ab', # apache benchmark
      '-n', str(num_requests), # number of requests
      '-c', str(i), # concurrency
      '-s', '120', # timeout
      '-X', proxy_addr, # disable the -X option to proxy the main server
    ]

    sh_cmd = cmd.copy()

    cmd.append(url)
    sh_cmd.append(url)

    # Command must be sent as a string because of the header quoting.
    sys.stderr.write('%s\n\n' % ' '.join(sh_cmd))
    try:
      result = subprocess.check_output(cmd, stderr=subprocess.PIPE).decode('utf8')
    except subprocess.CalledProcessError:
      sys.stderr.write('%d failed\n' % i)
      output.writerow([i, 0, 0, 0])
      # Server is probably overloaded, so back off a bit.
      time.sleep(4)
    else:
      if 'Non-2xx Responses' in result:
        sys.stderr.write('%s\n' % result)
        sys.stderr.write('%d failed\n' % i)
        output.writerow([i, 0, 0, 0])
      else:
        mean_time = REQUEST_TIME_RE.search(result)
        mean_time_concurrent = REQUEST_TIME_CONCURRENT_RE.search(result)
        req_rate = REQUEST_RATE_RE.search(result)

        if not (mean_time and mean_time_concurrent and req_rate):
          sys.stderr.write('%d failed\n' % i)
          output.writerow([i, 0, 0, 0])
        else:
          mean_time_ms = mean_time.group('time')
          mean_time_c_ms = mean_time_concurrent.group('time')
          req_rate_s = req_rate.group('rate')
          sys.stderr.write('%d: %s %s %s\n' % (i, mean_time_ms, mean_time_c_ms, req_rate_s))
          output.writerow([i, mean_time_ms, mean_time_c_ms, req_rate_s])

    # Give the server time to clear up any backlog, if created.
    time.sleep(1)

  return 0

if __name__ == '__main__':
  sys.exit(main())
