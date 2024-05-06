from setuptools import setup, find_packages

setup(
    name='data-quality-validation-pydeequ',
    version='0.2',
    author='Ketan Kirange',
    author_email='k.kirange@reply.com',
    description='A library for data quality validation using PyDeequ.',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'pydeequ',
        'boto3',
        'pyyaml',  
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='data quality validation pydeequ',
)
