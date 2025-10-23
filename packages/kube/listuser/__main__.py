#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
#--web true
#--param kubeconfig "$KUBECONFIG"

from listuser import listuser

def main(args):
    if args.get("__ow_method", "GET").upper() != "GET":
        return {
            "statusCode": 405,
            "body": {"error": "Method not allowed"}
        }
    
    result = listuser(args)
    if "Error" in result.get("output", ""):
        return {
            "statusCode": 400,
            "body": result
        }
    return {
        "statusCode": 200,
        "body": result
    }
