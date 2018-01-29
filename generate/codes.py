import re
from typing import List
import os.path
import yaml
from generate.base import BaseAPI
from generate import SOURCE_PATH
from generate.golang import GoPackages

cls = {
    'GoPackages': GoPackages,
}

regexp = re.compile(r"^\/")


class CodeListItem:
    api_version: str
    kind: str
    path: str

    def __init__(self, kind: str, api_version: str, path: str):
        self.kind = kind
        self.api_version = api_version
        self.path = path


class CodeList(BaseAPI):
    def __init__(self, items: List[CodeListItem]):
        super(CodeList, self).__init__('v1alpha1', 'CodeList')
        self.items = items

    @staticmethod
    def parse_from_file(path: str) -> BaseAPI:
        file = os.path.join(SOURCE_PATH, path)
        items: List[CodeListItem] = []
        with open(file, 'r') as fp:
            content = yaml.load(fp.read())
            assert content['kind'] == 'CodeList'
            assert content['apiVersion'] == 'v1alpha1'
            for item in content['items']:
                items.append(CodeListItem(kind=item['kind'], path=item['path'], api_version=item['apiVersion']))
        return CodeList(items)

    def generate(self):
        for item in self.items:
            path = item.path[1:] if item.path.startswith('/') else item.path
            filepath = os.path.join(SOURCE_PATH, path)
            if not os.path.isfile(filepath):
                print('File {0} is missing'.format(filepath))
                continue
            target_class = cls[item.kind]
            instance = target_class.parse_from_file(path)
            instance.generate()


cls['CodeList'] = CodeList
