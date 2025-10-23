import os
from unittest.mock import patch, Mock
import requests
import pytest
import packages.kube.listuser as listuser

@pytest.fixture
def mock_k8s_response():
    return {
        'items': [
            {
                'metadata': {'name': 'user1'},
                'spec': {
                    'email': 'user1@test.com',
                    'redis': True,
                    'mongo': False,
                    'postgres': True,
                    'minio': False,
                    'seaweedFS': True,
                    'milvus': False
                }
            }
        ]
    }

@patch('kubernetes.client.CustomObjectsApi')
def test_listuser(mock_api, mock_k8s_response):
    # Setup mock
    mock_instance = Mock()
    mock_instance.list_cluster_custom_object.return_value = mock_k8s_response
    mock_api.return_value = mock_instance
    
    # Test
    args = {
        "KUBERNETES_SERVICE_HOST": "localhost",
        "KUBERNETES_SERVICE_PORT": "8443",
        "KUBERNETES_API_TOKEN": "test-token"
    }
    
    result = listuser.listuser(args)
    
    assert "users" in result
    assert len(result["users"]) == 1
    assert result["users"][0]["name"] == "user1"
    assert result["users"][0]["email"] == "user1@test.com"
    assert result["users"][0]["spec"]["redis"] == True

def test_listuser_integration():
    host = os.getenv("OPSDEV_HOST")
    if not host:
        pytest.skip("OPSDEV_HOST not set")
        
    response = requests.get(f"{host}/api/my/kube/listuser")
    
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    
    # Validate user object structure
    if len(data["users"]) > 0:
        user = data["users"][0]
        assert "name" in user
        assert "email" in user
        assert "spec" in user
        assert all(k in user["spec"] for k in ["redis", "mongodb", "postgres", "minio", "seaweedFS", "milvus"])
