class XDict(dict):
    aliases: dict
    def __init__(self, **kwargs):
        super().__init__(**kwargs)