
class BaseFileException(Exception):
    def __init__(self, *args, **kwargs):
        self.msg = kwargs.get('message', '{}')
        self.file_name = kwargs.get('file_name', '')

    def __str__(self):
        return self.msg.format(self.file_name)

class FileNotFoundException(BaseFileException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.msg == '':
            self.msg = "File '{}' isn't found"

class IsNotFileException(BaseFileException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.msg == '':
            self.msg = "'{}' isn't file, may be a directory"