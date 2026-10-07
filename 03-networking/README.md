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

The command blocks record the network checks, including connectivity failures. I used a toolbox container for utilities that were not installed on the host.

```bash
ip -brief address
ip route
dig example.com
ping -c 2 1.1.1.1
ss -tuln
curl -I https://example.com
```

## Commands and output

### Commands and results

```bash
zephoryx@fedora$ ip -brief address
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

zephoryx@fedora$ ip route
default via 192.168.1.1 dev wlp0s20f3 proto dhcp src 192.168.6.199 metric 600
10.0.85.2 dev outline-tun0 scope link src 10.0.85.1 linkdown
172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
172.18.0.0/16 dev br-1e07af2e7d59 proto kernel scope link src 172.18.0.1
192.168.0.0/19 dev wlp0s20f3 proto kernel scope link src 192.168.6.199 metric 600
192.168.49.0/24 dev br-bd87a280590b proto kernel scope link src 192.168.49.1

zephoryx@fedora$ ip neigh
172.17.0.2 dev docker0 lladdr ba:97:c5:5d:d9:aa REACHABLE
172.17.0.3 dev docker0 lladdr e2:f7:67:1b:ca:24 REACHABLE
192.168.49.2 dev br-bd87a280590b lladdr 56:9d:45:53:19:0a STALE
192.168.1.1 dev wlp0s20f3 lladdr 90:e3:ba:02:21:c6 REACHABLE

zephoryx@fedora$ dig example.com
; <<>> DiG 9.18.50 <<>> example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 61654
# ... output shortened ...
;; Query time: 57 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Wed Oct 07 18:31:02 IST 2026
;; MSG SIZE  rcvd: 72

zephoryx@fedora$ getent hosts example.com
2606:4700:10::ac42:93f3 example.com
2606:4700:10::6814:179a example.com

zephoryx@fedora$ ping -c 2 1.1.1.1
PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
64 bytes from 1.1.1.1: icmp_seq=1 ttl=57 time=44.2 ms
64 bytes from 1.1.1.1: icmp_seq=2 ttl=57 time=60.9 ms

--- 1.1.1.1 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 44.222/52.562/60.902/8.340 ms

zephoryx@fedora$ ss -tuln
Netid State  Recv-Q Send-Q      Local Address:Port  Peer Address:Port
udp   UNCONN 0      0            192.168.49.1:50572      0.0.0.0:*
udp   UNCONN 0      0                 0.0.0.0:35298      0.0.0.0:*
udp   UNCONN 0      0                 0.0.0.0:60765      0.0.0.0:*
udp   UNCONN 0      0              172.17.0.1:60796      0.0.0.0:*
udp   UNCONN 0      0                 0.0.0.0:44448      0.0.0.0:*
# ... intermediate output omitted ...
tcp   LISTEN 0      4096            127.0.0.1:20241      0.0.0.0:*
tcp   LISTEN 0      4096            127.0.0.1:13000      0.0.0.0:*
tcp   LISTEN 0      4096                 [::]:5355          [::]:*
tcp   LISTEN 0      50     [::ffff:127.0.0.1]:52829            *:*
tcp   LISTEN 0      50                      *:1716             *:*
tcp   LISTEN 0      4096   [::ffff:127.0.0.1]:46421            *:*
tcp   LISTEN 0      4096                [::1]:631           [::]:*

zephoryx@fedora$ curl --head --max-time 15 https://example.com
HTTP/2 200
date: Wed, 07 Oct 2026 13:01:03 GMT
content-type: text/html; charset=utf-8
server: cloudflare
last-modified: Fri, 02 Oct 2026 16:11:02 GMT
allow: GET, HEAD
accept-ranges: bytes
age: 2927
cf-cache-status: HIT
cf-ray: a46d17a02f4ca901-MAA
alt-svc: h3=":443"; ma=86400

zephoryx@fedora$ ip -s link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    RX:  bytes packets errors dropped  missed   mcast
    TX:  bytes packets errors dropped carrier collsns
2: enp62s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc fq_codel state DOWN mode DEFAULT group default qlen 1000
    link/ether 74:d4:dd:5e:1b:8c brd ff:ff:ff:ff:ff:ff
# ... intermediate output omitted ...
    link/ether 7a:c5:a3:13:bc:65 brd ff:ff:ff:ff:ff:ff link-netnsid 4
    RX:  bytes packets errors dropped  missed   mcast
    TX:  bytes packets errors dropped carrier collsns
28: vethfc04432@if2: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master docker0 state UP mode DEFAULT group default
    link/ether 42:bb:cf:fd:e8:3b brd ff:ff:ff:ff:ff:ff link-netnsid 2
    RX:  bytes packets errors dropped  missed   mcast
    TX:  bytes packets errors dropped carrier collsns
```

### Additional network tools

These commands ran in the network toolbox container using host networking. The `+` prefixes are shell tracing.

```bash
+ traceroute -m 4 -w 1 1.1.1.1
traceroute to 1.1.1.1 (1.1.1.1), 4 hops max, 60 byte packets
 1  dns.nfen (192.168.1.1)  4.605 ms  4.540 ms  4.526 ms
 2  static-193.79.194.14-tataidc.co.in (14.194.79.193)  4.559 ms  4.551 ms  4.544 ms
 3  * 115.111.223.9 (115.111.223.9)  4.521 ms  4.514 ms
 4  172.31.167.58 (172.31.167.58)  10.616 ms  10.610 ms  11.007 ms
+ nc -z -w 3 127.0.0.1 13000
Connection to 127.0.0.1 13000 port [tcp/*] succeeded!
+ curl -I --max-time 15 https://example.com

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
```
