# Session 4: Networking

**Nitish Kumar Bhambu — 24BCS10589**

I checked the machine's interfaces, routes, neighbours, DNS, reachability, listening sockets, HTTPS response headers and link counters. These commands inspect the current network; they do not reconfigure it.

| Command | What I look for |
|---|---|
| ip -brief address | Interfaces, addresses and link state |
| ip route | Default gateway and subnet routes |
| ip neigh | Cached IP-to-link-layer neighbour mappings |
| dig / getent hosts | DNS answers and the system resolver's result |
| ping | ICMP reachability and round-trip time; blocked ICMP does not prove HTTP is down |
| ss -tuln | Listening TCP/UDP sockets; -n keeps numeric addresses/ports |
| curl --head | HTTP status, TLS/HTTP access and response headers |
| ip -s link | Traffic and error/drop counters |
| traceroute | Intermediate hops where routers respond; missing replies can be filtering |
| nc | Test a specific TCP port |
| tcpdump | Inspect packets on a selected interface; permissions and careful filtering matter |
| nmap | Inspect services on systems I own, such as a localhost lab |

The transcript is the record of what ran and includes any connectivity failures. Commands that require additional utilities or capture privileges are explained here without invented outputs. The supplementary toolbox exercise records those utilities against local lab services.

```bash
python3 scripts/run_basics.py 4
```

## Execution evidence

<!-- EVIDENCE -->

### current-run.txt

[Complete transcript](outputs/current-run.txt)

````text
Captured 2026-10-07T13:01:01.850923+00:00
$ ip -brief address
lo               UNKNOWN        127.0.0.1/8 ::1/128
enp62s0          DOWN
wlp0s20f3        UP             192.168.6.199/19 fe80::a215:ee0:afc3:7587/64
outline-tun0     DOWN           10.0.85.1/32
docker0          UP             172.17.0.1/16 fe80::b000:1ff:fe09:4a93/64
br-bd87a280590b  UP             192.168.49.1/24 fe80::10ad:19ff:fe46:7b42/64
veth8a1badc@if2  UP             fe80::28aa:cff:fe61:a822/64
br-1e07af2e7d59  UP             172.18.0.1/16 fe80::e490:2fff:fe38:45e7/64
veth4c492bf@if2  UP             fe80::ecbb:20ff:fec1:35f8/64
veth24caf47@if2  UP             fe80::80b1:b5ff:fe07:b65b/64
vethd1a3cc4@if2  UP             fe80::78c5:a3ff:fe13:bc65/64
vethfc04432@if2  UP             fe80::1cd9:78ff:fe1f:6505/64
[exit 0]
$ ip route
default via 192.168.1.1 dev wlp0s20f3 proto dhcp src 192.168.6.199 metric 600
10.0.85.2 dev outline-tun0 scope link src 10.0.85.1 linkdown
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
172.18.0.0/16 dev br-1e07af2e7d59 proto kernel scope link src 172.18.0.1
192.168.0.0/19 dev wlp0s20f3 proto kernel scope link src 192.168.6.199 metric 600
192.168.49.0/24 dev br-bd87a280590b proto kernel scope link src 192.168.49.1
[exit 0]
$ ip neigh
172.17.0.2 dev docker0 lladdr ba:97:c5:5d:d9:aa REACHABLE
172.17.0.3 dev docker0 lladdr e2:f7:67:1b:ca:24 REACHABLE
192.168.49.2 dev br-bd87a280590b lladdr 56:9d:45:53:19:0a STALE
192.168.1.1 dev wlp0s20f3 lladdr 90:e3:ba:02:21:c6 REACHABLE
[exit 0]
$ dig example.com

; <<>> DiG 9.18.50 <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 61654
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;example.com.			IN	A

;; ANSWER SECTION:
example.com.		58	IN	A	104.20.23.154
example.com.		58	IN	A	172.66.147.243

