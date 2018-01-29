class BaseAPI:
    api_version: str
    kind: str

    def __init__(self, kind: str, api_version: str):
        self.api_version = api_version
        self.kind = kind

    def generate(self):
        raise NotImplemented
