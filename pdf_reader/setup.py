import json
from setuptools import setup, find_packages

with open('install.json', 'r') as fh:
    version = json.load(fh)['programVersion']

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    author='Floyd Hightower',
    description='Playbook app to read a PDF.',
    license='MIT license',
    name='pdf_reader',
    packages=find_packages(),
    version=version
)
