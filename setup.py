import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.rst")).read()

setup(
    name="django-typesense",
    version="0.1",
    packages=["typesense"],
    description="Adds typesense binding to your Django models",
    long_description=README,
    author="Justin Köstinger",
    author_email="jkoestinger@gmail.com",
    url="https://github.com/jkoestinger/django-typesense/",
    license="MIT",
    install_requires=["Django>=3"],
)
