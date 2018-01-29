from typing import List
import os
import os.path
from subprocess import call
from jinja2 import Template
import yaml
from generate import SOURCE_PATH, OUTPUT_PATH
from generate.base import BaseAPI

template_source = open('template/golang.html', 'r')
template: Template = Template(template_source.read())
template_source.close()


class GoPackage:
    path: str
    src: str

    def __init__(self, path: str, src: str):
        self.path = path
        self.src = src

    def generate(self):
        path = self.path[1:] if self.path.startswith('/') else self.path
        file = os.path.join(OUTPUT_PATH, path, 'index.html')
        dir_name = os.path.dirname(file)
        os.makedirs(dir_name, exist_ok=True)
        content = template.render(src=self.src, path=self.path)
        fp = open(file, 'w+')
        fp.write(content)
        fp.close()


class GoPackages(BaseAPI):
    items: List[GoPackage]

    @staticmethod
    def parse_from_file(path: str) -> BaseAPI:
        file = os.path.join(SOURCE_PATH, path)
        items: List[GoPackage] = []

        with open(file, 'r') as fp:
            content = yaml.load(fp.read())
            assert content['kind'] == 'GoPackages'
            assert content['apiVersion'] == 'v1alpha1'
            for item in content['items']:
                items.append(GoPackage(path=item['path'], src=item['source']))

        return GoPackages(items)
    
    def __init__(self, items: List[GoPackage]):
        super(GoPackages, self).__init__(kind='GoPackages', api_version='v1alpha1')
        self.items = items

    def generate(self):
        for item in self.items:
            item.generate()
