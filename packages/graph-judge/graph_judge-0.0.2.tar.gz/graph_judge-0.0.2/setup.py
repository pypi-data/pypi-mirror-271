from setuptools import setup, find_packages

VERSION = "0.0.2"


def parse_requirements(requirement_file):
    with open(requirement_file) as fi:
        return fi.readlines()


with open('./README.rst') as f:
    long_description = f.read()


setup(
    name='graph_judge',
    packages=find_packages(),
    version=VERSION,
    description='TODO edit me',
    author='Spencer Hanson',
    long_description=long_description,
    url="https://github.com/spencer-hanson/GraphJudge",
    install_requires=parse_requirements('requirements.txt'),
    keywords=[],
    classifiers=[
        'Programming Language :: Python :: 3'
    ]
)

