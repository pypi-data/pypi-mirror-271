# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
setup(
    name='hebill_pypi',
    version='1.0.4',
    description='快速打包上传到项目到 pypi.org',
    long_description=open(r'D:\SDK\GitHub\python_hebill_pypi\hebill_pypi\README.MD', encoding='utf-8').read(),
    long_description_content_type='text/plain',
    packages=find_packages(),
    package_data={
        '': ['*.md', '*.MD'],
    },
    install_requires=[
        'twine==5.0.0',
        'wheel==0.43.0',
    ],
    python_requires='>=3.12',
)
