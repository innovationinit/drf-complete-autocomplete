# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-complete-autocomplete',
    version='1.0.0',
    description='A package supplying tools for easy creating autocompletes with drf.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='IIIT',
    author_email='github@iiit.pl',
    packages=find_packages(exclude=[
        'testproject',
        'testproject.*',
    ]),
    include_package_data=True,
    install_requires=[
        'Django>=2.0,<2.3',
        'djangorestframework>=3.7.4',
        'six>=1.9.0',
    ],
    extras_require={
        'django-filter': ['django-filter'],
    },
    test_suite='testproject.runtests.run_tests',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
