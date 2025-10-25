#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
#--web true
#--param kubeconfig "$KUBECONFIG"

from login import login

def main(args):
    if args.get("__ow_method", "POST").upper() != "POST":
        return {
            "statusCode": 405,
            "body": {"error": "Method not allowed"}
        }
    
    result = login(args)
    if "Error" in result.get("output", ""):
        return {
            "statusCode": 401,
            "body": result
        }
    return {
        "statusCode": 200,
        "body": result
    }
