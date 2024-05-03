
class EnumException(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class ThriftGeneratedModuleException(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message

class FileNotFoundException(Exception):
    def __init__(self, m):
        self.message = m
    def __str__(self):
        return self.message
