from setuptools import setup, find_packages

with open("README.md","r") as fh:
    long_description = fh.read()

setup(
    name="weatherapi-sdk",
    version="0.0.1",
    packages=find_packages(),
    install_requires=["requests"],
    author="Snehal Palve",
    description="A simple SDK for interacting with the OpenWeatherMap API",
    long_description=long_description,
    long_description_content_type= "text/markdown",
    classifiers =[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"],
    package_dir = {'':'src'},
    python_requires = ">=3.6",
    # url="https://github.com/snehalnp/weatherapi-sdk"
)
