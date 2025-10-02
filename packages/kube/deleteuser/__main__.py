#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
#--web true
#--param kube_host "$KUBE_HOST"
#--param kubeconfig "$KUBECONFIG"
#--param groups "nuvolaris.org"
#--param namespace "nuvolaris"
#--param version "v1"
#--param plural "whisksusers"
#--param propagation_policy "Foreground"

import deleteuser
def main(args):
  return { "body": deleteuser.deleteuser(args) }
