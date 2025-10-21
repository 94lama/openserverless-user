"""
Read the kubeconfig as args['kubeconfig] in base64
Access the kubernetes api and list all the namespaces.
Return `{"output": <array of namespaces>}`.
"""
import base64
import tempfile
import os
from config import load_kube_config
from kubernetes import client, config

""" List all users in the kubernetes cluster based on the custom resource WhisksUsers.
it reads the kubeconfig from args['KUBECONFIG'] in base64.
Returns {"output": <array of usernames>} or {"output": "Error: <error message>"}
"""
def listuser(args):
    # reads the KUBECONFIG value from env variable. If not found, defaults to empty string.
    # use the commands in the README to set the KUBECONFIG env variable.
    kube_b64 = os.getenv('KUBECONFIG', '')
    kubeconfig = load_kube_config(kube_b64)
    GROUP = args.get("groups", "nuvolaris.org")
    VERSION = args.get("version", "v1")
    PLURAL = args.get("plural", "whisksusers")
    NAMESPACE = args.get("namespace", "nuvolaris")

    if kubeconfig.get("output", "").startswith("Error"):
        return kubeconfig

    kubeconfig_path = kubeconfig.get("output")

    try:
        # Load kubeconfig into the kubernetes client configuration so the API client
        # uses the correct host, certs and credentials from the provided kubeconfig.
        config.load_kube_config(config_file=kubeconfig_path)

        api_client = client.ApiClient()
        api_client_instance = client.CustomObjectsApi(api_client)
        users = api_client_instance.list_namespaced_custom_object(
            group=GROUP,
            version=VERSION,
            namespace=NAMESPACE,
            plural=PLURAL
        )
        users_list = [user.get('metadata', {}).get('name') for user in users.get('items', [])]

        return {"output": users_list}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}
