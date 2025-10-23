import os
import requests as req
import base64
import pytest

def test_adduser_missing_params():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/adduser"
    res = req.post(url, json={})
    assert res.status_code in [400, 405]  # Either is acceptable
    
def test_adduser_invalid_name():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/adduser"
    data = {
        "name": "invalid-user@name",
        "email": "test@test.com",
        "password": "test123"
    }
    res = req.post(url, json=data)
    assert res.status_code == 400
    assert res.json().get("error") is not None

def test_adduser_invalid_email():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/adduser"
    data = {
        "name": "validuser",
        "email": "invalid-email",
        "password": "test123"
    }
    res = req.post(url, json=data)
    assert res.status_code == 400
    assert res.json().get("error") is not None

def test_adduser_short_password():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/adduser"
    data = {
        "name": "validuser",
        "email": "test@test.com",
        "password": "abc"  # less than 5 chars
    }
    res = req.post(url, json=data)
    assert res.status_code == 400
    assert res.json().get("error") is not None

@pytest.mark.skipif(not os.environ.get("KUBECONFIG"), reason="KUBECONFIG not set")
def test_adduser_success():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/adduser"
    with open(os.environ.get("KUBECONFIG"), 'rb') as f:
        kubeconfig_b64 = base64.b64encode(f.read()).decode('utf-8')
    
    data = {
        "name": "testuser1",
        "email": "test@example.com",
        "password": "test123",
        "kubeconfig": kubeconfig_b64,
        "options": {
            "redis": True,
            "postgres": True
        }
    }
    res = req.post(url, json=data)
    assert res.status_code == 200
    assert "successfully created" in res.json().get("output", "")