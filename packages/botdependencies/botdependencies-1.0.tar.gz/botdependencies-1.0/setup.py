from setuptools import setup

setup(
    name='botdependencies',
    version='1.0',
    author='Emmanuel',
    install_requires=[
        'nltk',
        'pandas',
        'numpy',
        'azure-storage-file-datalake',
        'azure-identity',
    ]
)