;; Query time: 57 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Wed Oct 07 18:31:02 IST 2026
;; MSG SIZE  rcvd: 72
[exit 0]
$ getent hosts example.com
2606:4700:10::ac42:93f3 example.com
2606:4700:10::6814:179a example.com
[exit 0]
$ ping -c 2 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=57 time=44.2 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=57 time=60.9 ms

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 44.222/52.562/60.902/8.340 ms
[exit 0]
$ ss -tuln

[Excerpt: 62 intermediate lines omitted; complete transcript linked above.]

cf-ray: a46d17a02f4ca901-MAA
alt-svc: h3=":443"; ma=86400
[exit 0]
$ ip -s link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    RX:  bytes packets errors dropped  missed   mcast
       2040551   11568      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
       2040551   11568      0       0       0       0
2: enp62s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN mode DEFAULT group default qlen 1000
    link/ether 74:d4:dd:5e:1b:8c brd ff:ff:ff:ff:ff:ff
    RX:  bytes packets errors dropped  missed   mcast
             0       0      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
             0       0      0       0       0       0
    altname enx74d4dd5e1b8c
3: wlp0s20f3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DORMANT group default qlen 1000
    link/ether e4:c7:67:8a:26:ef brd ff:ff:ff:ff:ff:ff
    RX:  bytes packets errors dropped  missed   mcast
    1687451296 1726935      0    1142       0       0
    TX:  bytes packets errors dropped carrier collsns
      81828716  323265      0      24       0       0
    altname wlxe4c7678a26ef
4: outline-tun0: <NO-CARRIER,POINTOPOINT,MULTICAST,NOARP,UP> mtu 1500 qdisc fq_codel state DOWN mode DEFAULT group default qlen 500
    link/none
    RX:  bytes packets errors dropped  missed   mcast
             0       0      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
             0       0      0      65       0       0
5: docker0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether b2:00:01:09:4a:93 brd ff:ff:ff:ff:ff:ff
    RX:  bytes packets errors dropped  missed   mcast
       1080569   15940      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
      87141223   33715      0      79       0       0
6: br-bd87a280590b: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether 12:ad:19:46:7b:42 brd ff:ff:ff:ff:ff:ff
    RX:  bytes packets errors dropped  missed   mcast
       7907242   18857      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
     115825783   47582      0      63       0       0
7: veth8a1badc@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-bd87a280590b state UP mode DEFAULT group default
    link/ether 2a:aa:0c:61:a8:22 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    RX:  bytes packets errors dropped  missed   mcast
       8171240   18857      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
     115832007   47618      0       0       0       0
18: br-1e07af2e7d59: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP mode DEFAULT group default
    link/ether e6:90:2f:38:45:e7 brd ff:ff:ff:ff:ff:ff
    RX:  bytes packets errors dropped  missed   mcast
           392      14      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
          8402      43      0      10       0       0
19: veth4c492bf@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-1e07af2e7d59 state UP mode DEFAULT group default
    link/ether ee:bb:20:c1:35:f8 brd ff:ff:ff:ff:ff:ff link-netnsid 1
    RX:  bytes packets errors dropped  missed   mcast
         19765     195      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
         38463     354      0       0       0       0
22: veth24caf47@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-1e07af2e7d59 state UP mode DEFAULT group default
    link/ether 82:b1:b5:07:b6:5b brd ff:ff:ff:ff:ff:ff link-netnsid 3
    RX:  bytes packets errors dropped  missed   mcast
         19995     247      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
         23464     209      0       0       0       0
23: vethd1a3cc4@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master br-1e07af2e7d59 state UP mode DEFAULT group default
    link/ether 7a:c5:a3:13:bc:65 brd ff:ff:ff:ff:ff:ff link-netnsid 4
    RX:  bytes packets errors dropped  missed   mcast
           126       3      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
          6734      37      0       0       0       0
28: vethfc04432@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether 42:bb:cf:fd:e8:3b brd ff:ff:ff:ff:ff:ff link-netnsid 2
    RX:  bytes packets errors dropped  missed   mcast
           264       6      0       0       0       0
    TX:  bytes packets errors dropped carrier collsns
          5972      38      0       0       0       0
