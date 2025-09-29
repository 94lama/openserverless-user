import sys, os, json, time
from kubernetes.client.rest import ApiException
from configure import get_api_client

"""
arguments:
1: namespace
2: name
"""

def main(pod_name, namespace_name) -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: get-pod.py <namespace> <name>")

    api = get_api_client()
    pod = api.read_namespaced_pod(name=pod_name, namespace=namespace_name)
    try:
        resp = api.read_namespaced_pod(name=pod_name,namespace=namespace_name)
    except ApiException as e:
        if e.status != 404:
            print(f"Unknown error: {e}")
            exit(1)
    return pod


if __name__ == "__main__":
    if len(sys.argv) > 2: namespace = sys.argv[2] 
    else: namespace = "default"
    res = main(sys.argv[1], namespace)
    print(res)
