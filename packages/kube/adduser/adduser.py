"""
Read the kubeconfig as args['kubeconfig] in base64
Access the kubernetes api and list all the namespaces.
Return `{"output": <array of namespaces>}`.
"""
import base64, tempfile, os, re, subprocess
from config import load_kube_config
from kubernetes import client, config
import secrets, string

def verify_name(name): # returns error dict if name is not valid
    #pattern = r"^[a-z0-9](?:[a-z0-9]{0,61}[a-z0-9])?$"
    pattern = r"^[a-z][a-z0-9]{4,61}$"
    if not name:
        raise ValueError("Error: name parameter is required")
    elif not re.fullmatch(pattern, name):
        raise ValueError("Error: name parameter must consist of lower case alphanumeric characters or '-', and must start and end with an alphanumeric character (max 61 characters)")
    else:
        return name

def verify_email(email):
    if not email:
        raise ValueError("Error: email parameter is required")
    elif "@" not in email or "." not in email:
        raise ValueError("Error: email parameter must be a valid email address")
    else:
        return email

def verify_password(password):
    if not password:
        raise ValueError("Error: password parameter is required")
    elif len(password) < 5:
        raise ValueError("Error: password parameter must be at least 5 characters long")
    else:
        return password

"""
Generate an auth token matching the structure:
<name>:<64-char-random-string>
where name is a short lowercase alphanumeric string starting with a letter.
"""
def generate_auth_secret(name, password):
    # name-like part (starts with a lowercase letter)
    user_len = 8
    first = secrets.choice(string.ascii_lowercase)
    rest = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(user_len - 1))
    user = first + rest

    # secret part: 64 characters, alphanumeric
    secret = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(64))

    return f"{user}:{secret}"

"""Generate secrets for services, following the structure:
    "${NAME}_SECRET_OPENWHISK"="$(random --uuid):$(random --str 64)"
    "${NAME}_SECRET_COUCHDB"="$(random --str 12)"
    "${NAME}_SECRET_REDIS"="$(random --str 12)"
    "${NAME}_SECRET_MONGODB"="$(random --str 12)"
    "${NAME}_SECRET_MINIO"="$(random --str 40)"
    "${NAME}_SECRET_POSTGRES"="$(random --str 12)"
    "${NAME}_SECRET_MILVUS"="$(random --str 12)"
"""
def generate_secrets(name):
    secrets_dict = {}
    services = {
        "openwhisk": 64,
        "couchdb": 12,
        "redis": 12,
        "mongodb": 12,
        "minio": 40,
        "postgres": 12,
        "milvus": 12,
        "seaweed": 12,
    }

    for service, length in services.items():
        secret_value = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
        secret = f"{secrets.token_hex(16)}:{secret_value}" if service == "openwhisk" else secret_value
        secrets_dict[f"{name}_SECRET_{service}".upper()] = secret
        os.environ[f"{name}_SECRET_{service}".upper()] = secret

    return secrets_dict

def adduser(args):
    name = verify_name(args.get('name', ''))
    password = verify_password(args.get('password', ''))
    email = verify_email(args.get('email', ''))
    auth_secret = generate_auth_secret(name, password)

    filepath = load_kube_config(args.get('kubeconfig', os.getenv('KUBECONFIG', '')))
    if (filepath.get("output", "").startswith("Error")):
        return filepath

    GROUP = args.get("groups", "nuvolaris.org")
    VERSION = args.get("version", "v1")
    PLURAL = args.get("plural", "whisksusers")
    NAMESPACE = args.get("namespace", "nuvolaris")

    # Load kubeconfig from the file and set up configuration
    config.load_kube_config(config_file=filepath["output"])
    configuration = client.Configuration.get_default_copy()

    try:
        api_client = client.ApiClient(configuration)
        api_client_instance = client.CustomObjectsApi(api_client)
        service_secrets = generate_secrets(name)

        # Create the WhiskUser resource with proper structure
        resource_body = {
            "apiVersion": f"{GROUP}/{VERSION}",
            "kind": "WhiskUser",
            "metadata": {
                "name": name,
                "namespace": NAMESPACE
            },
            "spec": {
                "email": email,
                "password": password,
                "namespace": name,  # Use user's name as their namespace
                "auth": auth_secret,  # Use generated auth_secret instead of empty string
                "redis": {"enabled": False},
                "mongodb": {"enabled": False},
                "postgres": {"enabled": False},
                "milvus": {"enabled": False},
                "seaweed": {"enabled": False},
                "object-storage": {
                    "password": service_secrets.get(f"{name.upper()}_SECRET_MINIO", ""),
                    "quota": f"{args.get('minio_storage_quota', 'auto')}",
                    "data": {
                        "enabled": args.get("minio_data", False),
                        "bucket": f"{name}-data",
                    },
                    "route": {
                        "enabled": args.get("minio_static", False),
                        "bucket": f"{name}-web",
                    },
                },
            },
        }
        # Enable services based on args
        if args["options"].get("redis", False):
            resource_body["spec"]["redis"] = {
                "enabled": True,
                "prefix": name,
                "password": service_secrets.get(f"{name.upper()}_SECRET_REDIS", ""),
            }
        for item in ["mongodb", "postgres", "milvus", "seaweed"]:
            if args["options"].get(item, False):
                resource_body["spec"][item] = {
                    "enabled": True,
                    "database": name,
                    "password": service_secrets.get(f"{name}_SECRET_{item}".upper(), ""),
                }

        print(args)
        print(resource_body)
        # Create the custom resource in Kubernetes
        api_client_instance.create_namespaced_custom_object(
            group=GROUP,
            version=VERSION,
            namespace=NAMESPACE,
            plural=PLURAL,
            body=resource_body
        )

        return {"output": f"User {name} has been successfully created!"}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}
