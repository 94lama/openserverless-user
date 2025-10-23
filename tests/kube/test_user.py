import pytest
import os
from packages.kube.adduser.adduser import adduser
from packages.kube.listuser.listuser import listuser
from packages.kube.deleteuser.deleteuser import deleteuser

@pytest.fixture
def mock_kubeconfig():
    return "dGVzdC1rdWJlLWNvbmZpZwo="  # Base64 encoded test config

@pytest.fixture
def valid_user_args(mock_kubeconfig):
    return {
        "name": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "kubeconfig": mock_kubeconfig
    }

def test_adduser_validates_input(valid_user_args):
    # Test with invalid name
    invalid_args = valid_user_args.copy()
    invalid_args["name"] = ""
    result = adduser(invalid_args)
    assert "Error" in result["output"]

    # Test with invalid email
    invalid_args = valid_user_args.copy()
    invalid_args["email"] = "invalid-email"
    result = adduser(invalid_args)
    assert "Error" in result["output"]

    # Test with invalid password
    invalid_args = valid_user_args.copy()
    invalid_args["password"] = ""
    result = adduser(invalid_args)
    assert "Error" in result["output"]

def test_listuser_requires_kubeconfig(mock_kubeconfig):
    result = listuser({})
    assert "Error: kubeconfig parameter is required" in result["output"]

def test_deleteuser_requires_name():
    result = deleteuser({})
    assert "Error: name parameter is required" in result["output"]

def test_deleteuser_requires_kubeconfig():
    result = deleteuser({"name": "testuser"})
    assert "Error: kubeconfig parameter is required" in result["output"]