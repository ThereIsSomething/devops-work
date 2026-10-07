#!/usr/bin/env python3
"""Embed excerpts from real transcripts without inventing or rewriting output."""
from pathlib import Path
import re
r=Path(__file__).resolve().parents[1]
folders=['01-linux-fundamentals','02-shell-scripting','03-networking','04-git-github','05-docker-fundamentals','06-dockerfiles-and-images','07-docker-network-volumes','08-kubernetes-fundamentals','09-kubernetes-core-objects','10-kubernetes-services','11-ingress-configmaps-secrets','12-storage-hpa-probes','13-kubernetes-troubleshooting','14-helm','19-monitoring-gitops']
for folder in folders:
 d=r/folder;p=d/'README.md'
 s=p.read_text().split('<!-- EVIDENCE -->')[0].rstrip()+'\n\n<!-- EVIDENCE -->\n'
 for log in sorted((d/'outputs').glob('*.txt')):
  text=log.read_text();text=re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]','',text)
  lines=text.splitlines()
  # Long describe/JSON logs are linked in full, with a labelled beginning/end excerpt.
  if len(lines)>180:
   excerpt='\n'.join(lines[:65])+f'\n\n[Excerpt: {len(lines)-145} intermediate lines omitted; complete transcript linked above.]\n\n'+'\n'.join(lines[-80:])
  else:excerpt=text.rstrip()
  # Use fence length safe even if source text contains Markdown backticks.
  s+=f'\n### {log.name}\n\n[Complete transcript](outputs/{log.name})\n\n````text\n{excerpt}\n````\n'
 p.write_text(s)
print('Updated README evidence excerpts from actual logs.')
