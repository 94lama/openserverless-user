#--kind python:default
#--web true
#--annotation index '99:Lovable:index:admin:/index.html'
import index
def main(args):
  return { "body": index.index(args) }
