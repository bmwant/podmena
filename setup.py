"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    # https://packaging.python.org/specifications/core-metadata/#name
    name='podmena',

    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.4.2',
    description='Enhance your git commit messages with emoji',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bmwant/podmena',
    author='Misha Behersky',
    author_email='bmwant@gmail.com',

    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Version Control :: Git',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Unix Shell',
    ],

    keywords='git hook fun emoji commit',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=[
        'click>=6.7',  # hi, mitshuhiko
    ],

    package_data={
        'podmena': [
            'resources/commit-msg',
            'resources/emoji-db',
        ],
    },

    data_files=[
        ('', ['podmena/resources/emoji-db']),
    ],

    entry_points={
        'console_scripts': [
            'podmena=podmena.cli:cli',
        ],
    },

    project_urls={
        'Blog post': 'https://bmwlog.pp.ua/',
        'Say Thanks!': 'https://gimmebackmyson.herokuapp.com/',
    },
)
