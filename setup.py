from setuptools import setup, find_packages

import re

def remove_images_from_markdown(markdown_text):
    # Regex pattern to match Markdown image syntax
    image_pattern = r'!\[.*?\]\(.*?\)'
    # Remove all instances of image syntax from the text
    return re.sub(image_pattern, '', markdown_text)

# Read the content of README.md
with open('README.md', 'r') as f:
    readme_content = f.read()

# Remove images from the readme content
readme_content_without_images = remove_images_from_markdown(readme_content)



setup(
    name='azc',
    version='1.0.3',
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    author='Sagi Smolarski',
    author_email='sagism@gmail.com',
    description='Command-line tool for interacting with LLMs',
    long_description=readme_content_without_images,
    long_description_content_type='text/markdown',
    url='https://github.com/sagism/azc',
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
