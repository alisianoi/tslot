#!/usr/bin/env python

from setuptools import setup

description = "TimeSlot"

setup(
    name="TimeSlot",
    version="0.0.1",
    description=description,
    long_description=description,
    # scripts=['src/train.py'],
    # entry_points={
    #     "console_scripts": [
    #         "train = src.train.main"
    #     ]
    # },
    install_requires=[
        "pyqt5==5.11.2",
        "sqlalchemy==1.2.10",
        "pendulum==2.0.4",
    ],
    extras_require={
        "dev": [
            "python-language-server[all]",
            "pyls-isort",
            "pyls-black",
            "black-macchiato",
            "pytest==3.7.1",
            "pytest-qt==3.0.0",
            "pytest-cov==2.5.1",
            "pytest-xvfb==1.1.0",
            "pytest-repeat==0.6.0",
            "pytest-xdist==1.22.5",
            "sphinx==1.8.1",
            "sphinxcontrib-tikz==0.4.6",
            "ipython",
        ],
    },
)
