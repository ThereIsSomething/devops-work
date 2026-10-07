# Session 6: Docker Fundamentals

**Nitish Kumar Bhambu — 24BCS10589**

Each required folder contains its application and Dockerfile. The runner builds all six images, starts named containers and verifies their responses. Ports bind to localhost for this lab.

| Folder | Implementation | Host URL |
|---|---|---|
| nodejs-app | Node HTTP server | http://localhost:3001 |
| python-app | Flask | http://localhost:3002 |
| java-app | Java HTTP server | http://localhost:3003 |
| Apache-app | Static HTML on Apache httpd | http://localhost:3004 |
| React-app | Vite/React build served by Nginx | http://localhost:3005 |
| nginx-app | Static HTML on Nginx | http://localhost:3006 |

A React page is rendered by the browser from a JavaScript bundle. Curl verifies the entry HTML and the bundle's Hello/World strings; it does not execute React. The other five responses contain the rendered message directly. A successful image build alone is not sufficient: the run checks HTTP and lists the running containers.

```bash
python3 scripts/run_basics.py 6
```

## Execution evidence

<!-- EVIDENCE -->

### current-run.txt

[Complete transcript](outputs/current-run.txt)

````text
Captured 2026-10-07T13:02:10.819004+00:00
$ docker rm -f homework-hello-nodejs
homework-hello-nodejs
[exit 0]
$ docker build -t homework-hello-nodejs 05-docker-fundamentals/nodejs-app
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 901B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/node:24-alpine
#2 DONE 1.2s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [internal] load build context
#4 DONE 0.0s

#5 [1/6] FROM docker.io/library/node:24-alpine@sha256:ebfe2f90462722a7a4de65e91990e97fe0d401c70e0e762c5b53302f905ec1c1
#5 resolve docker.io/library/node:24-alpine@sha256:ebfe2f90462722a7a4de65e91990e97fe0d401c70e0e762c5b53302f905ec1c1 0.1s done
#5 DONE 0.1s

#4 [internal] load build context
#4 transferring context: 181B done
#4 DONE 0.0s

#6 [2/6] WORKDIR /app
#6 CACHED

#7 [3/6] COPY package.json ./
#7 CACHED

#8 [4/6] RUN npm install --omit=dev && npm cache clean --force
#8 CACHED

#9 [5/6] COPY server.js ./
#9 CACHED

#10 [6/6] RUN addgroup -S app && adduser -S app -G app && chown -R app:app /app
#10 CACHED

#11 exporting to image
#11 exporting layers 0.0s done
#11 exporting manifest sha256:7bd284b4f5e03ce64e3032b4c1ddddbffa897d55d113dcb9255c4f52ea289aab done
#11 exporting config sha256:e8f2e0e41252869ba3c1dbf51605d1951378a568e1a1d1a64a77755bd1ae2b9b done
#11 exporting attestation manifest sha256:5371bb2c3dcf5c192ddd27bebdb225aef185e31d8919d32e30d7a3f68c2de60d 0.0s done
#11 exporting manifest list sha256:5fed384ebcbbd0d4e2b5a3ff32eb09719ce54ec50e4e60077ef8b8b77f323aea 0.0s done
#11 naming to docker.io/library/homework-hello-nodejs:latest done
#11 unpacking to docker.io/library/homework-hello-nodejs:latest 0.0s done
#11 DONE 0.2s
[exit 0]
$ docker run -d --name homework-hello-nodejs -p 127.0.0.1:3001:3000 homework-hello-nodejs
e263e2c615c21bd9176ca2e08dd8103f781c3b9cec2c0cd4da910d6e9d2b7fd4
[exit 0]
$ curl --retry 30 --retry-all-errors --retry-connrefused --retry-delay 1 --fail http://127.0.0.1:3001
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0
curl: (56) Recv failure: Connection reset by peer
Warning: Problem (retrying all errors). Will retry in 1 second. 30 retries
Warning: left.

[Excerpt: 961 intermediate lines omitted; complete transcript linked above.]


