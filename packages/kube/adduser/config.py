"""
Read the kubeconfig as args['kubeconfig'] in base64
Access the kubernetes api and list all the namespaces.
Return `{"output": <array of namespaces>}`.
"""
import base64
import tempfile
import os
from kubernetes import client, config

def load_kube_config(kubeconfig_b64):
    try:
        if not kubeconfig_b64:
            return {"output": "Error: kubeconfig parameter is required"}

        kubeconfig_content = base64.b64decode(kubeconfig_b64).decode('utf-8')

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(kubeconfig_content)
            temp_kubeconfig_path = temp_file.name

            return {"output": temp_kubeconfig_path}

    except Exception as e:
        return {"output": f"Error: {str(e)}"}

def delete_kube_config(temp_kubeconfig_path):
    if os.path.exists(temp_kubeconfig_path):
        os.unlink(temp_kubeconfig_path)