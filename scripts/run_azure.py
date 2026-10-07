#!/usr/bin/env python3
"""Real Azure lab runner. Local authentication/state stay outside public evidence."""
import json, os, pathlib, subprocess, sys, time
ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "18-cloud-terraform/outputs"
OUT.mkdir(exist_ok=True)
sub = subprocess.check_output(["az", "account", "show", "--query", "id", "-o", "tsv"], text=True).strip()
env = dict(os.environ, TF_VAR_subscription_id=sub, TF_IN_AUTOMATION="1")
rg = "rg-devops-homework"
# Reuse the current account on a recovery run instead of replacing it.
state_dir=ROOT / "18-cloud-terraform/azure-alternative"
existing=subprocess.run(["terraform", "-chdir="+str(state_dir), "output", "-raw", "storage_account"],capture_output=True,text=True)
account=existing.stdout.strip() if existing.returncode==0 else "nitishhw" + str(int(time.time()))

def run(args, log, check=True, extra=None):
    print("$ " + " ".join(args), flush=True)
    with open(log, "a") as f:
        f.write("\n$ " + " ".join(args).replace(sub, "<subscription-id>") + "\n")
        result = subprocess.run(args, cwd=ROOT, env=env | (extra or {}), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        f.write(result.stdout.replace(sub, "<subscription-id>"))
        f.write("\n[exit " + str(result.returncode) + "]\n")
    print(result.stdout[-1200:].replace(sub,"<subscription-id>"), flush=True)
    if check and result.returncode:
        raise RuntimeError("Command failed: " + args[0])
    return result

log=OUT/"azure-run.txt"
run(["az", "group", "create", "--name", rg, "--location", "centralindia", "--tags", "purpose=devops-homework", "--query", "{name:name,location:location,provisioningState:properties.provisioningState}", "-o", "json"],log)
# Entra-based storage polling needs a data-plane role, even for an Owner login.
principal = subprocess.check_output(["az", "ad", "signed-in-user", "show", "--query", "id", "-o", "tsv"], text=True).strip()
scope = "/subscriptions/" + sub + "/resourceGroups/" + rg
assignments = json.loads(subprocess.check_output(["az", "role", "assignment", "list", "--scope", scope, "-o", "json"], text=True))
if not any(a.get("principalId") == principal and a.get("roleDefinitionName") == "Storage Blob Data Contributor" for a in assignments):
    run(["az", "role", "assignment", "create", "--assignee-object-id", principal, "--assignee-principal-type", "User", "--role", "Storage Blob Data Contributor", "--scope", scope, "--query", "roleDefinitionName", "-o", "tsv"], log)
key=pathlib.Path("/tmp/devops-homework-azure-key")
if not key.exists():
    subprocess.run(["ssh-keygen","-q","-t","ed25519","-f",str(key),"-N",""],check=True)
env.update(TF_VAR_storage_account_name=account, TF_VAR_enable_vm="true", TF_VAR_vm_size="Standard_D2s_v3", TF_VAR_ssh_public_key=key.with_suffix(".pub").read_text().strip())
tf=["terraform","-chdir=18-cloud-terraform/azure-alternative"]
for cmd in [["init","-input=false","-no-color"],["fmt","-check"],["validate","-no-color"],["plan","-out=lab.tfplan","-input=false","-no-color"],["apply","-input=false","-no-color","lab.tfplan"],["show","-no-color"],["output","-no-color"]]:
    run(tf+cmd,log)
url=subprocess.check_output(tf+["output","-raw","web_url"],env=env,text=True).strip()
run(["curl","--fail","--retry","30","--retry-all-errors","--retry-delay","5",url],log)
print("VM lab ready. Resources retained only for current exercise; destroy is the next phase.",flush=True)
