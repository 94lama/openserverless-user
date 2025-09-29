import sys, os, json, time
from configure import get_api_client

"""
arguments:
1: namespace
2: name
"""

def main(pod_name, namespace_name) -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: get-pod.py <name> <namespace>")

    api = get_api_client()
    return api.read_namespaced_pod(name=pod_name,namespace=namespace_name)
    

if __name__ == "__main__":
    if len(sys.argv) > 2: namespace = sys.argv[2] 
    else: namespace = "default"
    res = main(sys.argv[1], namespace)
    print(res)
