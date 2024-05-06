import pathlib
from setuptools import setup, find_packages

setup(
    name='VSVNApplicationMonitoring',  # Replace with your actual package name 
    version='0.1.4',
    description="Used for integration with Application monitoring systems",
    long_description = pathlib.Path("README.rst").read_text(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        # Your project dependencies
    ],
)
