#--kind python:default
#--web true
#--annotation index '99:Lovable:address:admin:/address.html'
import address
def main(args):
  return { "body": address.address(args) }
