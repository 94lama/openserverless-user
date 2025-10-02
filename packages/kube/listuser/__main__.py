#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
#--web true
#--param kube_host "$KUBE_HOST"
#--param kubeconfig "$KUBECONFIG"

import listuser
def main(args):
  return { "body": listuser.listuser(args) }
