# http-mitm
## Perform an HTTP MITM attack for installation scripts.

# Docker
If you have Docker installed, you can run the http-mitm attack as follows:

```sh
docker build . -t http-mitm:latest
docker run --rm -p 8080:8080 http-mitm:latest
```

Alternatively, `sh proxy.sh` will also build and run the image.

To kill the container, find out the name using `docker ps` and kill it with
`docker kill {name}`:

```sh
λ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                              NAMES
cd5e1371e502        http-mitm:latest    "docker-entrypoint..."   9 minutes ago       Up 9 minutes        0.0.0.0:8080->8080/tcp, 8081/tcp   confident_montalcini
λ docker kill confident_montalcini
```
