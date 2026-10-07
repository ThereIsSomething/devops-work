#!/usr/bin/env python3
"""Run isolated homework labs and capture actual commands, output and exit status."""
from pathlib import Path
import subprocess, shlex, sys, time, datetime, json
ROOT=Path(__file__).resolve().parents[1];K=str(ROOT/'scripts/kubectl'); log=None
folders={9:'08-kubernetes-fundamentals',10:'09-kubernetes-core-objects',11:'10-kubernetes-services',12:'11-ingress-configmaps-secrets',13:'12-storage-hpa-probes',14:'13-kubernetes-troubleshooting',15:'14-helm'}
def record(s):
 print(s,flush=True)
 if log:log.write(s+'\n');log.flush()
def run(args,check=True,timeout=180):
 record('$ '+shlex.join(map(str,args)))
 p=subprocess.run(list(map(str,args)),cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
 record(p.stdout.rstrip());record(f'[exit {p.returncode}]')
 if check and p.returncode:raise RuntimeError('Command failed')
 return p.stdout
ns=''
def k(*args,**kw):return run([K,'-n',ns,*args],**kw)
def apply(path):return k('apply','-f',path)
def wait(name):k('rollout','status','deployment/'+name,'--timeout=180s')
def client():
 k('run','client','--image=busybox:1.37','--restart=Never','--','sleep','7200')
 k('wait','--for=condition=Ready','pod/client','--timeout=120s')
def http(host):return k('exec','client','--','wget','-qO-',f'http://{host}',check=False)
def snapshot():k('get','pods,deploy,rs,svc','-o','wide')
def lab9():
 run(['minikube','status']);k('cluster-info');k('get','nodes','-o','wide');k('get','pods','-n','kube-system')
 apply(f'{folders[9]}/app.yaml');wait('web');snapshot();k('explain','deployment.spec.replicas')
 client();http('web');k('scale','deployment/web','--replicas=3');wait('web');k('set','image','deployment/web','web=nginx:1.29-alpine');wait('web');k('rollout','history','deployment/web');k('rollout','undo','deployment/web');wait('web');snapshot()
def lab10():
 f=folders[10]
 for name in ['rolling','blue','green','stable','canary','recreate']:apply(f'{f}/{name}.yaml');wait(name)
 apply(f'{f}/services.yaml');client()
 for name,version in [('blue','blue'),('green','green'),('stable','stable'),('canary','canary')]:k('exec','deployment/'+name,'--','sh','-c',f"printf '{version}\\n' > /usr/share/nginx/html/version")
 k('get','rs');k('set','image','deployment/rolling','web=nginx:1.29-alpine');k('get','pods,rs');wait('rolling');k('get','rs')
 http('colour/version');k('patch','svc','colour','--type=merge','-p','{"spec":{"selector":{"app":"colour","version":"green"}}}');http('colour/version')
 k('get','endpointslices','-l','kubernetes.io/service-name=canary','-o','wide')
 k('exec','client','--','sh','-c','for i in $(seq 1 50); do wget -qO- http://canary/version; done | sort | uniq -c')
 k('set','image','deployment/recreate','web=nginx:1.29-alpine');k('get','pods,rs');wait('recreate');k('get','events','--sort-by=.metadata.creationTimestamp')
 for p in sorted((ROOT/f/'lifecycle').glob('*.yaml')):apply(str(p.relative_to(ROOT)))
 time.sleep(40)
 for p in sorted((ROOT/f/'lifecycle').glob('*.yaml')):
  import yaml
  name=yaml.safe_load(p.read_text())['metadata']['name'];k('get','pod',name,'-o','wide');k('describe','pod',name);k('logs',name,'--all-containers=true',check=False)
 k('delete','pod','lifecycle-termination','--wait=true');snapshot()
def lab11():
 f=folders[11];apply(f'{f}/app.yaml');wait('web')
 for name in ['clusterip','nodeport','loadbalancer','externalname','headless']:apply(f'{f}/{name}.yaml')
 client();k('get','svc','-o','wide')
 for name in ['clusterip','nodeport','loadbalancer','headless']:http(name)
 for name in ['clusterip','headless','externalname']:k('exec','client','--','nslookup',f'{name}.{ns}.svc.cluster.local')
 port=k('get','svc','nodeport','-o','jsonpath={.spec.ports[0].nodePort}').split('\n')[0]
 ip=run(['minikube','ip']).split('\n')[0];run(['curl','--fail','--max-time','10',f'http://{ip}:{port}'])
 # A pending external IP is real Minikube behavior; a managed external load balancer is not fabricated.
 k('describe','svc','loadbalancer');k('get','configmap','coredns','-n','kube-system','-o','yaml');k('logs','-n','kube-system','-l','k8s-app=kube-dns','--tail=20')
def lab12():
 f=folders[12];apply(f'{f}/configmap.yaml');apply(f'{f}/secret.example.yaml');apply(f'{f}/app.yaml');wait('web')
 k('exec','deployment/web','--','sh','-c','printf "APP_MODE=%s\\nWELCOME=%s\\n" "$APP_MODE" "$WELCOME"; test "$DEMO_PASSWORD" = "classroom-example-only" && echo "Demo Secret injected: verified"')
 apply(f'{f}/ingress.yaml');k('get','ingress');client();http('web')
 # Root-cause reproduction from instructor's secret-base64-gotcha.md; only a public dummy value.
 run(['bash','-c','echo "mypassword" | base64; printf %s "mypassword" | base64; echo; echo "mypassword" | od -An -tx1; printf %s "mypassword" | od -An -tx1'])
 k('create','secret','generic','newline-demo','--from-literal=PASSWORD=mypassword\n')
 k('get','secret','newline-demo','-o','jsonpath={.data.PASSWORD}')
 k('delete','secret','newline-demo');k('create','secret','generic','newline-demo','--from-literal=PASSWORD=mypassword');k('get','secret','newline-demo','-o','jsonpath={.data.PASSWORD}')
def lab13():
 f=folders[13];apply(f'{f}/app.yaml');wait('web-app');apply(f'{f}/hpa.yml');k('get','pvc,pv,sc');client();http('web')
 pods=json.loads(k('get','pods','-l','app=web-app','-o','json'))['items'];old=pods[0]['metadata']['name']
 k('exec',old,'--','sh','-c','echo persistent-homework-data > /data/student.txt; echo ephemeral-data > /scratch/transient.txt; cat /data/student.txt')
 k('delete','pod',old);wait('web-app')
 pods=json.loads(k('get','pods','-l','app=web-app','-o','json'))['items'];new=next(p['metadata']['name'] for p in pods if p['metadata']['name'] not in [q['metadata']['name'] for q in json.loads('{}').get('items',[])])
 k('exec',new,'--','cat','/data/student.txt');k('get','hpa');k('top','pods',check=False)
 apply(f'{f}/load-generator.yaml')
 # Deliberate CPU work in the application containers makes CPU scaling repeatable.
 procs=[]
 for p in pods:procs.append(subprocess.Popen([K,'-n',ns,'exec',p['metadata']['name'],'--','sh','-c','timeout 150 sh -c "while true; do :; done"'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
 record('CPU workload: bounded 150-second busy loop in each application Pod; HTTP load-generator also running.')
 for i in range(8):
  time.sleep(20);k('get','hpa');k('top','pods',check=False);k('get','pods')
  if '5' in k('get','deployment','web-app','-o','jsonpath={.spec.replicas}'):break
 for p in procs:p.wait(timeout=180)
 k('delete','pod','load-generator');k('describe','hpa');k('get','pods','-o','wide')
def lab14():
 f=folders[14];apply(f'{f}/app.yaml');wait('troubleshooting-app');client()
 for name in ['crash','image','pending','creating','config','dns']:apply(f'{f}/{name}.yaml')
 time.sleep(35)
 k('get','pods','-o','wide');k('events',check=False);k('explain','pod.spec.containers');k('top','pods',check=False)
 for name in ['crash','image','pending','creating','config','dns']:k('describe','pod',name)
 k('logs','crash','--previous',check=False);k('exec','dns','--','nslookup','kubernetes.default.svc.cluster.local',check=False,timeout=40)
 k('patch','svc','troubleshooting-service','--type=merge','-p','{"spec":{"selector":{"app":"wrong-app"}}}');k('get','endpointslices','-l','kubernetes.io/service-name=troubleshooting-service','-o','yaml');k('get','pods','--show-labels')
 k('patch','svc','troubleshooting-service','--type=merge','-p','{"spec":{"selector":{"app":"troubleshooting-app"}}}');http('troubleshooting-service')
 k('create','secret','generic','missing-volume','--from-literal=demo=public-dummy');k('create','configmap','missing-config','--from-literal=MODE=fixed')
 k('wait','--for=condition=Ready','pod/creating','pod/config','--timeout=120s')
 # Immutable Pod fields require replacing the deliberately broken standalone Pods.
 for name in ['crash','image','pending','dns']:
  k('delete','pod',name);k('run',name,'--image=busybox:1.37','--restart=Never','--','sleep','3600');k('wait','--for=condition=Ready','pod/'+name,'--timeout=120s')
 k('exec','dns','--','nslookup','kubernetes.default.svc.cluster.local');k('exec','client','--','wget','-qO-','http://troubleshooting-service');snapshot()
def lab15():
 f=folders[15];tmp=ROOT/f/'generated-example'
 if not tmp.exists():run(['helm','create',str(tmp)])
 run(['helm','repo','add','traefik','https://traefik.github.io/charts','--force-update']);run(['helm','repo','update']);run(['helm','search','repo','traefik/traefik','--versions'],timeout=180)
 run(['helm','lint',f'{f}/chart']);run(['helm','template','guestbook',f'{f}/chart','-n',ns])
 run(['helm','upgrade','--install','guestbook',f'{f}/chart','-n',ns,'--wait','--timeout','180s']);client()
 for cmd in [['list'],['status','guestbook'],['get','values','guestbook'],['get','manifest','guestbook']]:run(['helm',*cmd,'-n',ns])
 http('guestbook')
 for version in ['two','three']:
  run(['helm','upgrade','guestbook',f'{f}/chart','-n',ns,'--set',f'message=Welcome to my guestbook - version {version}','--wait','--timeout','180s']);http('guestbook')
 run(['helm','history','guestbook','-n',ns]);run(['helm','rollback','guestbook','1','-n',ns,'--wait','--timeout','180s']);http('guestbook');run(['helm','history','guestbook','-n',ns]);run(['helm','uninstall','guestbook','-n',ns]);run(['helm','list','-n',ns])
for n in map(int,sys.argv[1:] or range(9,16)):
 ns=f'homework-s{n:02}';path=Path('/tmp/devops-homework')/folders[n];path.mkdir(parents=True,exist_ok=True)
 with (path/'run.txt').open('w') as out:
  log=out;record('Captured '+datetime.datetime.now(datetime.timezone.utc).isoformat());run([K,'create','namespace',ns],check=False)
  try:globals()[f'lab{n}']();record('LAB EXECUTION FINISHED')
  except Exception as e:record(f'LAB INCOMPLETE: {e}');raise
 log=None
