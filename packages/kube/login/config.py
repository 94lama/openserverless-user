import os
import base64

def get_kubeconfig():
    return base64.b64decode(os.environ.get("kubeconfig", "")).decode("utf-8")
