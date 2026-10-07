# Session 8: Docker Networking and Volumes

**Nitish Kumar Bhambu — 24BCS10589**

The exercise creates three bridge networks: homework-front, homework-back and homework-isolated. The Nginx frontend joins the front network, MySQL joins the back network, and the Alpine backend joins both. The third network is intentionally separate. The backend tests HTTP to the frontend and TCP port 3306 to the database; the frontend cannot resolve the database on its separate network.

Docker's embedded DNS resolves container names on user-defined networks. The port check tests connectivity only.

For host networking on Linux, Apache shares the host network namespace and listens directly on port 80 without a -p mapping. The runner stops that container after the verification. For the bind mount, the Nginx container serves a local index.html containing Hello students, then serves the edited content without restarting. The mount uses :ro for container access and :z for the Fedora SELinux container label.

An overlay network connects containers across Docker hosts through an encapsulated network. In Docker Swarm, managers coordinate service/network membership and VXLAN carries cross-host data. An attachable overlay can also accept standalone containers. This requires Swarm setup, reachable host addresses and the appropriate control/data ports. The overlay part is research; the practical tests use local bridge networks.

```bash
docker network create homework-front
docker network create homework-back
docker network create homework-isolated
docker network connect homework-front homework-backend
```

Reference: [Docker overlay networks](https://docs.docker.com/engine/network/drivers/overlay/).

## Commands and output

### Commands and results

```bash
zephoryx@fedora$ docker network create homework-front
9b6ba834bade80da39712c6f4438545b8c022c070d7a098ca4ad3176b11be8f1

zephoryx@fedora$ docker network create homework-back
f992a0c6c49abf051e14e16644098bd4791ca18544f7059de83b61318669d90a

zephoryx@fedora$ docker network create homework-isolated
be2e243a63eccbf5c97ff2f0306021110b09f8f328351bb22b60a6168a4c6e7f

zephoryx@fedora$ docker run -d --name homework-front --network homework-front nginx:1.29-alpine
Unable to find image 'nginx:1.29-alpine' locally
1.29-alpine: Pulling from library/nginx
Digest: sha256:5616878291a2eed594aee8db4dade5878cf7edcb475e59193904b198d9b830de
Status: Downloaded newer image for nginx:1.29-alpine
a9539db202dcdbfcce064b57b781358450520812dfc39820b7aa2c32e8a652a2

zephoryx@fedora$ docker run -d --name homework-db --network homework-back -e MYSQL_ROOT_PASSWORD=classroom-example-only mysql:8.0
b9cf1fb3763522c390255c925059f75c3afc19e72476b262f93bf4e885739876

zephoryx@fedora$ docker run -d --name homework-backend --network homework-back alpine:latest sleep 3600
a383e8c163baeeffbb826f53fd9df2632b3bb1f9f709845068cecdbb9d3be69d

zephoryx@fedora$ docker network connect homework-front homework-backend

zephoryx@fedora$ docker inspect homework-backend --format '{{json .NetworkSettings.Networks}}'
{"homework-back":{"IPAMConfig":null,"Links":null,"Aliases":null,"DriverOpts":null,"GwPriority":0,"NetworkID":"f992a0c6c49abf051e14e16644098bd4791ca18544f7059de83b61318669d90a","EndpointID":"7cf58bc4cfba307d867d57de495917114dcfbe48009a7b45af2f4949481969e6","Gateway":"172.20.0.1","IPAddress":"172.20.0.3","MacAddress":"6e:0a:75:1e:f6:63","IPPrefixLen":16,"IPv6Gateway":"","GlobalIPv6Address":"","GlobalIPv6PrefixLen":0,"DNSNames":["homework-backend","a383e8c163ba"]},"homework-front":{"IPAMConfig":{},"Links":null,"Aliases":[],"DriverOpts":{},"GwPriority":0,"NetworkID":"9b6ba834bade80da39712c6f4438545b8c022c070d7a098ca4ad3176b11be8f1","EndpointID":"1288f75594e89105907acac14d464eb6947db47a3822b8cbe1bcacf1b1b2ed94","Gateway":"172.19.0.1","IPAddress":"172.19.0.3","MacAddress":"be:a9:cf:89:1a:d2","IPPrefixLen":16,"IPv6Gateway":"","GlobalIPv6Address":"","GlobalIPv6PrefixLen":0,"DNSNames":["homework-backend","a383e8c163ba"]}}

zephoryx@fedora$ docker exec homework-backend wget -qO- http://homework-front
<h1>Welcome to nginx!</h1>

zephoryx@fedora$ docker exec homework-backend nc -z -w 5 homework-db 3306
# Exit status: 1

zephoryx@fedora$ docker exec homework-front nslookup homework-db
Server:		127.0.0.11
Address:	127.0.0.11:53

** server can't find homework-db: NXDOMAIN

** server can't find homework-db: NXDOMAIN
# Exit status: 1

zephoryx@fedora$ docker run -d --name homework-bind -p 127.0.0.1:18081:80 -v "$PWD/07-docker-network-volumes/bind-mount-site:/usr/share/nginx/html:ro,z" nginx:1.29-alpine
4fee1bf54557c0e27a195817aeb5a7b4c0fd2cad2f652702364dc7ab8aefa6e0

zephoryx@fedora$ curl -f http://127.0.0.1:18081
curl: (56) Recv failure: Connection reset by peer
Warning: Problem (retrying all errors). Will retry in 1 second. 10 retries
Warning: left.

Hello students

zephoryx@fedora$ curl -f http://127.0.0.1:18081
Hello students - updated without restarting the container

zephoryx@fedora$ docker inspect homework-bind --format 'started={{.State.StartedAt}}'
started=2026-10-07T13:10:20.892639219Z

zephoryx@fedora$ docker run -d --name homework-host-apache --network host httpd:2.4
Unable to find image 'httpd:2.4' locally
2.4: Pulling from library/httpd
Digest: sha256:c842ac797bd1fe8b3cd26d002ac9d948aa2814097544600600b35aef42e6785a
Status: Downloaded newer image for httpd:2.4
12036a564f0f49fbf6b48e2b193c12162e4d57370fadb99de786118246fde7b4

zephoryx@fedora$ curl -f http://127.0.0.1:80
curl: (7) Failed to connect to 127.0.0.1 port 80 after 0 ms: Could not connect to server
Warning: Problem : connection refused. Will retry in 1 second. 10 retries left.

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<title>It works! Apache httpd</title>
</head>
<body>
<p>It works!</p>
</body>
</html>

zephoryx@fedora$ docker inspect homework-host-apache --format '{{.HostConfig.NetworkMode}}'
host

zephoryx@fedora$ docker stop homework-host-apache
homework-host-apache

zephoryx@fedora$ docker exec homework-backend nc -z -w 5 homework-db 3306
```
