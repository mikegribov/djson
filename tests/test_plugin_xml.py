import os
from ..xjson import XJson


def test_json_eq_xml():
    json = XJson(os.path.join("examples", "countries", "single_file.xml"))
    xml_file  = XJson(os.path.join("examples","countries", "single_file.xml"))
    assert json.structure == xml_file.structure