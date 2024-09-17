from setuptools import setup

setup(
    name='az',
    version='1.0',
    py_modules=['az'],
    entry_points={
        'console_scripts': [
            'az=az:main',
        ],
    },
)
