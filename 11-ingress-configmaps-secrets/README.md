# Session 12: Ingress, ConfigMaps and Secrets

**Nitish Kumar Bhambu — 24BCS10589**

A ConfigMap stores ordinary configuration separately from the container image. This demo injects APP_MODE and WELCOME through envFrom. Environment values are read when the container starts; editing a ConfigMap does not automatically change an existing process environment.

A Secret is used for credential-like data. `secret.example.yaml` deliberately contains a public dummy value so this repository is reproducible. Real values must be supplied outside Git. The verification checks the injected value and prints only a success message. Base64 does not make a password safe to commit.

An Ingress is a routing specification. An Ingress controller watches it and configures a proxy/load balancer that handles requests. Creating an Ingress alone does not create a working router. This lab uses Traefik and a Host rule for `homework.local`; the backend is the web Service on port 80. Testing with only the IP and without the Host header would not match that rule.

The instructor's troubleshooting example is a trailing newline in a Secret. `echo "mypassword"` includes byte 0a; `printf %s "mypassword"` does not. The transcript compares the base64 and byte output, then replaces a dummy Secret containing a newline with one without it. Matching padding is not a general test for this bug: inspect decoded bytes or length.

```bash
python3 scripts/run_kubernetes_labs.py 12
# Controller installation and routed request are recorded separately.
```

References: [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/), [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/), [Traefik installation](https://doc.traefik.io/traefik/setup/kubernetes/).

## Execution evidence

Actual local transcripts are included below after the runs finish. A missing or incomplete transcript is not a completed exercise.

<!-- EVIDENCE -->

### controller-fix.txt

[Complete transcript](outputs/controller-fix.txt)

````text
Release "homework-ingress" has been upgraded. Happy Helming!
NAME: homework-ingress
LAST DEPLOYED: Wed Oct  7 18:33:13 2026
NAMESPACE: homework-ingress
STATUS: deployed
REVISION: 2
DESCRIPTION: Upgrade complete
TEST SUITE: None
NOTES:
homework-ingress with docker.io/traefik:v3.7.13 has been deployed successfully on homework-ingress namespace!
$ scripts/kubectl get ingressclass
NAME      CONTROLLER                      PARAMETERS   AGE
traefik   traefik.io/ingress-controller   <none>       1s
$ curl --fail -H Host:homework.local http://127.0.0.1:18082
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0
100    615 100    615   0      0  73732      0                              0
100    615 100    615   0      0  68768      0                              0
100    615 100    615   0      0  65044      0                              0
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
````

### ingress-routing.txt

[Complete transcript](outputs/ingress-routing.txt)

````text
$ curl --fail -H Host:homework.local http://127.0.0.1:18082
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 10 retries
Warning: left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 9 retries left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 8 retries left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 7 retries left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 6 retries left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 5 retries left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 4 retries left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 3 retries left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 2 retries left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 1 retry left.

  0      0   0      0   0      0      0      0                              0
curl: (22) The requested URL returned error: 404

$ scripts/kubectl -n homework-s12 get ingress
NAME   CLASS     HOSTS            ADDRESS   PORTS   AGE
web    traefik   homework.local             80      8m49s
````

### run.txt

[Complete transcript](outputs/run.txt)

````text
Captured 2026-10-07T12:53:30.318228+00:00
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' create namespace homework-s12
namespace/homework-s12 created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 apply -f 11-ingress-configmaps-secrets/configmap.yaml
configmap/app-config created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 apply -f 11-ingress-configmaps-secrets/secret.example.yaml
secret/demo-secret created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 apply -f 11-ingress-configmaps-secrets/app.yaml
deployment.apps/web created
service/web created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 rollout status deployment/web --timeout=180s
Waiting for deployment "web" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "web" rollout to finish: 1 of 2 updated replicas are available...
deployment "web" successfully rolled out
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 exec deployment/web -- sh -c 'printf "APP_MODE=%s\nWELCOME=%s\n" "$APP_MODE" "$WELCOME"; test "$DEMO_PASSWORD" = "classroom-example-only" && echo "Demo Secret injected: verified"'
APP_MODE=homework
WELCOME=Hello students
Demo Secret injected: verified
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 apply -f 11-ingress-configmaps-secrets/ingress.yaml
ingress.networking.k8s.io/web created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 get ingress
NAME   CLASS     HOSTS            ADDRESS   PORTS   AGE
web    traefik   homework.local             80      1s
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 wait --for=condition=Ready pod/client --timeout=120s
pod/client condition met
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 exec client -- wget -qO- http://web
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
[exit 0]
$ bash -c 'echo "mypassword" | base64; printf %s "mypassword" | base64; echo; echo "mypassword" | od -An -tx1; printf %s "mypassword" | od -An -tx1'
bXlwYXNzd29yZAo=
bXlwYXNzd29yZA==

 6d 79 70 61 73 73 77 6f 72 64 0a
 6d 79 70 61 73 73 77 6f 72 64
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 create secret generic newline-demo '--from-literal=PASSWORD=mypassword
'
secret/newline-demo created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 get secret newline-demo -o 'jsonpath={.data.PASSWORD}'
bXlwYXNzd29yZAo=
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 delete secret newline-demo
secret "newline-demo" deleted from homework-s12 namespace
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 create secret generic newline-demo --from-literal=PASSWORD=mypassword
secret/newline-demo created
[exit 0]
$ '/home/zephoryx/Documents/Academics/SST/TERM - IX/DevOps/devops-work/scripts/kubectl' -n homework-s12 get secret newline-demo -o 'jsonpath={.data.PASSWORD}'
bXlwYXNzd29yZA==
[exit 0]
LAB EXECUTION FINISHED
````
