#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = []

test_requirements = ['pytest>=2', ]

setup(
    name='eule',
    author='Bruno Peixoto',
    author_email='brunolnetto@gmail.com',
    python_requires='>=2.7',
    classifiers=[
        'Development Status :: 4 - Beta'
        'Framework :: tox'
        'Intended Audience :: Developers'
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
        'Topic :: Software Development :: Testing'
        'Topic :: Software Development :: Libraries'
        'Topic :: Utilities'
        'Programming Language :: Python :: 2'
        'Programming Language :: Python :: 2.7'
        'Programming Language :: Python :: 3'
        'Programming Language :: Python :: 3.4'
        'Programming Language :: Python :: 3.5'
        'Programming Language :: Python :: 3.6'
        'Programming Language :: Python :: 3.7'
        'Programming Language :: Python :: 3.8'
    ],
    description="Euler's diagrams are non-empty Venn's diagrams",
    install_requires=requirements,
    license='MIT license',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords=['euler', 'venn', 'diagrams'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    test_suite='tests',
    tests_require=test_requirements,
    url='http://eule.readthedocs.org',
    version='0.1.8',
    zip_safe=False,
)
