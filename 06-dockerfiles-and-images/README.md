# Session 7: Docker Images and Multi-stage Builds

**Nitish Kumar Bhambu — 24BCS10589**

The [Go app](multistage-app/) compiles in a Go builder image, then copies the executable into a scratch runtime image. The final image contains the program rather than the compiler and source tree. The binary is static because scratch has no libc or shell.

The run verifies the exact message **Hello World from Docker multi-stage build**, shows docker ps and the published port **8080**, and records the image size/user. The three required application types—Node.js, Python and Java—are built in Session 6 and verified again in this session's command blocks.

```bash
docker build -t homework-multistage 06-dockerfiles-and-images/multistage-app
docker run -d --name homework-multistage -p 8080:8080 homework-multistage
docker ps
```

## Commands and output

### Multi-stage image

```bash
zephoryx@fedora$ docker build -t homework-multistage 06-dockerfiles-and-images/multistage-app
# ... build output shortened ...
#12 naming to docker.io/library/homework-multistage:latest done
#12 unpacking to docker.io/library/homework-multistage:latest 0.1s done
#12 DONE 0.3s
```

### Application, port and runtime user

```bash
zephoryx@fedora$ curl -fsS http://127.0.0.1:8080 | sed -n '/<h1>/p; /class="foot"/p'
<h1>Hello World from Docker multi-stage build</h1>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>

zephoryx@fedora$ docker ps --filter name=homework-multistage --format 'table {{.Names}}	{{.Status}}	{{.Ports}}'
NAMES                 STATUS       PORTS
homework-multistage   Up 2 hours   127.0.0.1:8080->8080/tcp

zephoryx@fedora$ docker port homework-multistage
8080/tcp -> 127.0.0.1:8080

zephoryx@fedora$ docker image inspect homework-multistage --format '{{.Size}} bytes; user={{.Config.User}}'
8251958 bytes; user=65534
```

### Three different application types

```bash
zephoryx@fedora$ curl -fsS http://127.0.0.1:3001 | sed -n '/<h1>/p'
<h1>Hello <span>World</span></h1>

zephoryx@fedora$ curl -fsS http://127.0.0.1:3002 | sed -n '/<h1>/p'
<h1>Hello <span>World</span></h1>

zephoryx@fedora$ curl -fsS http://127.0.0.1:3003 | sed -n '/<h1>/p'
<h1>Hello <span>World</span></h1>
```
