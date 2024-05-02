from setuptools import setup, find_packages

setup(
    name='topaz_data_reduction',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'argparse',
        'requests',
        'bioblend',
        'pathlib',
        'tempfile'
    ],
    author='Jenna DeLozier',
    author_email='delozierjk@ornl.gov',
    description='Package for interacting with Galaxy API for data reduction.',
    keywords='galaxy api data reduction'
)
