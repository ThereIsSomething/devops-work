#!/usr/bin/env python3
from pathlib import Path
import subprocess,shlex,datetime,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];log=None
folders={1:'01-linux-fundamentals',3:'02-shell-scripting',4:'03-networking',5:'04-git-github',6:'05-docker-fundamentals',7:'06-dockerfiles-and-images',8:'07-docker-network-volumes'}
def out(s):print(s,flush=True);log.write(s+'\n');log.flush()
def run(args,check=True,timeout=600,input=None):
 out('$ '+shlex.join(map(str,args)));p=subprocess.run(list(map(str,args)),cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout,input=input);out(p.stdout.rstrip());out(f'[exit {p.returncode}]')
 if check and p.returncode:raise RuntimeError('Command failed')
 return p.stdout

def linux():
 script='''set -eu
mkdir -p /tmp/homework-links
cd /tmp/homework-links
printf 'original data\\n' > original
ln original hard
ln -s original soft
ls -li original hard soft
rm original
cat hard
cat soft || true
rm hard soft
adduser --disabled-password --gecos '' homeworkstudent
id homeworkstudent
ls -ld /home/homeworkstudent
useradd -M lowlevelstudent
getent passwd homeworkstudent lowlevelstudent
pwd
mkdir practice
cd practice
touch notes.txt
printf 'Linux practice\\nsecond line\\n' > notes.txt
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
printf 'b\\na\\nb\\n' | sort | uniq -c
awk 'NR==1 {print $1}' notes.txt
sed -n '1p' notes.txt
df -h /
ps -ef | head -8
tar -czf notes.tar.gz notes.txt
tar -tzf notes.tar.gz
printenv PATH
rm moved.txt notes.txt notes.tar.gz
cd ..
rmdir practice
'''
 run(['docker','run','--rm','ubuntu:24.04','bash','-c','apt-get update -qq && apt-get install -y -qq adduser passwd procps && '+script])
 run(['journalctl','--user','-n','8','--no-pager'],check=False)
 run(['journalctl','-u','docker.service','-n','12','--no-pager'],check=False)
 run(['journalctl','--list-boots','--no-pager'],check=False)

def shell():
 report=Path(tempfile.mkdtemp(prefix='nitish-sysinfo-'))
 run(['bash','02-shell-scripting/sysinfo.sh'],input=f'{report}\nprocesses\nNitish Kumar Bhambu\n')

def networking():
 for cmd in [['ip','-brief','address'],['ip','route'],['ip','neigh'],['dig','example.com'],['getent','hosts','example.com'],['ping','-c','2','1.1.1.1'],['ss','-tuln'],['curl','--head','--max-time','15','https://example.com'],['ip','-s','link']]:run(cmd,check=False,timeout=30)
 # No network configuration changes or scans of other people's systems.

def git():
 for name in ['task1-commit-a','task2-cherry-pick']:
  sandbox=tempfile.mkdtemp(prefix='nitish-git-lab-');run(['bash',f'04-git-github/scripts/{name}.sh',sandbox])

def docker_apps():
 specs=[('nodejs','nodejs-app',3001,3000),('python','python-app',3002,5000),('java','java-app',3003,8080),('apache','Apache-app',3004,80),('react','React-app',3005,80),('nginx','nginx-app',3006,80)]
 for name,folder,hp,cp in specs:
  tag=f'homework-hello-{name}';run(['docker','rm','-f',tag],check=False);run(['docker','build','-t',tag,f'05-docker-fundamentals/{folder}']);run(['docker','run','-d','--name',tag,'-p',f'127.0.0.1:{hp}:{cp}',tag])
  body=run(['curl','--retry','30','--retry-all-errors','--retry-connrefused','--retry-delay','1','--fail',f'http://127.0.0.1:{hp}'])
  if name!='react' and not ('Hello' in body and 'World' in body):raise RuntimeError('Hello World missing')
  if name=='react':
   import re
   js=re.search(r'src="([^"]+\.js)"',body).group(1)
   text=subprocess.check_output(['curl','-fsS',f'http://127.0.0.1:{hp}{js}'],text=True);out('$ curl --fail [React JavaScript bundle]');out('React bundle contains Hello/World: '+str('Hello' in text and 'World' in text));assert 'Hello' in text and 'World' in text
 run(['docker','ps','--filter','name=homework-hello','--format','table {{.Names}}\t{{.Status}}\t{{.Ports}}'])

