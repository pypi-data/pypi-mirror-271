from setuptools import setup, find_packages

try:
    long_desc = open('README.md').read()
except:
    long_desc = ''

setup(
    name="dfcleanser",
    version="1.0.0",
    author="Rick Krasinski",
    author_email="rickmkrasinski@gmail.com",
    description="A Jupyter notebook extension for dataframe cleansing",
    long_description=long_desc,
    url="https://github.com/RickKrasinski/dfcleanser",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "jupyter==1",
    ],
)
