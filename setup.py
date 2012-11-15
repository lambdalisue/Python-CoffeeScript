#!/usr/bin/env python
from setuptools import setup
import io


def readfile(filename, encoding='utf-8'):
    with io.open(filename, encoding=encoding) as fp:
        return fp.read()


def getversion():
    import coffeescript
    return coffeescript.__version__


setup(
    name='CoffeeScript',
    version=getversion(),
    author='OMOTO Kenji',
    description='A bridge to the JS CoffeeScript compiler',
    packages=['coffeescript'],
    package_dir={'coffeescript': 'coffeescript'},
    package_data={
        'coffeescript': ['coffee-script.js'],
    },
    long_description=readfile('README.rst'),
    url='https://github.com/doloopwhile/Python-CoffeeScript',
    author_email='doloopwhile@gmail.com',
    license="MIT License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.2',
        'Programming Language :: JavaScript',
    ],
    install_requires=("PyExecJS",),
    test_suite="test_coffeescript",
)
