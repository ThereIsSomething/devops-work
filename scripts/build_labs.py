from pathlib import Path
import yaml, shutil
ROOT=Path(__file__).resolve().parents[1]
def write(path, text):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def save(path,*objects):write(path,yaml.safe_dump_all(objects,sort_keys=False))
def deployment(name='web',image='nginx:1.28-alpine',replicas=2,labels=None):
 labels=labels or {'app':name}
 return {'apiVersion':'apps/v1','kind':'Deployment','metadata':{'name':name},'spec':{'replicas':replicas,'selector':{'matchLabels':labels},'template':{'metadata':{'labels':labels},'spec':{'containers':[{'name':'web','image':image,'ports':[{'containerPort':80}],'resources':{'requests':{'cpu':'25m','memory':'16Mi'},'limits':{'cpu':'250m','memory':'64Mi'}}}]}}}}
def service(name='web',selector=None,typ='ClusterIP',**kwargs):
 return {'apiVersion':'v1','kind':'Service','metadata':{'name':name},'spec':{'type':typ,'selector':selector or {'app':'web'},'ports':[{'port':80,'targetPort':80}],**kwargs}}
def pod(name,command=None,image='busybox:1.37'):
 c={'name':'app','image':image}
 if command:c['command']=['sh','-c',command]
 return {'apiVersion':'v1','kind':'Pod','metadata':{'name':name},'spec':{'restartPolicy':'Never','containers':[c]}}
save('08-kubernetes-fundamentals/app.yaml',deployment(),service())
for name,labels,replicas in [('rolling',None,3),('blue',{'app':'colour','version':'blue'},2),('green',{'app':'colour','version':'green'},2),('stable',{'app':'canary','version':'stable'},4),('canary',{'app':'canary','version':'canary'},1),('recreate',None,2)]:
 d=deployment(name,replicas=replicas,labels=labels)
 if name=='rolling':d['spec']['strategy']={'type':'RollingUpdate','rollingUpdate':{'maxSurge':1,'maxUnavailable':0}}
 if name=='recreate':d['spec']['strategy']={'type':'Recreate'}
 save(f'09-kubernetes-core-objects/{name}.yaml',d)
save('09-kubernetes-core-objects/services.yaml',service('colour',{'app':'colour','version':'blue'}),service('canary',{'app':'canary'}))
src=ROOT.parent/'devops/session10-k8s-core-objects/pod-lifecycle'
for p in sorted(src.glob('*.yaml')):
 data=yaml.safe_load(p.read_text())
 for c in data['spec'].get('containers',[])+data['spec'].get('initContainers',[]):
  if c['image']=='nginx:1.27':c['image']='nginx:1.28-alpine'
  if c['image']=='busybox:1.36':c['image']='busybox:1.37'
  if p.name=='02-pending.yaml':c['resources']['requests']['cpu']='1000'
 save('09-kubernetes-core-objects/lifecycle/'+p.name,data)
