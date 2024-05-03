from setuptools import setup, find_packages

setup(
    name='fazah',
    version='3.12',
    description='A library that enhances the multilingual capabilities of Large Language Models by manipulating model input, allowing responses in all languages to be equally as coherent.',
    author='Aiden Lang, Will Foster',
    author_email='ajlang5@wisc.edu, wjfoster2@wisc.edu',
    packages=find_packages(),
    install_requires=[
        'deep_translator',
        'langdetect',
        'openai',
    ],
)
