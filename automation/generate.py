#!/usr/bin/env python3
import os
import yaml
from jinja2 import Environment, FileSystemLoader
from lib.schema import Intent

def load_intent(filepath: str) -> Intent:
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    return Intent(**data)

def generate_configs(intent: Intent, template_dir: str, output_dir: str):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("frr.conf.j2")

    for r_name, r_data in intent.routers.items():
        ctx = {
            "router_name": r_name,
            "router": r_data,
            "policies": intent.policies,
            "interfaces": [],
            "ibgp_peers": [],
            "ebgp_peers": []
        }

        # iBGP peers
        for peer_name, peer_data in intent.routers.items():
            if peer_data.asn == r_data.asn and peer_name != r_name:
                ctx["ibgp_peers"].append(peer_data)

        # Links
        for link in intent.links:
            if link.node_a == r_name or link.node_b == r_name:
                is_a = link.node_a == r_name
                intf_name = link.int_a if is_a else link.int_b
                intf_ip = link.ip_a if is_a else link.ip_b
                peer_name = link.node_b if is_a else link.node_a
                
                ctx["interfaces"].append({
                    "name": intf_name,
                    "ip": intf_ip,
                    "type": link.type
                })
                
                if link.type == "ebgp":
                    peer_data = intent.routers[peer_name]
                    peer_ip = str(link.ip_b).split("/")[0] if is_a else str(link.ip_a).split("/")[0]
                    local_pref = link.local_pref_a if is_a else link.local_pref_b
                    
                    ctx["ebgp_peers"].append({
                        "ip": peer_ip,
                        "asn": peer_data.asn,
                        "local_pref": local_pref
                    })

        rendered = template.render(**ctx)
        
        r_dir = os.path.join(output_dir, r_name)
        os.makedirs(r_dir, exist_ok=True)
        with open(os.path.join(r_dir, "frr.conf"), "w") as f:
            f.write(rendered)
        with open(os.path.join(r_dir, "daemons"), "w") as f:
            f.write("bgpd=yes\nisisd=yes\n")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    intent = load_intent(os.path.join(base_dir, "../topology/intent.yml"))
    generate_configs(intent, os.path.join(base_dir, "templates"), os.path.join(base_dir, "../topology/configs"))
    print("Configuration generation complete.")
