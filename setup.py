from setuptools import setup, find_packages


setup(
    name='azc',
    version='1.0.2',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    author='Sagi Smolarski',
    author_email='sagism@gmail.com',
    description='Command-line tool for interacting with LLMs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sagism/az',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    py_modules=['az'],
    entry_points={
        'console_scripts': [
            'azc=az.az:main',
        ],
    }
)
