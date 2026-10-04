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
*(To be implemented in Milestone 3: Intent-driven automation)*
Currently, configs are stored in `topology/configs/`.

## How to run verification
*(To be implemented in Milestone 3: Verification script)*
Currently, verify manually using `docker exec -it clab-network-lab-<node> vtysh`.
