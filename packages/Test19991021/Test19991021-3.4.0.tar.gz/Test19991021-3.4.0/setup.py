from setuptools import setup
from setuptools import find_packages


VERSION = '3.4.0'

setup(
    name='Test19991021',  # package name
    version=VERSION,  # package version
    description='my package',  # package description
    packages=find_packages(),
    zip_safe=False,
)