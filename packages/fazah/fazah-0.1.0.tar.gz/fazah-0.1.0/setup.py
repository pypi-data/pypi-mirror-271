from setuptools import setup, find_packages

setup(
    name='fazah',
    version='0.1.0',
    description='A library for multilingual translation using language models',
    author='Aiden Lang, Will Foster',
    author_email='ajlang5@wisc.edu, wjfoster2@wisc.edu',
    packages=find_packages(),
    install_requires=[
        'deep_translator',
        'langdetect',
        'openai',
    ],
)