[exit 0]
LAB EXECUTION FINISHED
````

### toolbox-build.txt

[Complete transcript](outputs/toolbox-build.txt)

````text
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 234B done
#1 DONE 0.0s

#2 [internal] load metadata for docker.io/library/alpine:3.23
#2 DONE 0.8s

#3 [internal] load .dockerignore
#3 transferring context: 2B done
#3 DONE 0.0s

#4 [1/2] FROM docker.io/library/alpine:3.23@sha256:85fe1e81d6758c208f3e1eed4338a1997e19d4be002d4dd32d3100c9a8c010a0
#4 resolve docker.io/library/alpine:3.23@sha256:85fe1e81d6758c208f3e1eed4338a1997e19d4be002d4dd32d3100c9a8c010a0 0.0s done
#4 CACHED

#5 [2/2] RUN apk add --no-cache iproute2 bind-tools traceroute tcpdump nmap curl wget net-tools netcat-openbsd whois
#5 1.956 ( 1/47) Installing fstrm (0.6.1-r4)
#5 2.008 ( 2/47) Installing krb5-conf (1.0-r2)
#5 2.056 ( 3/47) Installing libcom_err (1.47.3-r0)
#5 2.106 ( 4/47) Installing keyutils-libs (1.6.3-r4)
#5 2.158 ( 5/47) Installing libverto (0.3.2-r2)
#5 2.216 ( 6/47) Installing krb5-libs (1.22.1-r0)
#5 2.555 ( 7/47) Installing json-c (0.18-r1)
#5 2.623 ( 8/47) Installing nghttp2-libs (1.69.0-r0)
#5 2.692 ( 9/47) Installing protobuf-c (1.5.2-r2)
#5 2.752 (10/47) Installing userspace-rcu (0.15.3-r0)
#5 2.828 (11/47) Installing libuv (1.52.1-r0)
#5 2.914 (12/47) Installing xz-libs (5.8.4-r0)
#5 3.005 (13/47) Installing libxml2 (2.13.9-r1)
#5 3.247 (14/47) Installing bind-libs (9.20.29-r0)
#5 3.874 (15/47) Installing bind-tools (9.20.29-r0)
#5 4.265 (16/47) Installing brotli-libs (1.2.0-r0)
#5 4.876 (17/47) Installing c-ares (1.34.8-r0)
#5 4.995 (18/47) Installing libunistring (1.4.1-r0)
#5 5.676 (19/47) Installing libidn2 (2.3.8-r0)
#5 5.854 (20/47) Installing libpsl (0.21.5-r3)
#5 5.973 (21/47) Installing zstd-libs (1.5.7-r2)
#5 6.366 (22/47) Installing libcurl (8.22.0-r0)
#5 6.813 (23/47) Installing curl (8.22.0-r0)
#5 7.082 (24/47) Installing libcap2 (2.78-r0)
#5 7.202 (25/47) Installing libelf (0.194-r0)
#5 7.324 (26/47) Installing libmnl (1.0.5-r2)
#5 7.412 (27/47) Installing iproute2-minimal (6.17.0-r0)
#5 7.746 (28/47) Installing libxtables (1.8.11-r1)
#5 7.834 (29/47) Installing iproute2-tc (6.17.0-r0)
#5 8.079 (30/47) Installing iproute2-ss (6.17.0-r0)
#5 8.192 (31/47) Installing iproute2 (6.17.0-r0)
#5 8.373   Executing iproute2-6.17.0-r0.post-install
#5 8.377 (32/47) Installing mii-tool (2.10-r3)
#5 8.444 (33/47) Installing net-tools (2.10-r3)
#5 8.587 (34/47) Installing libmd (1.1.0-r0)
#5 8.675 (35/47) Installing libbsd (0.12.2-r0)
#5 8.792 (36/47) Installing netcat-openbsd (1.234.1-r0)
#5 8.916 (37/47) Installing libgcc (15.2.0-r2)
#5 9.094 (38/47) Installing lua5.4-libs (5.4.8-r0)
#5 9.275 (39/47) Installing libpcap (1.10.7-r0)
#5 9.513 (40/47) Installing libssh2 (1.11.1-r3)
#5 9.753 (41/47) Installing libstdc++ (15.2.0-r2)
#5 11.04 (42/47) Installing nmap (7.97-r0)
#5 13.93 (43/47) Installing tcpdump (4.99.5-r1)
#5 14.28 (44/47) Installing traceroute (2.1.6-r0)
#5 14.40 (45/47) Installing pcre2 (10.49-r0)
#5 14.82 (46/47) Installing wget (1.25.0-r2)
#5 15.15 (47/47) Installing whois (5.6.5-r0)
#5 15.24 Executing busybox-1.37.0-r30.trigger
#5 15.25 OK: 40.7 MiB in 63 packages
#5 DONE 15.4s

