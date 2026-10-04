# Addressing Plan

## Autonomous Systems
| Router | AS Number |
|---|---|
| R11, R12, R13 | 65001 |
| R21, R22 | 65002 |
| R31 | 65003 |

## Loopback Interfaces (10.255.0.0/24)
| Router | IP Address |
|---|---|
| R11 | 10.255.0.11/32 |
| R12 | 10.255.0.12/32 |
| R13 | 10.255.0.13/32 |
| R21 | 10.255.0.21/32 |
| R22 | 10.255.0.22/32 |
| R31 | 10.255.0.31/32 |

## Point-to-Point Links (10.0.0.0/24)
| Link | IP Network | Node A (IP) | Node B (IP) | Routing |
|---|---|---|---|---|
| R11 - R12 | 10.0.0.0/31 | R11 eth1 (10.0.0.0) | R12 eth1 (10.0.0.1) | IS-IS |
| R12 - R13 | 10.0.0.2/31 | R12 eth2 (10.0.0.2) | R13 eth1 (10.0.0.3) | IS-IS |
| R13 - R11 | 10.0.0.4/31 | R13 eth2 (10.0.0.4) | R11 eth2 (10.0.0.5) | IS-IS |
| R21 - R22 | 10.0.0.6/31 | R21 eth1 (10.0.0.6) | R22 eth1 (10.0.0.7) | IS-IS |
| R11 - R21 | 10.0.0.8/31 | R11 eth3 (10.0.0.8) | R21 eth2 (10.0.0.9) | eBGP (Primary) |
| R12 - R22 | 10.0.0.10/31 | R12 eth3 (10.0.0.10) | R22 eth2 (10.0.0.11) | eBGP (Backup) |
| R13 - R31 | 10.0.0.12/31 | R13 eth3 (10.0.0.12) | R31 eth1 (10.0.0.13) | eBGP |

## Customer/Host Prefixes
| Host | Gateway Router | IP Network | Gateway IP | Host IP |
|---|---|---|---|---|
| H1 | R11 | 10.10.1.0/24 | R11 eth4 (10.10.1.1) | H1 eth1 (10.10.1.10) |
| H2 | R31 | 10.10.2.0/24 | R31 eth2 (10.10.2.1) | H2 eth1 (10.10.2.10) |

## IS-IS NET Addresses
Format: `49.<Area>.<System ID>.00`
- Area `0001` for AS 65001
- Area `0002` for AS 65002
- System ID: Zero-padded loopback (e.g. `0102.5500.0011` for 10.255.0.11)
