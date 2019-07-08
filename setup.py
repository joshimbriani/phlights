import setuptools
from setuptools import find_packages
from distutils.core import setup

setup(
    name='phlights',
    version='0.2.0',
    author='Josh Imbriani',
    author_email='josh@mailinator.com',
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    url='http://pypi.python.org/pypi/phlights/',
    license='LICENSE',
    description='Flight Search API Powered by Kiwi',
    long_description=open('README.md').read(),
    install_requires=[
        "astroid == 2.2.5",
        "certifi == 2019.6.16",
        "chardet == 3.0.4",
        "idna == 2.8",
        "isort == 4.3.21",
        "lazy-object-proxy == 1.4.1",
        "mccabe == 0.6.1",
        "pylint == 2.3.1",
        "pytz == 2019.1",
        "requests == 2.22.0",
        "six == 1.12.0",
        "typed-ast == 1.4.0",
        "tzlocal == 1.5.1",
        "urllib3 == 1.25.3",
        "wrapt == 1.11.2"
    ],
)
