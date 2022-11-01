#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

test_requirements = ['pytest>=2', ]

setup(
    author="Bruno Peixoto",
    author_email='brunolnetto@gmail.com',
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Euler's diagrams are non-empty Venn's diagrams",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='eule',
    name='eule',
    packages=find_packages(include=['eule', 'eule.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/brunolnetto/eule',
    version='0.1.5',
    zip_safe=False,
)
