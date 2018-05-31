# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import io
import os


about = {}
about_filename = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'themis', 'finals', '__about__.py')
with io.open(about_filename, 'rb') as fp:
    exec(fp.read(), about)


setup(
    name='themis.finals',
    version=about['__version__'],
    description='Themis Finals CLI & public API library',
    author='Alexander Pyatkin',
    author_email='aspyatkin@gmail.com',
    url='https://github.com/themis-project/themis-finals-py',
    license='MIT',
    packages=find_packages('.'),
    install_requires=[
        'setuptools>=35.0.0',
        'requests>=2.18.4',
        'grequests==0.3.0',
        'click>=6.7',
        'python-dateutil>=2.6.0'
    ],
    extras_require={
        ':python_version<"3.4"': [
            'enum34>=1.1.6'
        ]
    },
    namespace_packages=[
        'themis'
    ],
    entry_points={
        'console_scripts': [
            'themis-finals = themis.finals:cli',
        ]
    }
)
