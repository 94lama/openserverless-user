import base64, tempfile, json
from config import load_kube_config
from kubernetes import client, config

""" Prepares a user object from the custom resource definition to be sent as output.
@param user = {
    "name": <username>,
    "email": <user email>,
    "options": {
        "minio": <true|false>,
        "postgres": <true|false>,
        "redis": <true|false>,
        "mongodb": <true|false>,
        "milvus": <true|false>
    }
}
"""
def build_user_object(user):
    name = user.get('metadata', {}).get('name')
    email = user.get('spec', {}).get('email', '')
    minio = user.get('spec', {}).get('minio', False)
    postgres = user.get('spec', {}).get('postgres', {}).get('enabled', False)
    redis = user.get('spec', {}).get('redis', {}).get('enabled', False)
    mongodb = user.get('spec', {}).get('mongodb', {}).get('enabled', False)
    milvus = user.get('spec', {}).get('milvus', {}).get('enabled', False)

    return {
        "name": name,
        "email": email,
        "options": {
            "minio": minio,
            "postgres": postgres,
            "redis": redis,
            "mongodb": mongodb,
            "milvus": milvus,
        }
    }

""" List all users in the kubernetes cluster based on the custom resource WhisksUsers.
    it reads the kubeconfig from args['KUBECONFIG'] in base64.
    Returns {"output": <array of usernames>} or {"output": "Error: <error message>"}
"""
def listuser(args):
    # reads the KUBECONFIG value from env variable. If not found, defaults to empty string.
    # use the commands in the README to set the KUBECONFIG env variable.
    kube_b64 = args.get('KUBECONFIG', "")
    if not kube_b64:
        return {"output": "Error: kubeconfig parameter is required"}
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

        users_list = [build_user_object(user) for user in users.get('items', [])]

        return {"output": users_list}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}
