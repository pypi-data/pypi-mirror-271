from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='princo',
    version='4.0.5',
    author='The Urban Penguin',
    author_email="mahdisahnoun31@gmail.com",  # Replace with your email address
    description='princo package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)
