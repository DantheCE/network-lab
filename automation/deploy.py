#!/usr/bin/env python3
import argparse
import subprocess
import yaml
import os

def deploy(dry_run=False):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    intent_file = os.path.join(base_dir, "../topology/intent.yml")
    with open(intent_file, "r") as f:
        intent = yaml.safe_load(f)
        
    routers = intent.get("routers", {}).keys()
    for r in routers:
        container = f"clab-network-lab-{r}"
        # FRR reload script handles idempotent application
        cmd = ["docker", "exec", container, "python3", "/usr/lib/frr/frr-reload.py"]
        if dry_run:
            cmd.append("--test")
        else:
            cmd.append("--reload")
        cmd.append("/etc/frr/frr.conf")
        
        print(f"Deploying to {r} {'(DRY RUN)' if dry_run else ''}...")
        try:
            res = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if dry_run:
                print(res.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error on {r}: {e.stderr}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    args = parser.parse_args()
    deploy(args.dry_run)
