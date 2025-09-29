import os, requests as req
def test_hello():
    url = os.environ.get("OPSDEV_HOST") + "/api/my/kube/hello"
    res = req.get(url).json()
    assert res.get("output") == "hello"
