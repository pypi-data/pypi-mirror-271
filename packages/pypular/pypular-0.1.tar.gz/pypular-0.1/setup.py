#!/usr/bin/python3
# This file is auto generated. Do not modify
from setuptools import setup
setup(
    name='pypular',
    version='0.1',
    description='Increase the popularity of your PYPI package by downloading it many times.',
    readme='README.md',
    url='https://codeberg.org/ltworf/pypular/',
    author="Salvo 'LtWorf' Tomaselli",
    author_email='tiposchi@tiscali.it',
    license='AGPL3',
    classifiers=['Development Status :: 2 - Pre-Alpha', 'Environment :: Console', 'License :: OSI Approved :: GNU Affero General Public License v3', 'Programming Language :: Python :: 3.11', 'Programming Language :: Python :: 3.12'],
    keywords='pypi counter popularity',
    packages=['pypular'],
    entry_points={
        'console_scripts': [
            'pypular = pypular.__main__:main',
        ]
    },
    install_requires=[
    ],
)
