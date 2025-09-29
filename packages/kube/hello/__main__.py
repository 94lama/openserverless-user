#--docker "nuvolaris/aigency-runtimes:python_v3.12-2506091954.1060304ecbd5"
#--web true
#--param kubeconfig "$KUBECONFIG"
import hello
def main(args):
  return { "body": hello.hello(args) }
