#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
#--web true
#--param kubeconfig "$KUBECONFIG"

from deleteuser import deleteuser
def main(args):
  if args.get("__ow_method", "DELETE").upper() != "DELETE":
        return {"statusCode": 405, "body": {"error": "Method not allowed"}}
  return { "body": deleteuser(args) }
