# Network Automation Lab + Monitoring Stack

## Purpose
This project is a multi-AS BGP/IS-IS network lab built to demonstrate Python automation, network monitoring, and failure handling in a containerized environment. It uses `containerlab` and `FRRouting`.

## Topology Diagram
*(Placeholder for diagram)*
- AS 65001: R11, R12, R13
- AS 65002: R21, R22
- AS 65003: R31

## Quickstart

To launch the lab:
```bash
make up
```
This will deploy the containerlab topology and load the initial router configurations.

To tear down the lab:
```bash
make down
```

## How to change the intent
1. Edit `topology/intent.yml` (the single source of truth).
2. Run `python3 automation/generate.py` to update the FRR templates.
3. Run `make deploy` to push the configurations to the running lab.

## How to run verification
Run `make verify` to execute `automation/verify.py`. This script ensures IS-IS adjacencies are up and BGP sessions are established across all routers.

To run the Python unit tests for the automation scripts:
```bash
make test
```
