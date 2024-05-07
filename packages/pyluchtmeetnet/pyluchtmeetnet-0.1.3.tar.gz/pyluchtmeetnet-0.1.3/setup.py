"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyluchtmeetnet",
    version="0.1.3",
    description="A module for getting air quality data from Luchtmeetnet OpenAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metbril/pyluchtmeetnet",
    author="Robert van Bregt",
    author_email="robertvanbregt@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="air quality, health, api",
    packages=find_packages(),
    python_requires=">=3.8, <4",
    install_requires=["requests"],
    project_urls={
        "Bug Reports": "https://github.com/metbril/pyluchtmeetnet/issues",
        "Funding": "https://ko-fi.com/metbril",
        "Source": "https://github.com/metbril/pyluchtmeetnet/",
    },
)
