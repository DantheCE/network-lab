from typing import List, Optional, Dict
from pydantic import BaseModel, IPvAnyAddress, IPvAnyNetwork, IPvAnyInterface

class Router(BaseModel):
    asn: int
    loopback: IPvAnyAddress
    isis_net: Optional[str] = None
    originate_prefixes: Optional[List[IPvAnyNetwork]] = []

class Link(BaseModel):
    node_a: str
    int_a: str
    ip_a: IPvAnyInterface
    node_b: str
    int_b: str
    ip_b: IPvAnyInterface
    type: str
    local_pref_a: Optional[int] = None
    local_pref_b: Optional[int] = None

class Policies(BaseModel):
    allowed_prefixes: List[str]
    ebgp_max_prefix: int

class Intent(BaseModel):
    routers: Dict[str, Router]
    links: List[Link]
    policies: Policies
