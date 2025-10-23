import os
import requests as req
import base64
import pytest

def test_deleteuser_missing_name():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/deleteuser"
    res = req.delete(url)
    assert res.status_code == 404
    assert "Error" in res.json().get("output", "")

def test_deleteuser_missing_kubeconfig():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/deleteuser"
    data = {"name": "testuser"}
    res = req.delete(url, json=data)
    assert res.status_code == 404
    assert "Error" in res.json().get("output", "")

@pytest.mark.skipif(not os.environ.get("KUBECONFIG"), reason="KUBECONFIG not set")
def test_deleteuser_nonexistent():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/deleteuser"
    with open(os.environ.get("KUBECONFIG"), 'rb') as f:
        kubeconfig_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    data = {
        "name": "nonexistentuser123",
        "kubeconfig": kubeconfig_b64
    }
    res = req.delete(url, json=data)
    assert res.status_code == 404
    assert "Error" in res.json().get("output", "")

@pytest.mark.skipif(not os.environ.get("KUBECONFIG"), reason="KUBECONFIG not set")
def test_deleteuser_success():
    # First create a test user
    add_url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/adduser"
    with open(os.environ.get("KUBECONFIG"), 'rb') as f:
        kubeconfig_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    user_data = {
        "name": "deletetest",
        "email": "delete@test.com",
        "password": "test123",
        "kubeconfig": kubeconfig_b64
    }
    res = req.post(add_url, json=user_data)
    assert res.status_code == 200
    assert "successfully created" in res.json().get("output", "")

    # Then delete the user
    delete_url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/deleteuser"
    data = {
        "name": "deletetest",
        "kubeconfig": kubeconfig_b64
    }
    res = req.delete(delete_url, json=data)
    assert res.status_code == 200
    assert "deleted successfully" in res.json().get("output", "")