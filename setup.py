# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

setup(
    name='poketrainer',
    version='0.1.0',
    description='Webapp for gamifying personal training with pokemon',
    url='https://pokefitbit.herokuapp.com/',
    packages=find_packages(),
)
