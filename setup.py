# coding: utf-8
import os
from setuptools import setup, find_packages


here = os.path.dirname(__file__)
packages = find_packages("src")
main_package = packages[0]

with open(os.path.join(here, "requirements.txt"), "r") as fd:
    requirements = [spec for spec in fd.readlines()]

setup(
    name="django-langchain",
    version="0.0.1",
    license="All rights reserved. 2023",
    description="Django Langchain",
    author=" P.A. SCHEMBRI",
    author_email="pa.schembri@advanced-stack.com",
    url="https://github.com/paschembri/django-langchain",
    packages=packages,
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=requirements,
)
