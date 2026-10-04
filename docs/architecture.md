# Network Architecture

## Design Choices

### IGP (IS-IS)
IS-IS was chosen as the Interior Gateway Protocol for the multi-router autonomous systems (AS 65001 and AS 65002) for several reasons:
- Protocol independence (routes at Layer 2 via NSAP), making it easier to adopt IPv6 later.
- Link-state nature provides fast convergence and complete visibility of the internal topology.
- We implemented a single Level-2 area to simplify the initial deployment since our domain is relatively small.

### iBGP
Inside AS 65001 and AS 65002, a full mesh of iBGP is used. Since the scale is small, route reflectors were not strictly necessary. iBGP is peered over Loopback interfaces (10.255.0.x) rather than physical links, ensuring sessions stay up even if a physical intra-AS link drops, as long as an alternate path exists via IS-IS.

### eBGP and Policy Rationale
eBGP is used for inter-AS routing over direct point-to-point links.
1. **Redundancy & Local Preference**: The path between AS 65001 and 65002 has a primary connection (R11-R21) and a backup connection (R12-R22). Local preference is heavily weighted towards the primary path (`LocalPref = 200`), falling back to `100` for the backup link. 
2. **Prefix Filtering**: We apply strict incoming and outgoing prefix-lists restricting routing updates to expected host subnets (e.g. `10.10.0.0/16 le 24`). Bogons or unallocated IPs are silently dropped.
3. **Max Prefix Limits**: All eBGP sessions are configured to shut down if they receive more than 100 prefixes, mitigating potential route-leak explosions.
4. **Community Tagging**: Routes advertised to peers are tagged with the origin ASN (e.g. `65001:1`), which allows upstream providers to build policies based on origin rather than raw prefixes.
