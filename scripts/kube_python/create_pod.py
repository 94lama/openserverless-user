import sys, os, json, time
from get_pod import main as get_pod
from configure import get_api_client

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

def main(namespace, manifest_arg, name) -> None:
    if not namespace or not manifest_arg:
        raise SystemExit("Usage: create-pod.py <namespace> <manifest_path_or_inline_json> <name (optional)>")

    manifest = load_manifest(manifest_arg)
    if (name): data["metadata"]["name"] = name
    else: name = manifest["metadata"]["name"]

    try:
        get_pod(name, namespace)
        raise SystemExit("The pod already exists")
    except Exception as e:
        # Continue only if the error is a 404 (Not Found)
        if hasattr(e, 'status') and e.status == 404:
            pass  # the pod does not exist, continue
        else:
            raise
        
    if not isinstance(manifest, dict):
        raise SystemExit("Manifest must deserialize to a JSON object")
    if "metadata" not in manifest or "name" not in manifest["metadata"]:
        raise SystemExit("Manifest must include metadata.name")

    api = get_api_client()
    v1_list = api.list_pod_for_all_namespaces(watch=False)
    api.create_namespaced_pod(body=manifest, namespace=namespace)
    resp = get_pod(name, namespace)

    return resp


if __name__ == "__main__":
    if len(sys.argv) > 3: name = sys.argv[3]
    else: name = ""
    res = main(sys.argv[1], sys.argv[2], name)
    print(res)
