#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
#--web true
#--param kubeconfig "$KUBECONFIG"

from adduser import adduser

def main(args):
  if args.get("__ow_method", "POST").upper() != "POST":
        return {"statusCode": 405, "body": {"error": "Method not allowed"}}
  return { "body": adduser(args) }
