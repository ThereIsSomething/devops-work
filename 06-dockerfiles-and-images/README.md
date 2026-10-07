# Session 7: Docker Images and Multi-stage Builds

**Nitish Kumar Bhambu — 24BCS10589**

The [Go app](multistage-app/) compiles in a Go builder image, then copies the executable into a scratch runtime image. The final image contains the program rather than the compiler and source tree. A static executable is required because scratch has no libc or shell. A smaller runtime still needs the application itself to be maintained; it is not automatically vulnerability-free.

The run verifies the exact message **Hello World from Docker multi-stage build**, shows docker ps and the published port **8080**, and records the image size/user. The source is already in this Git checkout; no separate multi-stage repository URL was supplied in the assignment. The three required application types—Node.js, Python and Java—are built in Session 6 and verified again in this session's transcript.

```bash
python3 scripts/run_basics.py 7
```

## Execution evidence

<!-- EVIDENCE -->

### current-run.txt

[Complete transcript](outputs/current-run.txt)

````text
Captured 2026-10-07T13:10:01.829376+00:00
$ docker build -t homework-multistage 06-dockerfiles-and-images/multistage-app
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 1.70kB done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/golang:1.26-alpine
#2 DONE 2.2s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [builder 1/6] FROM docker.io/library/golang:1.26-alpine@sha256:8ac98ca534ac3f51e1f420a1dd2c15e74c75cfa0f23f3ad27eb5d7236c349a0c
#4 resolve docker.io/library/golang:1.26-alpine@sha256:8ac98ca534ac3f51e1f420a1dd2c15e74c75cfa0f23f3ad27eb5d7236c349a0c 0.0s done
#4 CACHED

#5 [internal] load build context
#5 transferring context: 3.55kB done
#5 DONE 0.0s

#6 [builder 2/6] WORKDIR /build
#6 DONE 0.1s

#7 [builder 3/6] COPY go.mod ./
#7 DONE 0.1s

#8 [builder 4/6] RUN go mod download
#8 0.181 go: no module dependencies to download
#8 DONE 0.2s

#9 [builder 5/6] COPY main.go ./
#9 DONE 0.1s

#10 [builder 6/6] RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server main.go
#10 DONE 6.0s

#11 [stage-1 1/1] COPY --from=builder /app/server /server
#11 DONE 0.0s

#12 exporting to image
#12 exporting layers
#12 exporting layers 0.2s done
#12 exporting manifest sha256:b1f86faf26b2c1d8199a92c6457c78e601d5826a275db4c95c7f5659ddde27c1 done
#12 exporting config sha256:32632fb251d5341e323cfc123035cde3b49f5d0da8ab597d043c871a7a60d04d done
#12 exporting attestation manifest sha256:90559b402be1a8dfe995c7dc6424020150e54e9a104e14f4f5e8466f55356b24 done
#12 exporting manifest list sha256:6bbb761c1dcfc1eaca49383ea8646a0e1d0e2a918298c88075c969faaadd8fae done
#12 naming to docker.io/library/homework-multistage:latest done
#12 unpacking to docker.io/library/homework-multistage:latest 0.1s done
#12 DONE 0.3s
[exit 0]
$ docker run -d --name homework-multistage -p 127.0.0.1:8080:8080 homework-multistage
8d81f17bb0aa3c3f57abb1211e01f370ffb403d2ff347b93371f311536574030
[exit 0]
$ curl --retry 20 --retry-all-errors --retry-connrefused --retry-delay 1 --fail http://127.0.0.1:8080
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0
100   2017 100   2017   0      0  2.74M      0                              0
100   2017 100   2017   0      0  2.67M      0                              0
100   2017 100   2017   0      0  2.61M      0                              0
<!doctype html>

[Excerpt: 129 intermediate lines omitted; complete transcript linked above.]

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
    <div class="badge">● Python / Flask</div>
    <h1>Hello <span>World</span></h1>
    <p class="sub">Served by a Flask application running inside a Docker container.</p>
    <dl>
      <dt>Runtime</dt><dd>Python 3.12.15</dd>
      <dt>Framework</dt><dd>Flask</dd>
      <dt>Platform</dt><dd>Linux / x86_64</dd>
      <dt>Container</dt><dd>c6ec46df0904</dd>
      <dt>Port</dt><dd>5000</dd>
    </dl>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>
  </div>
</body>
</html>
[exit 0]
$ curl --fail http://127.0.0.1:3003
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0
100   1997 100   1997   0      0 653.7k      0                              0
100   1997 100   1997   0      0 649.1k      0                              0
100   1997 100   1997   0      0 644.4k      0                              0
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Hello World — Java</title>
  <style>:root{--bg:#0f1117;--card:#171a23;--line:#252a38;--fg:#e6e9f0;--muted:#8b93a7;--accent:#f89820}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--fg);min-height:100vh;display:grid;place-items:center;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:44px 52px;
  max-width:560px;width:100%;box-shadow:0 24px 60px rgba(0,0,0,.5)}
