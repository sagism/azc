from setuptools import setup

setup(
    name='azc',
    version='1.0',
    py_modules=['az'],
    entry_points={
        'console_scripts': [
            'azc=az.az:main',
        ],
    },
)
