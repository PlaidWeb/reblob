"""Setup for reblob packaging"""

# Always prefer setuptools over distutils
from setuptools import setup
from distutils.util import convert_path
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

main_ns = {}
ver_path = convert_path('reblob/__version__.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='reblob',

    version=main_ns['__version__'],

    description='A tool for formatting a response to a page',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/PlaidWeb/reblob',

    author='fluffy',
    author_email='fluffy@beesbuzz.biz',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        'License :: OSI Approved :: MIT License',

        'Natural Language :: English',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],

    keywords='publishing blog webmention publ indieweb',

    packages=['reblob'],

    install_requires=[
        'beautifulsoup4',
        'pypandoc',
        'requests',
        'mf2py'
    ],

    extras_require={
        'dev': ['pylint', 'twine', 'flake8'],
    },

    project_urls={
        'Bug Reports': 'https://github.com/PlaidWeb/reblob/issues',
        'Source': 'https://github.com/PlaidWeb/reblob/',
        'Discord': 'https://beesbuzz.biz/discord',
        'Funding': 'https://liberapay.com/fluffy',
    },

    entry_points={
        'console_scripts': [
            'reblob = reblob.__main__:main'
        ]
    },

    python_requires=">=3.4",
)
