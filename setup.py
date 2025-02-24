from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# get version from __version__ variable in trg_marketing/__init__.py
from trg_marketing import __version__ as version

setup(
    name="trg_marketing",
    version=version,
    description="TRG Marketing",
    author="slife",
    author_email="info@slife.guru",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)