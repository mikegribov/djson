from ..xjson import XJson
import os

def test_json_eq_xjson():
    json = XJson(os.path.join("examples", "countries", "single_file.json"))
    content = {name: {"title":json.structure[name]["title"], "city": json.structure[name]["city"], "continent": json.structure[name]["continent"]} for name in json.structure}
    csv_file  = XJson(os.path.join("examples", "countries", "single_file.csv"))
    assert content == csv_file.structure