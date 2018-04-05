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
    version='0.1.0',
    description='Enhance your git commit messages with emoji',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bmwant/podmena',
    author='Misha Behersky',
    author_email='bmwant@gmail.com',

    # For a list of valid classifiers, see
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: AsyncIO',
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
        'aiohttp>=3.1.1',  # why not?
        'coloredlogs>=9.0',  # not needed at all
        'click>=6.7',  # hi, mitshuhiko
        'PyYAML==3.12',  # when json is not enough
    ],

    extras_require={
        'dev': ['twine>=1.11.0'],
    },

    package_data={
        'sample': ['package_data.dat'],
    },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={  # Optional
        'console_scripts': [
            'podmena=cli',
        ],
    },

    project_urls={
        'Blog post': 'https://bmwlog.pp.ua/',
        'Say Thanks!': 'http://saythanks.io/to/example',
    },
)
