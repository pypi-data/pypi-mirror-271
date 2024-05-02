
from setuptools import setup, find_packages

setup(
    name='pyblksim',
    version='0.1.0',
    packages=find_packages(),
    description='Python package for block simulation',
    author='Dr. Kurian Polachan',
    author_email='kurian.polachan@iiitb.ac.in',
    license='GPLv3',
    install_requires=[
        'numpy',
        'matplotlib',
        'simpy',
        'scipy',
    ],
    python_requires='>=3.6',
)
