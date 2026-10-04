import pytest
from pydantic import ValidationError
from automation.lib.schema import Intent

def test_valid_intent():
    data = {
        "routers": {
            "r1": {
                "asn": 65000,
                "loopback": "1.1.1.1",
                "isis_net": "49.0001.0102.5500.0011.00",
                "originate_prefixes": ["10.10.1.0/24"]
            }
        },
        "links": [
            {
                "node_a": "r1",
                "int_a": "eth1",
                "ip_a": "10.0.0.0/31",
                "node_b": "r2",
                "int_b": "eth1",
                "ip_b": "10.0.0.1/31",
                "type": "isis"
            }
        ],
        "policies": {
            "allowed_prefixes": ["10.10.0.0/16 le 24"],
            "ebgp_max_prefix": 100
        }
    }
    intent = Intent(**data)
    assert intent.routers["r1"].asn == 65000
    assert len(intent.links) == 1

def test_invalid_intent_missing_asn():
    data = {
        "routers": {
            "r1": {
                "loopback": "1.1.1.1"
            }
        },
        "links": [],
        "policies": {
            "allowed_prefixes": [],
            "ebgp_max_prefix": 100
        }
    }
    with pytest.raises(ValidationError):
        Intent(**data)

def test_invalid_ip_address():
    data = {
        "routers": {
            "r1": {
                "asn": 65000,
                "loopback": "not-an-ip"
            }
        },
        "links": [],
        "policies": {
            "allowed_prefixes": [],
            "ebgp_max_prefix": 100
        }
    }
    with pytest.raises(ValidationError):
        Intent(**data)
