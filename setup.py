# coding: utf-8
from pathlib import Path
from setuptools import setup, find_packages


here = Path(__file__).parent
packages = find_packages("src")
main_package = packages[0]
long_description = (here / "README.md").read_text()
requirements = (here / "requirements.txt").read_text().split("\n")

setup(
    name="django-langchain",
    version="0.0.1",
    license="All rights reserved. 2023",
    description="Django Langchain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=" P.A. SCHEMBRI",
    author_email="pa.schembri@advanced-stack.com",
    url="https://github.com/paschembri/django-langchain",
    packages=packages,
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
)
