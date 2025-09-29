import sys 
sys.path.append("packages/kube/hello")
import hello

def test_hello():
    res = hello.hello({})
    assert res["output"] == "hello"
