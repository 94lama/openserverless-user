"""
Read the kubeconfig as args['kubeconfig] in base64
Access the kubernetes api and list all the namespaces.
Return `{"output": <array of namespaces>}`.
"""
import base64, tempfile, os, re, subprocess
from config import load_kube_config
from kubernetes import client, config

def verify_name(name): # returns error dict if name is not valid
    pattern = r"^[a-z0-9](?:[a-z0-9]{0,61}[a-z0-9])?$"
    if not name:
        return {"output": "Error: name parameter is required"}
    elif not re.fullmatch(pattern, name):
        return {"output": "Error: name parameter must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (max 61 characters)"}

def verify_email(email): # returns False if ok, error dict if email not valid
    if not email:
        return {"output": "Error: email parameter is required"}
    elif "@" not in email or "." not in email:
        return {"output": "Error: email parameter must be a valid email address"}

def verify_password(password): # returns False if ok, error dict if password not valid
    if not password:
        return {"output": "Error: password parameter is required"}
    elif len(password) < 5:
        return {"output": "Error: password parameter must be at least 8 characters long"}

def adduser(args):
    name = args.get('name', '')
    verify_name(name)
    email = args.get('email', '')
    verify_email(email)
    password = str(args.get('password', ''))
    verify_password(password)

    filepath = load_kube_config(args.get('kubeconfig', os.getenv('KUBECONFIG', '')))
    GROUP = args.get("groups", "nuvolaris.org")
    VERSION = args.get("version", "v1")
    PLURAL = args.get("plural", "whisksusers")
    NAMESPACE = args.get("namespace", "nuvolaris")

    # Load kubeconfig from the file and set up configuration
    config.load_kube_config(config_file=filepath["output"])
    configuration = client.Configuration.get_default_copy()
    #configuration.api_key = {"authorization": "Bearer <token>"}

    if (filepath.get("output", "").startswith("Error")):
        return filepath

    try:
        api_client = client.ApiClient(configuration)
        api_client_instance = client.CustomObjectsApi(api_client)

        resource_body = {
            "apiVersion": f"{GROUP}/{VERSION}",
            "kind": "WhiskUser",
            "metadata": {
                "name": name,
                "namespace": NAMESPACE
            },
            "spec": {
                "name": name,
                "email": email,
                "password": password,
                "namespace": NAMESPACE,
                "auth": args.get("auth", ""),
                "enableRedis": args.get('redis', 'false') == True,
                "enableMongo": args.get('mongodb', 'false') == True,
                "enablePostgres": args.get('postgres', 'false') == True,
                "enableMinio": args.get('minio', 'false') == True,
                "enableSeaweedFS": args.get('seaweedfs', 'false') == True,
                "enableMilvus": args.get('milvus', 'false') == True
            }
        }

        # Create the custom resource in Kubernetes
        res = api_client_instance.create_namespaced_custom_object(
            group=GROUP,
            version=VERSION,
            namespace=NAMESPACE,
            plural=PLURAL,
            body=resource_body
        )

        return {"output": f"User {name} has been successfully created!"}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}
