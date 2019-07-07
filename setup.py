from distutils.core import setup

setup(
    name='Phlights',
    version='0.1.0',
    author='Josh Imbriani',
    author_email='josh@mailinator.com',
    packages=['phlights'],
    url='http://pypi.python.org/pypi/Phlights/',
    license='LICENSE',
    description='Useful towel-related stuff.',
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
        "urllib3 == 1.25.3",
        "wrapt == 1.11.2"
    ],
)
