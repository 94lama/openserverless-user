"""
Read the kubeconfig as args['kubeconfig] in base64
Access the kubernetes api and list all the namespaces.
Return `{"output": <array of namespaces>}`.
"""
import base64
import tempfile
import os
from kubernetes import client, config

def hello(args):
    try:
        kubeconfig_b64 = args.get('kubeconfig')
        if not kubeconfig_b64:
            return {"output": "Error: kubeconfig parameter is required"}

        kubeconfig_content = base64.b64decode(kubeconfig_b64).decode('utf-8')

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as temp_file:
            temp_file.write(kubeconfig_content)
            temp_kubeconfig_path = temp_file.name

        try:
            config.load_kube_config(config_file=temp_kubeconfig_path)

            v1 = client.CoreV1Api()
            namespaces = v1.list_namespace()

            namespace_names = [namespace.metadata.name for namespace in namespaces.items]

            return {"output": namespace_names}

        finally:
            os.unlink(temp_kubeconfig_path)

    except Exception as e:
        return {"output": f"Error: {str(e)}"}
