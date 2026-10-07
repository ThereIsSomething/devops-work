# Session 12: Ingress, ConfigMaps and Secrets

**Nitish Kumar Bhambu — 24BCS10589**

A ConfigMap stores ordinary configuration separately from the container image. This demo injects APP_MODE and WELCOME through envFrom. Environment values are read when the container starts; editing a ConfigMap does not automatically change an existing process environment.

A Secret is used for credential-like data. `secret.example.yaml` deliberately contains a public dummy value so this repository is reproducible. Real values must be supplied outside Git. The verification checks the injected value and prints only a success message. Base64 does not make a password safe to commit.

An Ingress is a routing specification. An Ingress controller watches it and configures a proxy/load balancer that handles requests. Creating an Ingress alone does not create a working router. This lab uses Traefik and a Host rule for `homework.local`; the backend is the web Service on port 80. Testing with only the IP and without the Host header would not match that rule.

The instructor's troubleshooting example is a trailing newline in a Secret. `echo "mypassword"` includes byte 0a; `printf %s "mypassword"` does not. The command blocks compares the base64 and byte output, then replaces a dummy Secret containing a newline with one without it. I checked the decoded bytes to find the newline.

```bash
kubectl -n homework-s12 get configmap,secret,ingress
kubectl -n homework-s12 describe ingress web
```

References: [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/), [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/), [Traefik installation](https://doc.traefik.io/traefik/setup/kubernetes/).

## Commands and output

Results from 7 October 2026. Build and diagnostic output is shortened.

### Ingress controller configuration

```bash
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

zephoryx@fedora$ kubectl get ingressclass
NAME      CONTROLLER                      PARAMETERS   AGE
traefik   traefik.io/ingress-controller   <none>       1s

zephoryx@fedora$ curl -f -H Host:homework.local http://127.0.0.1:18082
<h1>Welcome to nginx!</h1>
```

### Ingress routing check

```bash
zephoryx@fedora$ curl -f -H Host:homework.local http://127.0.0.1:18082
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 10 retries
Warning: left.

curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 9 retries left.
# ... intermediate output omitted ...
curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 2 retries left.

curl: (22) The requested URL returned error: 404
Warning: Problem (retrying all errors). Will retry in 1 second. 1 retry left.

curl: (22) The requested URL returned error: 404

zephoryx@fedora$ kubectl -n homework-s12 get ingress
NAME   CLASS     HOSTS            ADDRESS   PORTS   AGE
web    traefik   homework.local             80      8m49s
```

### Commands and results

```bash
zephoryx@fedora$ kubectl create namespace homework-s12
namespace/homework-s12 created

zephoryx@fedora$ kubectl -n homework-s12 apply -f 11-ingress-configmaps-secrets/configmap.yaml
configmap/app-config created

zephoryx@fedora$ kubectl -n homework-s12 apply -f 11-ingress-configmaps-secrets/secret.example.yaml
secret/demo-secret created

zephoryx@fedora$ kubectl -n homework-s12 apply -f 11-ingress-configmaps-secrets/app.yaml
deployment.apps/web created
service/web created

zephoryx@fedora$ kubectl -n homework-s12 rollout status deployment/web
Waiting for deployment "web" rollout to finish: 0 of 2 updated replicas are available...
Waiting for deployment "web" rollout to finish: 1 of 2 updated replicas are available...
deployment "web" successfully rolled out

zephoryx@fedora$ kubectl -n homework-s12 exec deployment/web -- sh -c 'printf "APP_MODE=%s\nWELCOME=%s\n" "$APP_MODE" "$WELCOME"; test "$DEMO_PASSWORD" = "classroom-example-only" && echo "Demo Secret injected: verified"'
APP_MODE=homework
WELCOME=Hello students
Demo Secret injected: verified

zephoryx@fedora$ kubectl -n homework-s12 apply -f 11-ingress-configmaps-secrets/ingress.yaml
ingress.networking.k8s.io/web created

zephoryx@fedora$ kubectl -n homework-s12 get ingress
NAME   CLASS     HOSTS            ADDRESS   PORTS   AGE
web    traefik   homework.local             80      1s

zephoryx@fedora$ kubectl -n homework-s12 run client --image=busybox:1.37 --restart=Never -- sleep 7200
pod/client created

zephoryx@fedora$ kubectl -n homework-s12 wait --for=condition=Ready pod/client
pod/client condition met

zephoryx@fedora$ kubectl -n homework-s12 exec client -- wget -qO- http://web
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ bash -c 'echo "mypassword" | base64; printf %s "mypassword" | base64; echo; echo "mypassword" | od -An -tx1; printf %s "mypassword" | od -An -tx1'
bXlwYXNzd29yZAo=
bXlwYXNzd29yZA==

 6d 79 70 61 73 73 77 6f 72 64 0a
 6d 79 70 61 73 73 77 6f 72 64

zephoryx@fedora$ kubectl -n homework-s12 create secret generic newline-demo '--from-literal=PASSWORD=mypassword
'
secret/newline-demo created

zephoryx@fedora$ kubectl -n homework-s12 get secret newline-demo -o 'jsonpath={.data.PASSWORD}'
bXlwYXNzd29yZAo=

zephoryx@fedora$ kubectl -n homework-s12 delete secret newline-demo
secret "newline-demo" deleted from homework-s12 namespace

zephoryx@fedora$ kubectl -n homework-s12 create secret generic newline-demo --from-literal=PASSWORD=mypassword
secret/newline-demo created

zephoryx@fedora$ kubectl -n homework-s12 get secret newline-demo -o 'jsonpath={.data.PASSWORD}'
bXlwYXNzd29yZA==
```
