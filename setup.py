from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

setup(
    name='djson',
    version='0.12',
    description='Distributed JSON',
    author='Michael Gribov',
    author_email='mihail.g.gribov@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikegribov/djson",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)