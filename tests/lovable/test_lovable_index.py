import lovable.index.index as m

def test_lovable_index():
    args = {}
    res = m.index(args)
    assert res["output"] == "index"