#9 exporting to image
#9 exporting layers 0.1s done
#9 exporting manifest sha256:50f37f2c57e6542f39f89fc8e51684f222a03dcdb13a5b31773c1c5f1b1cc564 done
#9 exporting config sha256:a75535bd1bb1ffadd54de838de5d4ff42bb7fc4499b78d7e7c5911a400a52093 done
#9 exporting attestation manifest sha256:2b85829250f840a8577573afdc9821881175fbc805bc84eccc08f6cd1230a3da done
#9 exporting manifest list sha256:79378eaec73afef1ade1c350645f0ef03fa4d1c33aae2d193dda67637517e654 done
#9 naming to docker.io/library/homework-hello-nginx:latest done
#9 unpacking to docker.io/library/homework-hello-nginx:latest 0.0s done
#9 DONE 0.1s
[exit 0]
$ docker run -d --name homework-hello-nginx -p 127.0.0.1:3006:80 homework-hello-nginx
9faa0cfec7cc02645371c9641921bb67ebb405cfeb810f9ceb9fd581a970ac7e
[exit 0]
$ curl --retry 30 --retry-all-errors --retry-connrefused --retry-delay 1 --fail http://127.0.0.1:3006
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0
curl: (56) Recv failure: Connection reset by peer
Warning: Problem (retrying all errors). Will retry in 1 second. 30 retries
Warning: left.

  0      0   0      0   0      0      0      0                              0
100   2050 100   2050   0      0  2.79M      0                              0
100   2050 100   2050   0      0  2.72M      0                              0
100   2050 100   2050   0      0  2.65M      0                              0
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Hello World — Nginx</title>
  <style>
    :root{--bg:#0f1117;--card:#171a23;--line:#252a38;--fg:#e6e9f0;--muted:#8b93a7;--accent:#00b04f}
    *{margin:0;padding:0;box-sizing:border-box}
    body{background:var(--bg);color:var(--fg);min-height:100vh;display:grid;place-items:center;
      font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px}
    .card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:44px 52px;
      max-width:560px;width:100%;box-shadow:0 24px 60px rgba(0,0,0,.5)}
    .badge{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:600;
      letter-spacing:.08em;text-transform:uppercase;color:var(--accent);
      background:rgba(0,176,79,.14);border:1px solid rgba(0,176,79,.3);
      padding:6px 12px;border-radius:999px;margin-bottom:22px}
    h1{font-size:44px;line-height:1.1;letter-spacing:-.02em;margin-bottom:10px}
    h1 span{color:var(--accent)}
    .sub{color:var(--muted);font-size:15px;margin-bottom:28px}
    dl{display:grid;grid-template-columns:auto 1fr;gap:10px 18px;font-size:14px;
      border-top:1px solid var(--line);padding-top:22px}
    dt{color:var(--muted)}
    dd{font-family:ui-monospace,'SF Mono',Menlo,monospace}
    .foot{margin-top:24px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}
  </style>
</head>
<body>
  <div class="card">
    <div class="badge">● Nginx</div>
    <h1>Hello <span>World</span></h1>
    <p class="sub">Static page served by the Nginx web server inside a Docker container.</p>
    <dl>
      <dt>Server</dt><dd>nginx (alpine)</dd>
      <dt>Serving</dt><dd>/usr/share/nginx/html</dd>
      <dt>Port</dt><dd>80 &rarr; published on 3006</dd>
      <dt>Type</dt><dd>static content</dd>
    </dl>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>
  </div>
</body>
</html>
[exit 0]
$ docker ps --filter name=homework-hello --format 'table {{.Names}}	{{.Status}}	{{.Ports}}'
NAMES                   STATUS                            PORTS
homework-hello-nginx    Up 1 second (health: starting)    127.0.0.1:3006->80/tcp
homework-hello-react    Up 4 seconds (health: starting)   127.0.0.1:3005->80/tcp
homework-hello-apache   Up About a minute (healthy)       127.0.0.1:3004->80/tcp
homework-hello-java     Up About a minute (healthy)       127.0.0.1:3003->8080/tcp
homework-hello-python   Up 6 minutes (healthy)            127.0.0.1:3002->5000/tcp
homework-hello-nodejs   Up 7 minutes (healthy)            127.0.0.1:3001->3000/tcp
[exit 0]
LAB EXECUTION FINISHED
````
