from setuptools import setup, find_packages

VERSION = '0.0.7'
DESCRIPTION = 'Utilities for indexing a corpus with llama-index'
LONG_DESCRIPTION = 'Utilities for indexing a corpus with llama-index'

setup(
    name='llama-kg',
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
)
