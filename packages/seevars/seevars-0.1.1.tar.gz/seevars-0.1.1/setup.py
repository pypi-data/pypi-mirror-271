#!/usr/bin/env python
from setuptools import setup, find_packages

readme = open('./README.md', 'r')

setup(
    name='seevars',
    version='0.1.1',
    description='A tool to view the variables entered by the python prompt',
    long_description=readme.read(),
    long_description_content_type='text/markdown',
    author='nicriv',
    author_email='nicriv.dev@gmail.com',
    url='https://github.com/NicRiv/seevars',
    keywords=['utilities', 'prompt', 'monitor','vars'],
    license='MIT',
    packages=find_packages(),
    py_modules=['seevars'],
)
