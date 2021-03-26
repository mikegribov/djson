from xjson.src.xjson import XJson
import os

def test_json_eq_xjson():
    json = XJson(os.path.join("examples", "single_file.json"))
    xjson  = XJson(os.path.join("examples", "single_file.yaml"))
    assert json.structure == xjson.structure