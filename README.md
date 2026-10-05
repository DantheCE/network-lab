# Automated Network Lab and Observability Stack

This repository contains two linked projects. The projects show skills in network production engineering.

1. **Project 1: Automated Network Lab**
   This project is a network lab. It uses `containerlab`, `FRRouting`, and a custom Python toolchain. The lab contains multiple Autonomous Systems (AS). The routers use BGP and IS-IS.

2. **Project 2: Observability Stack**
   This project is a monitoring stack. It uses Prometheus, Alertmanager, and Grafana. The monitoring stack connects to the routers through sidecar exporters. The stack includes Alertmanager rules to detect dropped BGP sessions and high CPU use.

## Architecture Diagram

```mermaid
graph TD
    classDef asn fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef router fill:#d4e6f1,stroke:#2874a6,stroke-width:2px,color:#000;
    classDef host fill:#d5f5e3,stroke:#239b56,stroke-width:2px,color:#000;
    classDef monitor fill:#fcf3cf,stroke:#f1c40f,stroke-width:2px,color:#000;

    subgraph AS65001 [AS 65001: IS-IS and iBGP]
        direction TB
        R11((R11<br>10.255.0.11))
        R12((R12<br>10.255.0.12))
        R13((R13<br>10.255.0.13))
        
        R11 <---|IS-IS and iBGP|---> R12
        R11 <---|IS-IS and iBGP|---> R13
        R12 <---|IS-IS and iBGP|---> R13
    end
    class AS65001 asn;

    subgraph AS65002 [AS 65002: IS-IS and iBGP]
        direction TB
        R21((R21<br>10.255.0.21))
        R22((R22<br>10.255.0.22))
        H1[Host 1]
        H2[Host 2]

        R21 <---|IS-IS and iBGP|---> R22
        R21 --- H1
        R22 --- H2
    end
    class AS65002 asn;

    subgraph AS65003 [AS 65003: Single Node]
        R31((R31<br>10.255.0.31))
    end
    class AS65003 asn;

    %% External Connections
    R11 <===|eBGP Primary<br>Local Pref 200|===> R21
    R12 <===|eBGP Backup<br>Local Pref 100|===> R22
    R13 <===|eBGP|===> R31

    %% Observers
    subgraph Observability [Observability Stack]
        Prometheus[Prometheus<br>:9090]
        Grafana[Grafana<br>:3000]
        Alertmanager[Alertmanager<br>:9093]
        Prometheus --- Grafana
        Prometheus --- Alertmanager
    end
    class Observability monitor;

    Prometheus -.->|Scrapes Exporters| R11
    Prometheus -.->|Scrapes Exporters| R21

    class R11,R12,R13,R21,R22,R31 router;
    class H1,H2 host;
    class Prometheus,Grafana,Alertmanager monitor;
```

## Quickstart

**Requirements:** You must have a Linux host (or WSL2/VM). The host must have Docker, `containerlab`, and `docker compose` installed.

1. **Start the Network Lab (Project 1)**
   ```bash
   make up
   ```
   This command starts the containerlab topology. It also starts the exporter sidecars.

2. **Deploy the Configurations**
   ```bash
   make deploy
   ```
   This command reads the `topology/intent.yml` file. It generates Jinja2 configuration files. It then sends the files to the routers. The FRR reload scripts apply the configurations safely.

3. **Verify the Connections**
   ```bash
   make verify
   ```
   This command runs a Python script. The script checks the FRR JSON outputs. It confirms that all IS-IS adjacencies and BGP sessions have an `Established` status.

4. **Start the Monitoring Stack (Project 2)**
   ```bash
   make monitoring-up
   ```
   This command uses docker compose to start Prometheus (port 9090), Alertmanager (port 9093), and Grafana (port 3000). The command automatically provisions the Grafana dashboards.

To stop the environment and remove the containers, run this command:
```bash
make clean
```

## How to Change the Intent (Infrastructure as Code)

1. Edit the `topology/intent.yml` file. This file is the single source of truth.
2. Run `python3 automation/generate.py`. This script updates the FRR templates and the Containerlab topology file.
3. Run `make deploy`. This command sends the new configurations to the active network lab.

## Unit Tests and Integration Tests

To run the Python unit tests for the Pydantic schema validation and the automation scripts, run this command:

```bash
make test
```

*Note: The `test_integration.py` script requires Docker. If Docker is not available, the script skips the tests automatically.*
