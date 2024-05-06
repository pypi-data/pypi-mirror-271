from setuptools import setup, find_packages
from os import path
working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='energysandbox', # name of package which will be package dir below project
    version='0.0.3',
    # url='https://github.com/yourname/yourproject',
    author='Sandstone Group',
    author_email='mtanner@sandstone-group.com',
    description='Energy Sandbox toolset for ETL in the oil and gas business',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(where="energysandbox"),
    package_dir={"": "energysandbox"},
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
)