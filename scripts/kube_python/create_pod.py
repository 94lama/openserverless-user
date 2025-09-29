import sys, os, json, time
from get_pod import main as get_pod
from configure import get_api_client
from kubernetes.client.rest import ApiException

"""
arguments:
1: namespace
2: pod configuration (path to YAML/JSON file or inline JSON string)
3: name (optional)
"""

def load_manifest(manifest_arg: str) -> dict:
    """Load a Kubernetes Pod manifest from a file path (JSON) or inline JSON string."""
    if os.path.isfile(manifest_arg):
        _, ext = os.path.splitext(manifest_arg)
        with open(manifest_arg, "r", encoding="utf-8") as f:
            data = f.read()
            data = json.loads(data)
    else:
        # Treat as inline JSON
        data = json.loads(manifest_arg)
    return data

def main(namespace, manifest_arg, name="") -> None:
    if not namespace or not manifest_arg:
        raise SystemExit("Usage: create-pod.py <namespace> <manifest_path_or_inline_json> <name (optional)>")

    manifest = load_manifest(manifest_arg)
    if not isinstance(manifest, dict):
        raise SystemExit("Manifest must deserialize to a JSON object")
    if "metadata" not in manifest or "name" not in manifest["metadata"]:
        raise SystemExit("Manifest must include metadata.name")

    api = get_api_client()

    # Check if the namespace exists before creating the pod
    try:
        api.read_namespace(namespace)
    except ApiException as e:
        raise
    # Optional override for metadata.name via the function argument
    if name:
        manifest["metadata"]["name"] = name
    else:
        name = manifest["metadata"]["name"]
    # If the pod already exists, return it directly
    try:
        existing = get_pod(name, namespace)
        return existing
    except ApiException as e:
        if e.status != 404:
            # Any non-404 error should bubble up
            raise

    try:
        api.create_namespaced_pod(body=manifest, namespace=namespace)
    except ApiException as e:
        if e.status == 409:
            print(f"The pod {name}")
            return get_pod(name, namespace)
        else:
            raise

    return get_pod(name, namespace)


if __name__ == "__main__":
    if len(sys.argv) > 3: name = sys.argv[3]
    else: name = ""
    res = main(sys.argv[1], sys.argv[2], name)
    print(res)
