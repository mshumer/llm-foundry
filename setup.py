"""MosaicML LLM Foundry package setup."""

import os
import re

import setuptools
from setuptools import setup

_PACKAGE_NAME = 'llm-foundry'
_PACKAGE_DIR = 'llmfoundry'
_REPO_REAL_PATH = os.path.dirname(os.path.realpath(__file__))
_PACKAGE_REAL_PATH = os.path.join(_REPO_REAL_PATH, _PACKAGE_DIR)

# Read the repo version
# We can't use `.__version__` from the library since it's not installed yet
with open(os.path.join(_PACKAGE_REAL_PATH, '__init__.py')) as f:
    content = f.read()
# regex: '__version__', whitespace?, '=', whitespace, quote, version, quote
# we put parens around the version so that it becomes elem 1 of the match
expr = re.compile(r"""^__version__\W+=\W+['"]([0-9\.]*)['"]""", re.MULTILINE)
repo_version = expr.findall(content)[0]

# Use repo README for PyPi description
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Hide the content between <!-- SETUPTOOLS_LONG_DESCRIPTION_HIDE_BEGIN --> and
# <!-- SETUPTOOLS_LONG_DESCRIPTION_HIDE_END --> tags in the README
while True:
    start_tag = '<!-- SETUPTOOLS_LONG_DESCRIPTION_HIDE_BEGIN -->'
    end_tag = '<!-- SETUPTOOLS_LONG_DESCRIPTION_HIDE_END -->'
    start = long_description.find(start_tag)
    end = long_description.find(end_tag)
    if start == -1:
        assert end == -1, 'there should be a balanced number of start and ends'
        break
    else:
        assert end != -1, 'there should be a balanced number of start and ends'
        long_description = long_description[:start] + long_description[
            end + len(end_tag):]

classifiers = [
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
]

install_requires = [
    'mosaicml[nlp,streaming,wandb]>=0.14.1,<0.15',
    'torch==1.13.1',
    'datasets==2.10.1',
    'sentencepiece==0.1.97',
    'einops==0.5.0',
    'omegaconf>=2.2.3,<3',
    'pynvml<12',
    'slack-sdk<4',
    'mosaicml-cli>=0.3,<1',
    'onnx==1.13.1',
    'onnxruntime==1.14.1',
]

extra_deps = {}

extra_deps['dev'] = [
    'pre-commit>=2.18.1,<3',
    'pytest>=7.2.1,<8',
    'pytest_codeblocks>=0.16.1,<0.17',
    'pytest-cov>=4,<5',
    'pyright==1.1.296',
    'toml>=0.10.2,<0.11',
    'packaging>=21,<23',
]

extra_deps['gpu'] = [
    'flash-attn==v1.0.3.post0',
    'triton==2.0.0.dev20221202',
    # PyPI does not support direct dependencies, so we remove this line before uploading from PyPI
    'xentropy-cuda-lib@git+https://github.com/HazyResearch/flash-attention.git@v0.2.8#subdirectory=csrc/xentropy',
]

extra_deps['all'] = set(dep for deps in extra_deps.values() for dep in deps)

setup(
    name=_PACKAGE_NAME,
    version=repo_version,
    author='MosaicML',
    author_email='team@mosaicml.com',
    description='LLM Foundry',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mosaicml/llm-foundry/',
    package_data={
        'llmfoundry': ['py.typed'],
    },
    packages=setuptools.find_packages(
        exclude=['.github*', 'mcli*', 'scripts*', 'tests*']),
    classifiers=classifiers,
    install_requires=install_requires,
    extras_require=extra_deps,
    python_requires='>=3.7',
)