#6 exporting to image
#6 exporting layers
#6 exporting layers 1.0s done
#6 exporting manifest sha256:34d48af494efce9f7460fc0b98465f1c12fc5fd44fe6a1b452fa9545fe806967 done
#6 exporting config sha256:f0af04b4c370045082af5e49d4c3a6e86ec595d500f48aa771e9eb855cc6c2df done
#6 exporting attestation manifest sha256:08d30767b15a9d8b4f2ab073a69b110dcad4f6916a656d55fc128f706ac02bfd 0.0s done
#6 exporting manifest list sha256:d39c3838938f5e14c9e02520d91cb9ef83bb1ab465948d14d0a50720d20f71ac done
#6 naming to docker.io/library/homework-network-toolbox:latest done
#6 unpacking to docker.io/library/homework-network-toolbox:latest
#6 unpacking to docker.io/library/homework-network-toolbox:latest 0.3s done
#6 DONE 1.3s
````

### toolbox-run.txt

[Complete transcript](outputs/toolbox-run.txt)

````text
+ set -u
+ ip -brief address
lo               UNKNOWN        127.0.0.1/8 ::1/128
enp62s0          DOWN
wlp0s20f3        UP             192.168.6.199/19 fe80::a215:ee0:afc3:7587/64
outline-tun0     DOWN           10.0.85.1/32
docker0          UP             172.17.0.1/16 fe80::b000:1ff:fe09:4a93/64
br-bd87a280590b  UP             192.168.49.1/24 fe80::10ad:19ff:fe46:7b42/64
veth8a1badc@if2  UP             fe80::28aa:cff:fe61:a822/64
br-1e07af2e7d59  UP             172.18.0.1/16 fe80::e490:2fff:fe38:45e7/64
veth4c492bf@if2  UP             fe80::ecbb:20ff:fec1:35f8/64
vethd1a3cc4@if2  UP             fe80::78c5:a3ff:fe13:bc65/64
veth753170f@if2  UP             fe80::10e6:9dff:fe74:e6b1/64
vethbe315d7@if2  UP             fe80::58d0:25ff:fe1a:837d/64
veth096df60@if2  UP             fe80::8013:96ff:fe1b:7c23/64
vethb89e5bf@if2  UP             fe80::584d:a2ff:fe3b:7602/64
veth33aaa2f@if2  UP             fe80::449c:fff:feef:4191/64
vethf83e503@if2  UP             fe80::ac71:faff:feaa:b5e5/64
vethf40cd42@if2  UP             fe80::7c06:73ff:fe19:b8e0/64
br-9b6ba834bade  UP             172.19.0.1/16 fe80::60e6:f7ff:fec3:b1fd/64
br-f992a0c6c49a  UP             172.20.0.1/16 fe80::48db:16ff:fe51:3cfd/64
br-be2e243a63ec  DOWN           172.21.0.1/16
veth274ac39@if2  UP             fe80::7c8a:80ff:fe2c:9a3e/64
veth8c7db06@if2  UP             fe80::885d:16ff:fe5c:8a0e/64
veth28d2b1d@if2  UP             fe80::2e:dcff:fe27:c285/64
veth96ec519@if3  UP             fe80::c44a:7eff:fec1:52eb/64
vethcfb71c1@if2  UP             fe80::4051:b1ff:fea4:101a/64
vethe8d74df@if2  UP             fe80::5c38:9ff:feb8:91c7/64
veth42d8852@if93 UP             fe80::d43a:d7ff:fe01:7b9a/64
+ ip route
default via 192.168.1.1 dev wlp0s20f3 proto dhcp src 192.168.6.199 metric 600
10.0.85.2 dev outline-tun0 scope link src 10.0.85.1 linkdown
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
172.18.0.0/16 dev br-1e07af2e7d59 proto kernel scope link src 172.18.0.1
172.19.0.0/16 dev br-9b6ba834bade proto kernel scope link src 172.19.0.1
172.20.0.0/16 dev br-f992a0c6c49a proto kernel scope link src 172.20.0.1
172.21.0.0/16 dev br-be2e243a63ec proto kernel scope link src 172.21.0.1 linkdown
192.168.0.0/19 dev wlp0s20f3 proto kernel scope link src 192.168.6.199 metric 600
192.168.49.0/24 dev br-bd87a280590b proto kernel scope link src 192.168.49.1
+ nslookup example.com
Server:		127.0.0.53
Address:	127.0.0.53#53

