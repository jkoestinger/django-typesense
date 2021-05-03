import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

setup(
    name="django-type_sense",
    version="0.1",
    packages=["type_sense"],
    description="Adds type_sense binding to your Django models",
    long_description=README,
    author="Justin Köstinger",
    author_email="jkoestinger@gmail.com",
    url="https://github.com/jkoestinger/django-typesense/",
    license="MIT",
    install_requires=["Django>=3"],
)