save('10-kubernetes-services/app.yaml',deployment())
for name,typ,opts in [('clusterip','ClusterIP',{}),('nodeport','NodePort',{}),('loadbalancer','LoadBalancer',{}),('headless','ClusterIP',{'clusterIP':'None'})]:save(f'10-kubernetes-services/{name}.yaml',service(name,typ=typ,**opts))
save('10-kubernetes-services/externalname.yaml',{'apiVersion':'v1','kind':'Service','metadata':{'name':'externalname'},'spec':{'type':'ExternalName','externalName':'example.com'}})
cm={'apiVersion':'v1','kind':'ConfigMap','metadata':{'name':'app-config'},'data':{'APP_MODE':'homework','WELCOME':'Hello students'}}
d=deployment();d['spec']['template']['spec']['containers'][0]['envFrom']=[{'configMapRef':{'name':'app-config'}},{'secretRef':{'name':'demo-secret'}}]
save('11-ingress-configmaps-secrets/configmap.yaml',cm)
save('11-ingress-configmaps-secrets/app.yaml',d,service())
save('11-ingress-configmaps-secrets/secret.example.yaml',{'apiVersion':'v1','kind':'Secret','metadata':{'name':'demo-secret'},'type':'Opaque','stringData':{'DEMO_PASSWORD':'classroom-example-only'}})
save('11-ingress-configmaps-secrets/ingress.yaml',{'apiVersion':'networking.k8s.io/v1','kind':'Ingress','metadata':{'name':'web'},'spec':{'ingressClassName':'traefik','rules':[{'host':'homework.local','http':{'paths':[{'path':'/','pathType':'Prefix','backend':{'service':{'name':'web','port':{'number':80}}}}]}}]}})
pvc={'apiVersion':'v1','kind':'PersistentVolumeClaim','metadata':{'name':'web-data'},'spec':{'accessModes':['ReadWriteOnce'],'storageClassName':'standard','resources':{'requests':{'storage':'500Mi'}}}}
d=deployment('web-app');c=d['spec']['template']['spec']['containers'][0];c['volumeMounts']=[{'name':'data','mountPath':'/data'},{'name':'scratch','mountPath':'/scratch'}]
for key in ['startupProbe','readinessProbe','livenessProbe']:c[key]={'httpGet':{'path':'/','port':80},'periodSeconds':5,'failureThreshold':12 if key=='startupProbe' else 3}
d['spec']['template']['spec']['volumes']=[{'name':'data','persistentVolumeClaim':{'claimName':'web-data'}},{'name':'scratch','emptyDir':{}}]
hpa={'apiVersion':'autoscaling/v2','kind':'HorizontalPodAutoscaler','metadata':{'name':'web-app'},'spec':{'scaleTargetRef':{'apiVersion':'apps/v1','kind':'Deployment','name':'web-app'},'minReplicas':2,'maxReplicas':5,'metrics':[{'type':'Resource','resource':{'name':'cpu','target':{'type':'Utilization','averageUtilization':50}}}],'behavior':{'scaleDown':{'stabilizationWindowSeconds':30}}}}
save('12-storage-hpa-probes/app.yaml',pvc,d,service(selector={'app':'web-app'}))
save('12-storage-hpa-probes/hpa.yml',hpa)
save('12-storage-hpa-probes/load-generator.yaml',pod('load-generator','while true; do wget -q -O /dev/null http://web; done'))
save('13-kubernetes-troubleshooting/app.yaml',deployment('troubleshooting-app'),service('troubleshooting-service',{'app':'troubleshooting-app'}))
for name,p in [('crash',pod('crash','echo deliberate-failure; exit 1')),('image',pod('image',image='nginx:homework-does-not-exist')),('pending',pod('pending','sleep 3600')),('creating',pod('creating','sleep 3600')),('config',pod('config','sleep 3600')),('dns',pod('dns','sleep 3600'))]:
 if name=='crash':p['spec']['restartPolicy']='Always'
 if name=='pending':p['spec']['containers'][0]['resources']={'requests':{'cpu':'1000'}}
 if name=='creating':p['spec']['volumes']=[{'name':'missing','secret':{'secretName':'missing-volume'}}];p['spec']['containers'][0]['volumeMounts']=[{'name':'missing','mountPath':'/config'}]
 if name=='config':p['spec']['containers'][0]['envFrom']=[{'configMapRef':{'name':'missing-config'}}]
 if name=='dns':p['spec']['dnsPolicy']='None';p['spec']['dnsConfig']={'nameservers':['192.0.2.1']}
 save(f'13-kubernetes-troubleshooting/{name}.yaml',p)
write('14-helm/chart/Chart.yaml','apiVersion: v2\nname: homework-web\ndescription: Guestbook configuration and rollback exercise\ntype: application\nversion: 0.1.0\nappVersion: "1.28"\n')
write('14-helm/chart/values.yaml','replicaCount: 1\nimage: nginx:1.28-alpine\nmessage: Welcome to my guestbook - version one\n')
write('14-helm/chart/templates/app.yaml','''apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Release.Name }}-page
data:
  index.html: {{ .Values.message | quote }}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      app: {{ .Release.Name }}
  template:
    metadata:
      labels:
        app: {{ .Release.Name }}
      annotations:
        checksum/page: {{ .Values.message | sha256sum | quote }}
    spec:
      containers:
        - name: nginx
          image: {{ .Values.image | quote }}
          ports:
            - containerPort: 80
          readinessProbe:
            httpGet:
              path: /
              port: 80
          resources:
            requests:
              cpu: 25m
              memory: 16Mi
            limits:
              cpu: 250m
              memory: 64Mi
          volumeMounts:
            - name: page
              mountPath: /usr/share/nginx/html
      volumes:
        - name: page
          configMap:
            name: {{ .Release.Name }}-page
---
apiVersion: v1
kind: Service
metadata:
  name: {{ .Release.Name }}
spec:
  selector:
    app: {{ .Release.Name }}
  ports:
    - port: 80
      targetPort: 80
''')
print('Generated manifests and Helm chart.')
