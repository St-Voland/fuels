import os
from typing import Any, Dict

import setuptools
from setuptools import find_packages, setup

# pip3 install google-api-python-client oauth2client

REQUIRED = [
    "python-telegram-bot==13.11",
    "google-api-python-client",
    "oauth2client",
    "click>=7.1.2, <8.0.0",
    "numpy",
    "lat_lon_parser"
]

here = os.path.abspath(os.path.dirname(__file__))

about: Dict[str, str] = {}
with open(os.path.join(here, "fuels", "__info__.py"), "r") as f:
    exec(f.read(), about)
print("Version = ", about["__version__"])

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    python_requires=">=3.5.0",
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    include_package_data=True,
    install_requires=REQUIRED,
    zip_safe=False,
    entry_points={"console_scripts": ["fuels=fuels.cli:cli"]}
)
