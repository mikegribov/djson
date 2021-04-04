from setuptools import setup, find_packages

with open("README.short.txt", "r") as file:
    long_description = file.read()

setup(
    name='xjson',
    version='0.25',
    description='Distributed JSON',
    author='Michael Gribov',
    author_email='mihail.g.gribov@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mikegribov/xjson",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)