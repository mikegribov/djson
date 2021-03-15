from typing import Union

class BasePlugin:

    def __init__(self, full_name: str, **kwargs) -> None:
        self.full_name = full_name
        self._init(**kwargs)

    def _init(self, **kwargs):
        ''' for inheritor initializations by kwargs'''
        pass

    def check(self) -> bool:
        return False

    def get(self) -> Union[bool, str, int, float, list, dict]:
        pass

