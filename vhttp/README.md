# vHTTP
## Vantage-Point based HTTP Proxy

vHTTP is an HTTP proxy server that checks for consensus among different vantage
points for a given request. In other words, any request proxied through vHTTP
is sent in turn to multiple different proxies (ideally, proxies that are
located in different geographical locations). These proxies are specified by
the server.

After receiving the responses from each proxy server, vHTTP will look for
consensus on content among the different responses. Consensus is defined as the
number of responses that share the same content. If this consensus passes a
server-specified threshold, then the response with greatest consensus is sent
back to the user.

Otherwise, the response is discarded and an error is returned. This mechanism
is used to circumvent Man-in-the-Middle attacks being performed at some point
along the request path. With HTTP, such MiTM attacks are easy to perform and
can have disastrous results

## Setup

vHTTP requires Python 3.5 or greater. Install dependencies with

```bash
λ cd vhttp
λ pipenv install
λ pipenv shell
λ cd ..
```

Run vHTTP:

```bash
λ python vhttp/server.py
```

### Docker

vHTTP can also be run with Docker:

```bash
λ cd vhttp
λ docker build . -t vhttp:latest
λ docker run --rm -p 7777:7777 vhttp:latest
```

## Example

We use the following HTTP proxies, which were available at the time of writing:

- http://128.68.150.9:53281, in Russia
- http://217.61.15.26:3128, in Italy
- http://88.99.151.121:3128, in Germany
- http://173.255.197.30:3128, in Dallas (United States)

We are requesting a simple install script, as such:

```bash
λ curl http://deis.io/deisctl/install.sh
```

For simplictiy of performing the MiTM, let us also add in a malicious proxy,
run with our `http-mitm` example. First, we run the malicious proxy:

```bash
λ docker run --rm -p 8081:8080 http-mitm:latest
```

First, with just the malicious proxy:

```bash
λ VHTTP_PROXIES=http://localhost:8081 python vhttp/server.py
```

With Docker, use

```bash
λ docker run --rm -p 7777:7777 -e VHTTP_PROXIES=http://localhost:8081 vhttp:latest
```

and make the actual request:

```bash
λ http_proxy=http://localhost:7777 curl http://deis.io/deisctl/install.sh
#!/bin/sh
# mitm/malicious.sh
# http-mitm
# Author: Rushy Panchal
# Date: December 22nd, 2017
# Description: "malicious" shell script.

echo "zucc"
```

Here, we don't get the actual script because of the malicious proxy. Now, we
add on the additional proxies:

```bash
λ export VHTTP_PROXIES=http://localhost:8081,http://128.68.150.9:53281,http://217.61.15.26:3128,http://173.255.197.30:3128,http://88.99.151.121:3128
λ python vhttp/server.py
```

With Docker, use

```bash
λ docker run --rm -p 7777:7777 -e VHTTP_PROXIES=http://localhost:8081,http://128.68.150.9:53281,http://217.61.15.26:3128,http://173.255.197.30:3128,http://88.99.151.121:3128 vhttp:latest
```

And again, the actual request:

```bash
λ http_proxy=http://localhost:7777 curl http://deis.io/deisctl/install.sh
#!/bin/sh

# install current version unless overridden by first command-line argument
VERSION=${1:-1.13.3}

...
```

Now, we get the actual script! The vHTTP server logs show that all except the
malicious proxy are in consensus about the contents.