.badge{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:600;
  letter-spacing:.08em;text-transform:uppercase;color:var(--accent);
  background:rgba(248,152,32,.14);border:1px solid rgba(248,152,32,.3);
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
    <div class="badge">● Java</div>
    <h1>Hello <span>World</span></h1>
    <p class="sub">Served by a Java HTTP server running inside a Docker container.</p>
    <dl>
      <dt>Runtime</dt><dd>Java 21.0.12.1</dd>
      <dt>JVM</dt><dd>OpenJDK 64-Bit Server VM</dd>
      <dt>Platform</dt><dd>Linux / amd64</dd>
      <dt>Container</dt><dd>ceceb6eb2bc4</dd>
      <dt>Port</dt><dd>8080</dd>
    </dl>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>
  </div>
</body>
</html>
[exit 0]
LAB EXECUTION FINISHED
````

### identity-build.txt

[Complete transcript](outputs/identity-build.txt)

````text
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 1.71kB done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/golang:1.26-alpine
#2 DONE 0.8s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [builder 1/6] FROM docker.io/library/golang:1.26-alpine@sha256:8ac98ca534ac3f51e1f420a1dd2c15e74c75cfa0f23f3ad27eb5d7236c349a0c
#4 resolve docker.io/library/golang:1.26-alpine@sha256:8ac98ca534ac3f51e1f420a1dd2c15e74c75cfa0f23f3ad27eb5d7236c349a0c 0.0s done
#4 DONE 0.0s

#5 [internal] load build context
#5 transferring context: 3.52kB done
#5 DONE 0.0s

#6 [builder 2/6] WORKDIR /build
#6 CACHED

#7 [builder 3/6] COPY go.mod ./
#7 CACHED

#8 [builder 4/6] RUN go mod download
#8 CACHED

#9 [builder 5/6] COPY main.go ./
#9 DONE 0.1s

#10 [builder 6/6] RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /app/server main.go
#10 DONE 6.0s

#11 [stage-1 1/1] COPY --from=builder /app/server /server
#11 DONE 0.0s

#12 exporting to image
#12 exporting layers
#12 exporting layers 0.2s done
#12 exporting manifest sha256:ca8013364dddb0b220967f58fa25e44616f9e72ef77136a657261b826faec02a done
#12 exporting config sha256:f1eaf7aa7e3484c7d349e4eebe01e8b84e0f5a4a0ce256fec99aeea633370fb3 done
#12 exporting attestation manifest sha256:4b5722aa2f4785a4eae72ee6c94b0dca3febba2df1260b904ba987e7639658ec done
#12 exporting manifest list sha256:6a55a3542b6eac25059e9ce6a708b0fe52b8763cc6aba8fed12a8867f4d632e4 done
#12 naming to docker.io/library/homework-multistage:latest done
#12 unpacking to docker.io/library/homework-multistage:latest 0.1s done
#12 DONE 0.3s
````

### identity-page.txt

[Complete transcript](outputs/identity-page.txt)

````text
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0
100   2025 100   2025   0      0  1.71M      0                              0
100   2025 100   2025   0      0  1.55M      0                              0
100   2025 100   2025   0      0  1.44M      0                              0
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Docker Multi-Stage Build</title>
  <style>
:root{--bg:#0f1117;--card:#171a23;--line:#252a38;--fg:#e6e9f0;--muted:#8b93a7;--accent:#00add8}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--fg);min-height:100vh;display:grid;place-items:center;
  font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;padding:24px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:44px 52px;
  max-width:640px;width:100%;box-shadow:0 24px 60px rgba(0,0,0,.5)}
.badge{display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:600;
  letter-spacing:.08em;text-transform:uppercase;color:var(--accent);
  background:rgba(0,173,216,.14);border:1px solid rgba(0,173,216,.3);
  padding:6px 12px;border-radius:999px;margin-bottom:22px}
h1{font-size:34px;line-height:1.2;letter-spacing:-.02em;margin-bottom:14px}
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
    <div class="badge">● Multi-Stage Build</div>
    <h1>Hello World from Docker multi-stage build</h1>
    <p class="sub">A static Go binary in a scratch-based image &mdash; no compiler, no OS, no shell.</p>
    <dl>
      <dt>Language</dt><dd>go1.26.8</dd>
      <dt>Platform</dt><dd>linux / amd64</dd>
      <dt>Container</dt><dd>a85a62432ef2</dd>
      <dt>Port</dt><dd>8080</dd>
      <dt>Uptime</dt><dd>0.0s</dd>
    </dl>
    <p class="foot">Nitish Kumar Bhambu &middot; 24BCS10589 &middot; DevOps Homework</p>
  </div>
</body>
</html>
````
