from setuptools import setup, find_packages

setup(
    name='data-quality-validation-pydeequ',
    version='0.1',
    author='Ketan Kirange',
    description='A library for data quality validation using PyDeequ.',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pydeequ',
        'boto3'
        # Add other dependencies here
    ],
)
