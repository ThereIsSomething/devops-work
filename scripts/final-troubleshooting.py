#!/usr/bin/env python3
from pathlib import Path
import subprocess,shlex,time
r=Path(__file__).resolve().parents[1];k=str(r/'scripts/kubectl');ns='homework-final'
with (r/'final-devops-project/outputs/troubleshooting.txt').open('w') as f:
 def run(args,check=True):
  f.write('$ '+shlex.join(args)+'\n');f.flush();p=subprocess.run(args,cwd=r,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);f.write(p.stdout+f'[exit {p.returncode}]\n');f.flush()
  if check and p.returncode:raise RuntimeError('Command failed')
 def kub(*a,**kw):return run([k,'-n',ns,*a],**kw)
 # Record direct Pod connectivity separately from Service selection/port routing.
 kub('run','challenge-client','--image=busybox:1.37','--restart=Never','--','sleep','1800')
 kub('wait','--for=condition=Ready','pod/challenge-client','--timeout=120s')
 ip=subprocess.check_output([k,'-n',ns,'get','pods','-l','app=taskboard-backend','-o','jsonpath={.items[0].status.podIP}'],text=True)
 kub('exec','challenge-client','--','wget','-qO-',f'http://{ip}:8000/health')
 kub('patch','svc','backend','--type=merge','-p','{"spec":{"selector":{"app":"wrong-backend"}}}')
 kub('get','endpointslices','-l','kubernetes.io/service-name=backend','-o','yaml')
 kub('get','pods','--show-labels')
 kub('exec','challenge-client','--','wget','-T','3','-qO-','http://backend:8000/health',check=False)
 kub('patch','svc','backend','--type=merge','-p','{"spec":{"selector":{"app":"taskboard-backend"}}}')
 kub('patch','svc','backend','--type=json','-p','[{"op":"replace","path":"/spec/ports/0/targetPort","value":8999}]')
 kub('describe','svc','backend')
 kub('exec','challenge-client','--','wget','-T','3','-qO-','http://backend:8000/health',check=False)
 kub('patch','svc','backend','--type=json','-p','[{"op":"replace","path":"/spec/ports/0/targetPort","value":"http"}]')
 kub('exec','challenge-client','--','wget','-qO-','http://backend:8000/health')
 kub('set','image','deployment/backend','backend=homework-taskboard-backend:does-not-exist')
 time.sleep(20);kub('get','pods');kub('get','events','--sort-by=.metadata.creationTimestamp')
 kub('set','image','deployment/backend','backend=homework-taskboard-backend:local')
 kub('rollout','status','deployment/backend','--timeout=180s')
 kub('exec','challenge-client','--','nslookup','backend.homework-final.svc.cluster.local')
 kub('exec','challenge-client','--','wget','-qO-','http://backend:8000/ready')
 kub('delete','pod','challenge-client')
