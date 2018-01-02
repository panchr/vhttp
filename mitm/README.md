# http-mitm
## Perform a HTTP MITM attack for installation scripts.

## Docker
If you have Docker installed, you can run the http-mitm attack as follows:

```sh
docker build . -t http-mitm:latest
docker run --rm -p 8080:8080 http-mitm:latest
```

Alternatively, `sh bin/proxy.sh` will also build and run the image.

Now, you can view the effects of the man-in-the-middle attack by making a
request that proxies through this server:

```sh
λ http_proxy=http://localhost:8080 curl http://example.com/test.sh
```

To kill the container, find out the name using `docker ps` and kill it with
`docker kill {name}`:

```sh
λ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                              NAMES
cd5e1371e502        http-mitm:latest    "docker-entrypoint..."   9 minutes ago       Up 9 minutes        0.0.0.0:8080->8080/tcp, 8081/tcp   confident_montalcini
λ docker kill confident_montalcini
```

### Tests
Tests can be run with Docker. First, build the test image:

```sh
docker build . -f tests/Dockerfile -t http-mitm:test
```

then run the test container:

```sh
docker run --rm http-mitm:test
```

## Without Docker

Make sure you have the [`mitmdump` tool](https://mitmproxy.org.) installed.
Run `sh bin/proxy.sh` to start the server.

### Tests

Without Docker, some tests can be run with `sh bin/test.sh`.
