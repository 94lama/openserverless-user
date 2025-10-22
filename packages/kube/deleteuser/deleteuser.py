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

def cleanup_whisk_resources(api_client_instance, namespace, name):
  """Clean up associated Whisk resources before user deletion"""
  try:
    # List all whisk resources associated with the user
    whisk_resources = api_client_instance.list_namespaced_custom_object(
      group="nuvolaris.org",
      version="v1",
      namespace=namespace,
      plural="whisksusers",
      label_selector=f"user={name}"
    )

    # Delete each whisk resource with Foreground deletion
    for resource in whisk_resources.get('items', []):
      resource_name = resource['metadata']['name']
      api_client_instance.delete_namespaced_custom_object(
        group="nuvolaris.org",
        version="v1",
        namespace=namespace,
        plural="wskus",
        name=resource_name,
        body=client.V1DeleteOptions(propagation_policy='Foreground')
      )
  except Exception as e:
    print(f"Warning: Error cleaning up Whisk resources: {str(e)}")

def deleteuser(args):
  name = args.get('name', '')
  if not name:
    return {"output": "Error: name parameter is required"}

  # reads the KUBECONFIG value from env variable. If not found, defaults to empty string.
  # use the commands in the README to set the KUBECONFIG env variable.
  kube_b64 = args.get('kubeconfig', "")
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
    config.load_kube_config(config_file=kubeconfig_path)
    api_client = client.ApiClient()
    api_client_instance = client.CustomObjectsApi(api_client)

    # First cleanup associated Whisk resources
    cleanup_whisk_resources(api_client_instance, NAMESPACE, name)

    # Then delete the user with Foreground propagation
    delete_options = client.V1DeleteOptions(
      propagation_policy='Foreground'  # Changed to ensure proper cleanup order
    )

    res = api_client_instance.delete_namespaced_custom_object(
      group=GROUP, 
      version=VERSION, 
      namespace=NAMESPACE, 
      plural=PLURAL, 
      name=name,
      body=delete_options
    )
    return {"output": f"User {name} deleted successfully"}
  except Exception as e:
    return {"output": f"Error: {str(e)}"}
  finally:
    # Clean up the temporary kubeconfig file
    if os.path.exists(kubeconfig_path):
      os.remove(kubeconfig_path)
