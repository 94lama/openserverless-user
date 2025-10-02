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

def listuser(args):
    filepath = load_kube_config(args.get('kubeconfig', os.getenv('KUBECONFIG', '')))
    GROUP = args.get("groups", "nuvolaris.org")
    VERSION = args.get("version", "v1")
    PLURAL = args.get("plural", "whisksusers")
    NAMESPACE = args.get("namespace", "nuvolaris")

    # Load kubeconfig from the file and set up configuration
    config.load_kube_config(config_file=filepath["output"])
    configuration = client.Configuration.get_default_copy()
    configuration.api_key = {"authorization": "Bearer <token>"}

    if (filepath.get("output", "").startswith("Error")):
        return filepath

    try:
        api_client = client.ApiClient(configuration)
        api_client_instance = client.CustomObjectsApi(api_client)
        users = api_client_instance.list_namespaced_custom_object(
            group=GROUP,
            version=VERSION,
            namespace=NAMESPACE,
            plural=PLURAL
        )
        listuser = [user['metadata']['name'] for user in users['items']]

        return {"output": listuser}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}
