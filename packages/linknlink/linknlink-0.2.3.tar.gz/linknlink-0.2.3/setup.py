#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


version = '0.2.3'

setup(
    name="linknlink",
    version=version,
    author="Zhao Zehua",
    author_email="huahua.zzh@gmail.com",
    url="https://github.com/xuanxuan000/python-linknlink",
    packages=find_packages(),
    scripts=[],
    install_requires=["cryptography>=3.2"],
    description="Python API for controlling linknlink devices",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    include_package_data=True,
    zip_safe=False,
)
