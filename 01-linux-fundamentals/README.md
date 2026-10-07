# Sessions 1 & 2: Linux Fundamentals

**Nitish Kumar Bhambu — 24BCS10589**

I used an Ubuntu container for user-management commands so the exercise would not create test accounts on my Fedora laptop. `adduser` is the convenient interactive wrapper commonly used on Ubuntu/Debian; `useradd` is the lower-level tool and often needs explicit options for a home directory and shell. That preference is distribution-specific, not a universal Linux rule. The transcript creates homeworkstudent with adduser and verifies its UID and home directory.

A hard link is another directory entry for the same inode; removing the original name does not remove data while a hard link remains. It normally cannot cross filesystems or link directories. A symbolic link stores a target path; it can cross filesystems and can point at a directory, but becomes dangling if its target disappears. The exercise compares inodes, removes the original and tests both links.

`journalctl` reads the systemd journal. `journalctl -u docker.service` filters by service, `-n` limits recent entries and `--list-boots` shows available boots. Access depends on journal permissions. These commands use this host's real journal; an Ubuntu container without systemd is not a substitute for actual service logs.

The command practice covers navigation, files/directories, copying/moving, reading, searching, permissions, awk/sed, sorting, environment variables, process/disk inspection, pipes/redirection and tar archives. I avoid changing the host's users or networking for a homework demonstration.

```bash
python3 scripts/run_basics.py 1
```

## Execution evidence

<!-- EVIDENCE -->

### current-run.txt

[Complete transcript](outputs/current-run.txt)

