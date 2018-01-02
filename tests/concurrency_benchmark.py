# tests/concurrencybenchmark.py
# vhttp
# Author: Rushy Panchal
# Date: December 31st, 2017
# Description: Benchmark with concurrent requests, using ab.

import subprocess
import os
import sys

def main() -> int:
  if len(sys.argv) < 7:
    print('Usage: python concurrency_benchmark.py {start} {end} {step} {output_folder} {proxy_addr} {url}')
    return 1

  con_start = int(sys.argv[1])
  con_end = int(sys.argv[2])
  con_step = int(sys.argv[3])
  output_folder = sys.argv[4]
  proxy_addr = sys.argv[5]
  url = sys.argv[6]

  aggregate = {}

  print('concurrency,50th,70th,75th')
  for i in range(con_start, con_end+1, con_step):
    output_file = os.path.join(output_folder, '%d.csv' % i)
    num_requests = i*10
    if num_requests < 100:
      num_requests = 100
    cmd = [
      'ab',
      '-e', output_file,
      '-n', str(num_requests),
      '-c', str(i),
      '-X', proxy_addr, # disable the -X option to benchmark the major server
      url
    ]
    result = subprocess.check_output(cmd)

    with open(output_file) as f:
      data = f.readlines()
      ms_50th = data[51].split(',')[1].strip()
      ms_70th = data[71].split(',')[1].strip()
      ms_75th = data[76].split(',')[1].strip()
      print(','.join([str(i), ms_50th, ms_70th, ms_75th]))

if __name__ == '__main__':
  sys.exit(main())
