# tests/mock_server.py
# vhttp
# Author: Rushy Panchal
# Date: January 2nd, 2017
# Description: Mock HTTP Server with two endpoints.

import asyncio
import sys

import aiohttp
import aiohttp.web

def main():
  if len(sys.argv) < 3:
    print("Usage: python mock_server.py {host} {port}")
    return 1

  host = sys.argv[1]
  port = int(sys.argv[2])

  loop = asyncio.get_event_loop()
  proxy_server = aiohttp.web.Server(handler)
  server = loop.create_server(proxy_server, host, port)
  loop.run_until_complete(server)
  loop.run_forever()
  return 1

async def handler(request: aiohttp.web.Request) -> aiohttp.web.Response:
  await asyncio.sleep(3)
  return aiohttp.web.Response(body=b'Done!')

if __name__ == '__main__':
  sys.exit(main())
