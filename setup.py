from setuptools import setup

setup(
    name='matrix-rain',
    version='1.0',
    py_modules=['matrix'],
    entry_points={
        'console_scripts': [
            'matrix=matrix:main',
        ],
    },
)