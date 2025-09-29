import sys, os, json, time
from configure import get_api_client
from kubernetes import client
from kubernetes.client.rest import ApiException

"""
arguments:
1: namespace
2: pod configuration (path to YAML/JSON file or inline JSON string)
3: name (optional)
"""

def main(name, api_version="v1", labels=None) -> None:
    if not name:
        raise SystemExit("Usage: create-namespace.py <name> <api (optional)> <labels (optional)>")

    if labels is None:
        labels = {"purpose": "demo"}

    api_client = get_api_client()
    
    # If the namespace already exists, return it directly
    try:
        existing = api_client.read_namespace(name=name)
        return existing
    except ApiException as e:
        if e.status != 404:
            # Any non-404 error should bubble up
            raise

    # Check if the namespace exists before creating the pod
    try:
        # V1Namespace is the Python object that represents the Namespace resource.
        namespace_body = client.V1Namespace(
            api_version=api_version,
            kind="Namespace",
            metadata=client.V1ObjectMeta(
                name=name,
                labels=labels
            )
        )
        api_client.create_namespace(body=namespace_body)
    except ApiException as e:
        if e.status != 404:
            raise

    return api_client.read_namespace(name=name)


if __name__ == "__main__":
    api_version = sys.argv[2] if len(sys.argv) > 2 else "v1"
    labels_arg = sys.argv[3] if len(sys.argv) > 3 else None
    res = main(sys.argv[1], api_version, labels_arg)
    print(res)