````text
Captured 2026-10-07T13:00:06.523153+00:00
$ docker run --rm ubuntu:24.04 bash -c 'apt-get update -qq && apt-get install -y -qq adduser passwd procps && set -eu
mkdir -p /tmp/homework-links
cd /tmp/homework-links
printf '"'"'original data\n'"'"' > original
ln original hard
ln -s original soft
ls -li original hard soft
rm original
cat hard
cat soft || true
rm hard soft
adduser --disabled-password --gecos '"'"''"'"' homeworkstudent
id homeworkstudent
ls -ld /home/homeworkstudent
useradd -M lowlevelstudent
getent passwd homeworkstudent lowlevelstudent
pwd
mkdir practice
cd practice
touch notes.txt
printf '"'"'Linux practice\nsecond line\n'"'"' > notes.txt
cp notes.txt copy.txt
mv copy.txt moved.txt
cat notes.txt
head -n 1 notes.txt
tail -n 1 notes.txt
wc -l notes.txt
grep Linux notes.txt
find . -type f
chmod 640 notes.txt
ls -l
printf '"'"'b\na\nb\n'"'"' | sort | uniq -c
awk '"'"'NR==1 {print $1}'"'"' notes.txt
sed -n '"'"'1p'"'"' notes.txt
df -h /
ps -ef | head -8
tar -czf notes.tar.gz notes.txt
tar -tzf notes.tar.gz
printenv PATH
rm moved.txt notes.txt notes.tar.gz
cd ..
rmdir practice
'
Unable to find image 'ubuntu:24.04' locally
24.04: Pulling from library/ubuntu
a60ef8ec184e: Pulling fs layer
2ea90c0e4faa: Download complete
a60ef8ec184e: Download complete
a60ef8ec184e: Pull complete
Digest: sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55
Status: Downloaded newer image for ubuntu:24.04
debconf: delaying package configuration, since apt-utils is not installed
Selecting previously unselected package adduser.
(Reading database ... 
(Reading database ... 5%
(Reading database ... 10%
(Reading database ... 15%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... 100%
(Reading database ... 4381 files and directories currently installed.)
Preparing to unpack .../adduser_3.137ubuntu1_all.deb ...
Unpacking adduser (3.137ubuntu1) ...
Setting up adduser (3.137ubuntu1) ...
6830343 -rw-r--r--. 2 root root 14 Oct  7 13:00 hard
6830343 -rw-r--r--. 2 root root 14 Oct  7 13:00 original
6830344 lrwxrwxrwx. 1 root root  8 Oct  7 13:00 soft -> original
original data
cat: soft: No such file or directory
info: Adding user `homeworkstudent' ...
info: Selecting UID/GID from range 1000 to 59999 ...
info: Adding new group `homeworkstudent' (1001) ...
info: Adding new user `homeworkstudent' (1001) with group `homeworkstudent (1001)' ...
info: Creating home directory `/home/homeworkstudent' ...
info: Copying files from `/etc/skel' ...
info: Adding new user `homeworkstudent' to supplemental / extra groups `users' ...
info: Adding user `homeworkstudent' to group `users' ...
uid=1001(homeworkstudent) gid=1001(homeworkstudent) groups=1001(homeworkstudent),100(users)
drwxr-x---. 1 homeworkstudent homeworkstudent 54 Oct  7 13:00 /home/homeworkstudent
homeworkstudent:x:1001:1001:,,,:/home/homeworkstudent:/bin/bash
lowlevelstudent:x:1002:1002::/home/lowlevelstudent:/bin/sh
/tmp/homework-links
Linux practice
second line
Linux practice
second line
2 notes.txt
Linux practice
./notes.txt
./moved.txt
total 8
-rw-r--r--. 1 root root 27 Oct  7 13:00 moved.txt
-rw-r-----. 1 root root 27 Oct  7 13:00 notes.txt
      1 a
      2 b
Linux
Linux practice
Filesystem      Size  Used Avail Use% Mounted on
overlay         365G  125G  238G  35% /
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 13:00 ?        00:00:00 bash -c apt-get update -qq && apt-get install -y -qq adduser passwd procps && set -eu mkdir -p /tmp/homework-links cd /tmp/homework-links printf 'original data\n' > original ln original hard ln -s original soft ls -li original hard soft rm original cat hard cat soft || true rm hard soft adduser --disabled-password --gecos '' homeworkstudent id homeworkstudent ls -ld /home/homeworkstudent useradd -M lowlevelstudent getent passwd homeworkstudent lowlevelstudent pwd mkdir practice cd practice touch notes.txt printf 'Linux practice\nsecond line\n' > notes.txt cp notes.txt copy.txt mv copy.txt moved.txt cat notes.txt head -n 1 notes.txt tail -n 1 notes.txt wc -l notes.txt grep Linux notes.txt find . -type f chmod 640 notes.txt ls -l printf 'b\na\nb\n' | sort | uniq -c awk 'NR==1 {print $1}' notes.txt sed -n '1p' notes.txt df -h / ps -ef | head -8 tar -czf notes.tar.gz notes.txt tar -tzf notes.tar.gz printenv PATH rm moved.txt notes.txt notes.tar.gz cd .. rmdir practice 
root         234       1  0 13:00 ?        00:00:00 ps -ef
root         235       1  0 13:00 ?        00:00:00 head -8
notes.txt
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
[exit 0]
$ journalctl --user -n 8 --no-pager
Oct 07 18:30:29 fedora chatgpt[10536]: [10536:10536:1007/183029.747783:ERROR:owl/browser/api/electron_api_web_contents.cc:8361] Electron renderer console [error] app://-/index.html:0 ResizeObserver loop completed with undelivered notifications.
Oct 07 18:30:30 fedora chatgpt[10536]: [electron-message-handler] [desktop-notifications][global-error] ResizeObserver loop completed with undelivered notifications. rendererWebContentsId=1 rendererWindowAppearance=primary rendererWindowFocused=false rendererWindowId=1 rendererWindowVisible=true
Oct 07 18:30:30 fedora chatgpt[10536]: [10536:10536:1007/183030.370827:ERROR:owl/browser/api/electron_api_web_contents.cc:8361] Electron renderer console [error] app://-/index.html:0 ResizeObserver loop completed with undelivered notifications.
Oct 07 18:30:30 fedora chatgpt[10536]: [electron-message-handler] [desktop-notifications][global-error] ResizeObserver loop completed with undelivered notifications. rendererWebContentsId=1 rendererWindowAppearance=primary rendererWindowFocused=false rendererWindowId=1 rendererWindowVisible=true
Oct 07 18:30:30 fedora chatgpt[10536]: [10536:10536:1007/183030.884323:ERROR:owl/browser/api/electron_api_web_contents.cc:8361] Electron renderer console [error] app://-/index.html:0 ResizeObserver loop completed with undelivered notifications.
Oct 07 18:30:31 fedora chatgpt[10536]: [electron-message-handler] [desktop-notifications][global-error] ResizeObserver loop completed with undelivered notifications. rendererWebContentsId=1 rendererWindowAppearance=primary rendererWindowFocused=false rendererWindowId=1 rendererWindowVisible=true
Oct 07 18:30:31 fedora chatgpt[10536]: [10536:10536:1007/183031.949592:ERROR:owl/browser/api/electron_api_web_contents.cc:8361] Electron renderer console [error] app://-/index.html:0 ResizeObserver loop completed with undelivered notifications.
Oct 07 18:30:51 fedora baloo_file_extractor[76790]: Failed to register with host portal QDBusError("org.freedesktop.portal.Error.Failed", "Could not register app ID: App info not found for 'org.kde.baloo'")
[exit 0]
$ journalctl -u docker.service -n 12 --no-pager
Oct 07 18:30:10 fedora dockerd[1401]: time="2026-10-07T18:30:10.379702812+05:30" level=info msg="detected 127.0.0.53 nameserver, assuming systemd-resolved, so using resolv.conf: /run/systemd/resolve/resolv.conf"
Oct 07 18:30:10 fedora dockerd[1401]: time="2026-10-07T18:30:10.771282617+05:30" level=info msg="sbJoin: gwep4 ''->'c30de969a938', gwep6 ''->''"
Oct 07 18:30:13 fedora dockerd[1401]: time="2026-10-07T18:30:13.271590705+05:30" level=warning msg="healthcheck failed" actualDuration="878.065µs" error="Unavailable: connection error: desc = \"transport: Error while dialing: only one connection allowed\"" timeout=15s
Oct 07 18:30:14 fedora dockerd[1401]: time="2026-10-07T18:30:14.852218879+05:30" level=info msg="detected 127.0.0.53 nameserver, assuming systemd-resolved, so using resolv.conf: /run/systemd/resolve/resolv.conf"
Oct 07 18:30:15 fedora dockerd[1401]: time="2026-10-07T18:30:15.278688201+05:30" level=info msg="sbJoin: gwep4 ''->'88251fd03f6a', gwep6 ''->''"
Oct 07 18:30:18 fedora dockerd[1401]: time="2026-10-07T18:30:18.271198589+05:30" level=error msg="healthcheck failed fatally" error="session healthcheck failed fatally: Unavailable: connection error: desc = \"transport: Error while dialing: only one connection allowed\""
Oct 07 18:30:26 fedora dockerd[1401]: time="2026-10-07T18:30:26.009441464+05:30" level=info msg="sbJoin: gwep4 ''->'dacdb3b556b6', gwep6 ''->''" eid=dacdb3b556b6 ep=homework-hello-nodejs net=bridge nid=d6199b27e911
Oct 07 18:30:27 fedora dockerd[1401]: time="2026-10-07T18:30:27.505783025+05:30" level=info msg="image pulled" digest="sha256:534baea6a22c03a63003dbc8dbe78fe34bc0d7e595d9a9dc9834884ff530eb55" remote="docker.io/library/ubuntu:24.04"
Oct 07 18:30:28 fedora dockerd[1401]: time="2026-10-07T18:30:28.323743146+05:30" level=warning msg="healthcheck failed" actualDuration="717.036µs" error="Unavailable: connection error: desc = \"transport: Error while dialing: only one connection allowed\"" timeout=15s
Oct 07 18:30:28 fedora dockerd[1401]: time="2026-10-07T18:30:28.805864108+05:30" level=info msg="sbJoin: gwep4 ''->'9efd7a65b575', gwep6 ''->''" eid=9efd7a65b575 ep=dazzling_varahamihira net=bridge nid=d6199b27e911
Oct 07 18:30:33 fedora dockerd[1401]: time="2026-10-07T18:30:33.324512273+05:30" level=error msg="healthcheck failed fatally" error="session healthcheck failed fatally: Unavailable: connection error: desc = \"transport: Error while dialing: only one connection allowed\""
Oct 07 18:30:54 fedora dockerd[1401]: time="2026-10-07T18:30:54.072691846+05:30" level=info msg="received task-delete event from containerd" container=c66dcd8517ca8f1b4dce66250e1ff1239c624dc14f2dbbeefeab1df24a77ddaf module=libcontainerd namespace=moby topic=/tasks/delete type="*events.TaskDelete"
[exit 0]
$ journalctl --list-boots --no-pager
IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY
 -5 d55eaacaefd84253a2d24c5f82514b5a Sun 2026-10-04 17:25:12 IST Sun 2026-10-04 17:27:39 IST
 -4 4105fd8123e84602b1512df120be6006 Sun 2026-10-04 22:57:53 IST Mon 2026-10-05 14:16:31 IST
 -3 2b486c8e724e4311bf8c2ca68338797b Mon 2026-10-05 19:46:41 IST Mon 2026-10-05 14:17:01 IST
 -2 644539813dd5436eb052ca421bb55881 Mon 2026-10-05 19:47:13 IST Wed 2026-10-07 15:19:22 IST
 -1 245f231297ed4a77bc4eb1d5ed915cac Wed 2026-10-07 20:49:33 IST Wed 2026-10-07 16:23:39 IST
  0 e02bdae9cfdd4484914d365af722a8ff Wed 2026-10-07 21:53:50 IST Wed 2026-10-07 18:31:00 IST
[exit 0]
LAB EXECUTION FINISHED
````
