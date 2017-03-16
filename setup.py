#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "Flask==0.12",
    "graphitesend==0.7.0"
]

setup_requirements = [
    "pytest-runner"
]

test_requirements = [
    "pytest==3.0.0"
]

setup(
    name='flask_graphite',
    version='0.1.0',
    description="Flask-Graphite grant you the power to push useful metrics"
                " for each route without effort",
    long_description=readme + '\n\n' + history,
    author="Numberly",
    author_email='alexandre.bonnetain@1000mercis.com',
    url='https://github.com/numberly/flask_graphite',
    packages=[
        'flask_graphite',
    ],
    package_dir={'flask_graphite':
                 'flask_graphite'},
    include_package_data=True,
    install_requires=requirements,
    setup_requires=setup_requirements,
    license="BSD license",
    zip_safe=False,
    keywords='flask_graphite',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='py.test',
    tests_require=test_requirements
)