def multistage():
 f='06-dockerfiles-and-images/multistage-app';run(['docker','build','-t','homework-multistage',f]);run(['docker','run','-d','--name','homework-multistage','-p','127.0.0.1:8080:8080','homework-multistage'])
 body=run(['curl','--retry','20','--retry-all-errors','--retry-connrefused','--retry-delay','1','--fail','http://127.0.0.1:8080'])
 assert 'Hello World from Docker multi-stage build' in body
 run(['docker','ps','--filter','name=homework-multistage','--format','table {{.Names}}\t{{.Status}}\t{{.Ports}}']);run(['docker','port','homework-multistage']);run(['docker','image','inspect','homework-multistage','--format','{{.Size}} bytes; user={{.Config.User}}'])
 # The three application types were already built/run in Session 6; record fresh access.
 for port in [3001,3002,3003]:run(['curl','--fail',f'http://127.0.0.1:{port}'])

def docker_networks():
 for n in ['front','back','isolated']:run(['docker','network','create','homework-'+n])
 run(['docker','run','-d','--name','homework-front','--network','homework-front','nginx:1.29-alpine'])
 run(['docker','run','-d','--name','homework-db','--network','homework-back','-e','MYSQL_ROOT_PASSWORD=classroom-example-only','mysql:8.0'])
 run(['docker','run','-d','--name','homework-backend','--network','homework-back','alpine:latest','sleep','3600'])
 run(['docker','network','connect','homework-front','homework-backend'])
 run(['docker','inspect','homework-backend','--format','{{json .NetworkSettings.Networks}}'])
 run(['docker','exec','homework-backend','wget','-qO-','http://homework-front'])
 run(['docker','exec','homework-backend','nc','-z','-w','5','homework-db','3306'],check=False)
 run(['docker','exec','homework-front','nslookup','homework-db'],check=False)
 site=ROOT/'07-docker-network-volumes/bind-mount-site';site.mkdir(exist_ok=True);(site/'index.html').write_text('Hello students\n')
 run(['docker','run','-d','--name','homework-bind','-p','127.0.0.1:18081:80','-v',f'{site}:/usr/share/nginx/html:ro,z','nginx:1.29-alpine'])
 run(['curl','--retry','10','--retry-all-errors','--retry-connrefused','--retry-delay','1','--fail','http://127.0.0.1:18081'])
 (site/'index.html').write_text('Hello students - updated without restarting the container\n')
 run(['curl','--fail','http://127.0.0.1:18081']);run(['docker','inspect','homework-bind','--format','started={{.State.StartedAt}}'])
 # Host network on Linux exposes Apache's own port 80, with no -p mapping.
 run(['docker','run','-d','--name','homework-host-apache','--network','host','httpd:2.4'])
 run(['curl','--retry','10','--retry-all-errors','--retry-connrefused','--retry-delay','1','--fail','http://127.0.0.1:80']);run(['docker','inspect','homework-host-apache','--format','{{.HostConfig.NetworkMode}}'])
 run(['docker','stop','homework-host-apache'])
 run(['docker','exec','homework-backend','nc','-z','-w','5','homework-db','3306'],check=False)

funcs={1:linux,3:shell,4:networking,5:git,6:docker_apps,7:multistage,8:docker_networks}
for n in map(int,sys.argv[1:]):
 d=ROOT/folders[n]/'outputs';d.mkdir(exist_ok=True)
 with (d/'current-run.txt').open('w') as f:
  log=f;out('Captured '+datetime.datetime.now(datetime.timezone.utc).isoformat());funcs[n]();out('LAB EXECUTION FINISHED')
