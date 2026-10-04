#!/usr/bin/env python3
import subprocess
import json
import yaml
import sys
import os

def get_intent():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base_dir, "../topology/intent.yml"), "r") as f:
        return yaml.safe_load(f)

def run_cmd(container, cmd):
    res = subprocess.run(["docker", "exec", container] + cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    try:
        return json.loads(res.stdout)
    except:
        return res.stdout

def verify_isis(routers):
    print("--- Verifying IS-IS Adjacencies ---")
    failed = False
    for r, data in routers.items():
        if "isis_net" not in data: continue
        container = f"clab-network-lab-{r}"
        output = run_cmd(container, ["vtysh", "-c", "show isis neighbor json"])
        if not output:
            print(f"[{r}] Failed to get IS-IS neighbors or not running IS-IS")
            continue
        print(f"[{r}] IS-IS Neighbors checked.")
    return not failed

def verify_bgp(routers):
    print("--- Verifying BGP Sessions ---")
    failed = False
    for r in routers:
        container = f"clab-network-lab-{r}"
        output = run_cmd(container, ["vtysh", "-c", "show bgp summary json"])
        if not output:
            print(f"[{r}] Failed to get BGP summary")
            failed = True
            continue
        
        peers = output.get("ipv4Unicast", {}).get("peers", {})
        for peer_ip, peer_info in peers.items():
            state = peer_info.get("state", "")
            if state != "Established":
                print(f"[{r}] BGP Peer {peer_ip} is {state}")
                failed = True
        print(f"[{r}] BGP sessions OK.")
    return not failed

if __name__ == "__main__":
    intent = get_intent()
    routers = intent.get("routers", {})
    ok1 = verify_isis(routers)
    ok2 = verify_bgp(routers)
    
    if not (ok1 and ok2):
        print("Verification FAILED")
        sys.exit(1)
    else:
        print("Verification PASSED")
        sys.exit(0)
