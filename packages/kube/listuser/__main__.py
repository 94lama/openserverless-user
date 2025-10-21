#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
#--param web true
#--param KUBECONFIG $KUBECONFIG

from listuser import listuser

def main(args):
    if args.get("__ow_method", "GET").upper() != "GET":
        return {"statusCode": 405, "body": {"error": "Method not allowed"}}
    return {"body": listuser(args)}
