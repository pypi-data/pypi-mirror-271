from setuptools import setup, find_packages

setup(
    name='asyncrun',
    version='0.1.0',
    author='Jack English',
    author_email='jackjenglish@gmail.com',
    packages=find_packages(),
    install_requires=[
        'tqdm' 
    ],
    python_requires='>=3.6',
    description='A simple utility for running functions in parallel.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/jackjenglish/asyncrun'
)
