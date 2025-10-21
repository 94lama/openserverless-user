import sys 
sys.path.append("packages/kube/hello")
import packages.kube.hello

def test_hello():
    res = hello.hello({})
    assert res["output"] == "hello"
