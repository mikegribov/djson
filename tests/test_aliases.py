from xjson.src.xjson import XJson
import os


def test_alias_key():
    xj = XJson(os.path.join("examples", "countries", "single_file.xjson"))
    assert xj.structure.alias('russia_population') == xj.structure['russia_population']

def test_alias_path():
    xj = XJson(os.path.join("examples", "countries", "single_file.xjson"))
    assert xj.structure.alias('russia_population') == xj.structure.get_value('russia.population')