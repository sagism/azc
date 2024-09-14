from setuptools import setup

setup(
    name='chata',
    version='1.0',
    py_modules=['chata'],
    entry_points={
        'console_scripts': [
            'az=chata:main',  # 'as' is the command, 'chata:main' points to the `main` function in `chata.py`
        ],
    },
)
