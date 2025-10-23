import os
import requests as req
import base64
import pytest

def test_listuser_success_noargs():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/listuser"
    res = req.get(url)
    assert res.status_code == 200
    
    output = res.json().get("output", [])
    assert isinstance(output, list)
    
    if output:  # If there are users, check the structure
        user = output[0]
        assert "name" in user
        assert "email" in user
        assert "options" in user
        assert isinstance(user["options"], dict)

@pytest.mark.skipif(not os.environ.get("KUBECONFIG"), reason="KUBECONFIG not set")
def test_listuser_success():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/listuser"
    with open(os.environ.get("KUBECONFIG"), 'rb') as f:
        kubeconfig_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    res = req.get(url, json={"kubeconfig": kubeconfig_b64})
    res_json = res.json()
    assert isinstance(res_json.get("output"), list)
    
    # If there are users, check the structure
    if res_json.get("output"):
        user = res_json.get("output")[0]
        assert "name" in user
        assert "email" in user
        assert "options" in user
        assert isinstance(user["options"], dict)
        assert "redis" in user["options"]
        assert "postgres" in user["options"]
