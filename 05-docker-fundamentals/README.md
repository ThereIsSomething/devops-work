# Session 6: Docker Fundamentals

**Nitish Kumar Bhambu — 24BCS10589**

Each required folder contains its application and Dockerfile. I built all six images, started named containers and checked their HTTP responses. Ports bind to localhost for this lab.

| Folder | Implementation | Host URL |
|---|---|---|
| nodejs-app | Node HTTP server | http://localhost:3001 |
| python-app | Flask | http://localhost:3002 |
| java-app | Java HTTP server | http://localhost:3003 |
| Apache-app | Static HTML on Apache httpd | http://localhost:3004 |
| React-app | Vite/React build served by Nginx | http://localhost:3005 |
| nginx-app | Static HTML on Nginx | http://localhost:3006 |

A React page is rendered by the browser from a JavaScript bundle. Curl verifies the entry HTML and the bundle's Hello/World strings; it does not execute React. The other five responses contain the rendered message directly. I checked the HTTP responses and running containers.

```bash
docker build -t homework-hello-nodejs 05-docker-fundamentals/nodejs-app
docker run -d --name homework-hello-nodejs -p 3001:3000 homework-hello-nodejs
curl http://localhost:3001
```

## Commands and output

### Commands and results

```bash
zephoryx@fedora$ docker build -t homework-hello-nodejs 05-docker-fundamentals/nodejs-app
# ... build output shortened ...
#11 unpacking to docker.io/library/homework-hello-nodejs:latest 0.0s done
#11 DONE 0.2s

zephoryx@fedora$ docker run -d --name homework-hello-nodejs -p 127.0.0.1:3001:3000 homework-hello-nodejs
e263e2c615c21bd9176ca2e08dd8103f781c3b9cec2c0cd4da910d6e9d2b7fd4

zephoryx@fedora$ curl -f http://127.0.0.1:3001
<h1>Hello <span>World</span></h1>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>

zephoryx@fedora$ docker build -t homework-hello-python 05-docker-fundamentals/python-app
# ... build output shortened ...
#11 unpacking to docker.io/library/homework-hello-python:latest 1.6s done
#11 DONE 2.5s

zephoryx@fedora$ docker run -d --name homework-hello-python -p 127.0.0.1:3002:5000 homework-hello-python
c6ec46df0904ae98d9158d52a535819c82e0a345c96394d53e0f876d37c06b75

zephoryx@fedora$ curl -f http://127.0.0.1:3002
<h1>Hello <span>World</span></h1>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>

zephoryx@fedora$ docker build -t homework-hello-java 05-docker-fundamentals/java-app
# ... build output shortened ...
#14 unpacking to docker.io/library/homework-hello-java:latest 2.3s done
#14 DONE 2.5s

zephoryx@fedora$ docker run -d --name homework-hello-java -p 127.0.0.1:3003:8080 homework-hello-java
ceceb6eb2bc4e9911f1fefb0d952e80ef3331cb68fb5c6b374fbb313b15888d4

zephoryx@fedora$ curl -f http://127.0.0.1:3003
<h1>Hello <span>World</span></h1>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>

zephoryx@fedora$ docker build -t homework-hello-apache 05-docker-fundamentals/Apache-app
# ... build output shortened ...
#8 unpacking to docker.io/library/homework-hello-apache:latest 0.4s done
#8 DONE 0.5s

zephoryx@fedora$ docker run -d --name homework-hello-apache -p 127.0.0.1:3004:80 homework-hello-apache
dee5a64137283cd9ceea5452e618659df13d08d1e6aa181a5d1d12828dc646a9

zephoryx@fedora$ curl -f http://127.0.0.1:3004
<h1>Hello <span>World</span></h1>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>

zephoryx@fedora$ docker build -t homework-hello-react 05-docker-fundamentals/React-app
# ... build output shortened ...
#17 unpacking to docker.io/library/homework-hello-react:latest 0.5s done
#17 DONE 0.7s

zephoryx@fedora$ docker run -d --name homework-hello-react -p 127.0.0.1:3005:80 homework-hello-react
5ce789187d1e9f085f314341e7cc71801bafa33c70bec5971ab532ce48cee76a

zephoryx@fedora$ curl -f http://127.0.0.1:3005
curl: (56) Recv failure: Connection reset by peer
Warning: Problem (retrying all errors). Will retry in 1 second. 30 retries
Warning: left.

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Hello World — React</title>
    <script type="module" crossorigin src="/assets/index-BfCIXmL_.js"></script>
    <link rel="stylesheet" crossorigin href="/assets/index-B2s8ZJlT.css">
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>

zephoryx@fedora$ curl -f [React JavaScript bundle]
React bundle contains Hello/World: True

zephoryx@fedora$ docker build -t homework-hello-nginx 05-docker-fundamentals/nginx-app
# ... build output shortened ...
#9 unpacking to docker.io/library/homework-hello-nginx:latest 0.0s done
#9 DONE 0.1s

zephoryx@fedora$ docker run -d --name homework-hello-nginx -p 127.0.0.1:3006:80 homework-hello-nginx
9faa0cfec7cc02645371c9641921bb67ebb405cfeb810f9ceb9fd581a970ac7e

zephoryx@fedora$ curl -f http://127.0.0.1:3006
<h1>Hello <span>World</span></h1>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>

zephoryx@fedora$ docker ps --filter name=homework-hello --format 'table {{.Names}}	{{.Status}}	{{.Ports}}'
NAMES                   STATUS                            PORTS
homework-hello-nginx    Up 1 second (health: starting)    127.0.0.1:3006->80/tcp
homework-hello-react    Up 4 seconds (health: starting)   127.0.0.1:3005->80/tcp
homework-hello-apache   Up About a minute (healthy)       127.0.0.1:3004->80/tcp
homework-hello-java     Up About a minute (healthy)       127.0.0.1:3003->8080/tcp
homework-hello-python   Up 6 minutes (healthy)            127.0.0.1:3002->5000/tcp
homework-hello-nodejs   Up 7 minutes (healthy)            127.0.0.1:3001->3000/tcp
```

### HTTP response checks

```bash
zephoryx@fedora$ curl -fsS http://127.0.0.1:3001 | sed -n '/<h1>/p'
<h1>Hello <span>World</span></h1>

zephoryx@fedora$ curl -fsS http://127.0.0.1:3002 | sed -n '/<h1>/p'
<h1>Hello <span>World</span></h1>

zephoryx@fedora$ curl -fsS http://127.0.0.1:3003 | sed -n '/<h1>/p'
<h1>Hello <span>World</span></h1>

zephoryx@fedora$ curl -fsS http://127.0.0.1:3004 | sed -n '/<h1>/p'
<h1>Hello <span>World</span></h1>

zephoryx@fedora$ curl -fsS http://127.0.0.1:3006 | sed -n '/<h1>/p'
<h1>Hello <span>World</span></h1>
```
