#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
#--web true
#--param kubeconfig "$KUBECONFIG"

from deleteuser import deleteuser

def main(args):
    if args.get("__ow_method", "DELETE").upper() != "DELETE":
        return {
            "statusCode": 405,
            "body": {"error": "Method not allowed"}
        }
    
    result = deleteuser(args)
    if "Error" in result.get("output", ""):
        return {
            "statusCode": 404,
            "body": result
        }
    return {
        "statusCode": 200,
        "body": result
    }
