#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
    name='mylib',
    version='0.1',
    packages=find_packages(where='.'),
    package_dir={'': '.'},
    include_package_data=True,
    package_data={
        '': ['*.py', '*.png', '*.jpg', '*.kv', '*.atlas'],
    },
    install_requires=[
        'python3',
        'kivy',
        'pyzbar',
        'pillow',
        'mysql-connector-python',
        'pyjwt',
        'KivyGradient==0.0.4',
    ],
    entry_points={
        'console_scripts': [
            'mylib = main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.8.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
