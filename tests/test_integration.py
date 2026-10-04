import pytest
import subprocess
import time

# Marker to skip if containerlab is not available
pytestmark = pytest.mark.skipif(
    subprocess.run(["docker", "ps"], capture_output=True).returncode != 0,
    reason="Docker is not available"
)

def run_cmd(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, shell=True)

def test_deploy_and_verify():
    # Deploy configs
    deploy_res = run_cmd("python3 automation/deploy.py")
    assert deploy_res.returncode == 0
    
    # Wait for convergence
    time.sleep(10)
    
    # Verify state
    verify_res = run_cmd("python3 automation/verify.py")
    assert verify_res.returncode == 0
    assert "Verification PASSED" in verify_res.stdout

def test_failure_reconvergence():
    # Simulate link failure on primary path R11-R21
    run_cmd("docker exec clab-network-lab-r11 ip link set eth3 down")
    
    # Wait for BGP hold timer to drop session and reconverge to backup path
    time.sleep(15) 
    
    # Verify e2e ping still works via backup path R12-R22
    ping_res = run_cmd("docker exec clab-network-lab-h1 ping -c 3 10.10.2.10")
    assert ping_res.returncode == 0
    
    # Restore link
    run_cmd("docker exec clab-network-lab-r11 ip link set eth3 up")
    time.sleep(15)
    
    # Verify ping again
    ping_res = run_cmd("docker exec clab-network-lab-h1 ping -c 3 10.10.2.10")
    assert ping_res.returncode == 0
