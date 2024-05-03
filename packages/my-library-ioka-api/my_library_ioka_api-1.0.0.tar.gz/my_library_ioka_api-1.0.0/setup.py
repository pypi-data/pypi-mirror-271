from setuptools import setup, find_packages

setup(
    name="my_library_ioka_api",
    version='1.0.0',
    description='simple library for ioka api',
    author='sultan',
    packages=find_packages(where='src', exclude=['tests']),
    package_dir={'': 'src'},
    install_requires=['requests', 'dataclasses']
)