Non-authoritative answer:
Name:	example.com
Address: 104.20.23.154
Name:	example.com
Address: 172.66.147.243
Name:	example.com
Address: 2606:4700:10::ac42:93f3
Name:	example.com
Address: 2606:4700:10::6814:179a

+ netstat -tuln
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 127.0.0.1:32772         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:32768         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:32769         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:32770         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:32771         0.0.0.0:*               LISTEN
tcp        0      0 0.0.0.0:5355            0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:631           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:18000         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:18081         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:18082         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:3004          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:3005          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:3006          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:3001          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:3002          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:3003          0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.54:53           0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:19090         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:20241         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:13000         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:13001         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:13002         0.0.0.0:*               LISTEN
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN
tcp6       0      0 :::5355                 :::*                    LISTEN
tcp6       0      0 ::1:13002               :::*                    LISTEN
tcp6       0      0 ::1:13001               :::*                    LISTEN
tcp6       0      0 127.0.0.1:52829         :::*                    LISTEN
tcp6       0      0 ::1:18082               :::*                    LISTEN
tcp6       0      0 :::1716                 :::*                    LISTEN
tcp6       0      0 127.0.0.1:46421         :::*                    LISTEN
tcp6       0      0 ::1:631                 :::*                    LISTEN
tcp6       0      0 ::1:19090               :::*                    LISTEN
udp        0      0 192.168.49.1:50572      0.0.0.0:*
udp        0      0 0.0.0.0:35298           0.0.0.0:*
udp        0      0 172.17.0.1:60796        0.0.0.0:*
udp        0      0 172.17.0.1:45708        0.0.0.0:*
udp        0      0 224.0.0.251:5353        0.0.0.0:*
udp        0      0 224.0.0.251:5353        0.0.0.0:*
udp        0      0 0.0.0.0:5353            0.0.0.0:*
udp        0      0 0.0.0.0:5353            0.0.0.0:*
udp        0      0 0.0.0.0:5355            0.0.0.0:*
udp        0      0 172.18.0.1:54925        0.0.0.0:*
udp        0      0 172.17.0.1:39275        0.0.0.0:*
udp        0      0 172.19.0.1:47628        0.0.0.0:*
udp        0      0 172.20.0.1:47735        0.0.0.0:*
udp        0      0 192.168.6.199:39656     0.0.0.0:*
udp        0      0 172.17.0.1:56433        0.0.0.0:*
udp        0      0 0.0.0.0:56511           0.0.0.0:*
udp        0      0 127.0.0.54:53           0.0.0.0:*
udp        0      0 127.0.0.53:53           0.0.0.0:*
udp        0      0 127.0.0.1:323           0.0.0.0:*
udp6       0      0 :::41772                :::*
udp6       0      0 :::1716                 :::*
udp6       0      0 :::5353                 :::*
udp6       0      0 :::5355                 :::*
udp6       0      0 ::1:323                 :::*
+ traceroute -m 4 -w 1 1.1.1.1
traceroute to 1.1.1.1 (1.1.1.1), 4 hops max, 60 byte packets
 1  dns.nfen (192.168.1.1)  4.605 ms  4.540 ms  4.526 ms
 2  static-193.79.194.14-tataidc.co.in (14.194.79.193)  4.559 ms  4.551 ms  4.544 ms
 3  * 115.111.223.9 (115.111.223.9)  4.521 ms  4.514 ms
 4  172.31.167.58 (172.31.167.58)  10.616 ms  10.610 ms  11.007 ms
