import os
from ..xjson import XJson


def test_json_eq_xjson():
    json = XJson(os.path.join("examples", "countries", "single_file.json"))
    yaml_file  = XJson(os.path.join("examples","countries", "single_file.yaml"))
    assert json.structure == yaml_file.structure