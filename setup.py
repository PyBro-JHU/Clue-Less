# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='Clue-Less',
    version='0.5',
    description='',
    author='PyBro-JHU',
    author_email='stevendgonzales@gmail.com',
    tests_require=[
        "mock",
        "nose",
        "nosexcover",
        "testtools",
        "tox"
    ],
    install_requires=[
        "kivy",
        "flask",
        "flask-restful",
        "pymongo",
        "requests"
    ],
    test_suite='nose.collector',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup']),
    package_dir={'help': 'clueless/help'},
    package_data={'help': ['clueless_help.htm']}
)