+ nc -z -w 3 127.0.0.1 13000
Connection to 127.0.0.1 13000 port [tcp/*] succeeded!
+ curl -I --max-time 15 https://example.com
  % Total    % Received % Xferd  Average Speed  Time    Time    Time   Current
                                 Dload  Upload  Total   Spent   Left   Speed

  0      0   0      0   0      0      0      0                              0HTTP/2 200

  0      0   0      0   0      0      0      0                              0
  0      0   0      0   0      0      0      0                              0
  0      0   0      0   0      0      0      0                              0
date: Wed, 07 Oct 2026 13:15:50 GMT
content-type: text/html; charset=utf-8
server: cloudflare
last-modified: Fri, 02 Oct 2026 16:11:02 GMT
allow: GET, HEAD
accept-ranges: bytes
age: 3814
cf-cache-status: HIT
cf-ray: a46d2d487acc7821-MAA
alt-svc: h3=":443"; ma=86400

+ wget --spider -T 15 https://example.com
Spider mode enabled. Check if remote file exists.
--2026-10-07 13:15:50--  https://example.com/
Resolving example.com (example.com)... 172.66.147.243, 104.20.23.154, 2606:4700:10::ac42:93f3, ...
Connecting to example.com (example.com)|172.66.147.243|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified [text/html]
Remote file exists and could contain further links,
but recursion is disabled -- not retrieving.

+ nmap -sT -Pn -p 13000,18000 127.0.0.1
Starting Nmap 7.97 ( https://nmap.org ) at 2026-10-07 13:15 +0000
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000026s latency).

PORT      STATE SERVICE
13000/tcp open  unknown
18000/tcp open  biimenu

Nmap done: 1 IP address (1 host up) scanned in 0.02 seconds
+ CAPTURE_PID=18
+ sleep 1
+ timeout 8 tcpdump -i lo -nn -c 3 'tcp port 13000'
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on lo, link-type EN10MB (Ethernet), snapshot length 262144 bytes
+ curl -s http://127.0.0.1:13000/health
{"status":"UP"}+ wait 18
13:15:51.714626 IP 127.0.0.1.50208 > 127.0.0.1.13000: Flags [S], seq 2036061428, win 65495, options [mss 65495,sackOK,TS val 1861999113 ecr 0,nop,wscale 10], length 0
13:15:51.714644 IP 127.0.0.1.13000 > 127.0.0.1.50208: Flags [S.], seq 2313278429, ack 2036061429, win 65483, options [mss 65495,sackOK,TS val 2468076271 ecr 1861999113,nop,wscale 10], length 0
13:15:51.714655 IP 127.0.0.1.50208 > 127.0.0.1.13000: Flags [.], ack 1, win 64, options [nop,nop,TS val 1861999113 ecr 2468076271], length 0
3 packets captured
20 packets received by filter
0 packets dropped by kernel
````
