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

def deleteuser(args):
    print(args)
    name = args.get('name', '')
    if not name:
        return {"output": "Error: name parameter is required"}

    filepath = load_kube_config(args.get('kubeconfig', os.getenv('KUBECONFIG', '')))
    GROUP = args.get("groups")
    VERSION = args.get("version")
    PLURAL = args.get("plural")
    NAMESPACE = args.get("namespace")
    """ PROPAGATION_POLICY can be 'Foreground', 'Background' or 'Orphan'
    Decides whether and how garbage collection will be performed. Either this field or OrphanDependents may be set, but not both. The default policy is decided by the existing finalizer set in the metadata.finalizers and the resource-specific default policy.
    - 'Foreground' - The object exists in the system until the garbage collector finishes deleting all the objects it owns. Once all owned objects are deleted, the object is deleted.
    - 'Background' - The object is deleted immediately. Once the garbage collector discovers the object is missing, it deletes all the objects it owns in the background.
    - 'Orphan' - The object is deleted immediately, but the garbage collector will not delete the objects it owns. Instead, the garbage collector will remove the owner references from the owned objects.
    - true - Equivalent to 'Foreground'
    - false - Equivalent to 'Background'
    """
    PROPAGATION_POLICY = args.get("propagation_policy") # default Foreground

    # Load kubeconfig from the file and set up configuration
    config.load_kube_config(config_file=filepath["output"])
    configuration = client.Configuration.get_default_copy()
    #configuration.api_key = {"authorization": "Bearer <token>"}

    if (filepath.get("output", "").startswith("Error")):
        return filepath

    try:
        api_client = client.ApiClient(configuration)
        api_client_instance = client.CustomObjectsApi(api_client)
        res = api_client_instance.delete_namespaced_custom_object(group=GROUP, version=VERSION, namespace=NAMESPACE, plural=PLURAL, name=name, grace_period_seconds=60, propagation_policy=PROPAGATION_POLICY, )

        return {"output": f"User {name} deleted successfully"}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}
