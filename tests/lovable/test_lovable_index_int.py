import os, requests as req

def test_lovable_index_int():
    url = f"{os.environ.get("OPSDEV_HOST", "")}/api/my/lovable/index"
    res = req.get(url).json()
    assert res.get("output") == "index"
