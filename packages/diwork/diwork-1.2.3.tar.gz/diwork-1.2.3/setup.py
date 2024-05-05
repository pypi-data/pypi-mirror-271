# coding: utf-8

from setuptools import setup, find_packages
from distutils.util import convert_path

# https://setuptools.pypa.io/en/latest/userguide/quickstart.html
# pip install --upgrade pip
# pip install --upgrade build
# pip install --upgrade setuptools
# python3 -m pip install --upgrade twine
# python3 -m build
# python3 -m twine upload --repository testpypi dist/*
# pip3 install --no-deps --index-url https://test.pypi.org/simple {package_name}

main_ns = {}
ver_path = convert_path("diwork/__version__.py")
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name="diwork",
    version=main_ns["__version__"],
    install_requires=[
        "argparse",
        "tqdm",
    ],
    packages=find_packages(
        # All keyword arguments below are optional:
        where='.',  # '.' by default or "src"
    ),
    entry_points={
        "console_scripts": [
                "diwork = diwork.main:main",
            ]
    },
    include_package_data=False,
)
