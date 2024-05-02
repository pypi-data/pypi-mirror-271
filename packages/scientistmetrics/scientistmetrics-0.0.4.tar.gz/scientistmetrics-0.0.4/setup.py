# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scientistmetrics", 
    version="0.0.4",
    author="Duverier DJIFACK ZEBAZE",
    author_email="duverierdjifack@gmail.com",
    description="Python package for metrics and scoring : quantifying the quality of predictions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enfantbenidedieu/scientistmetrics",
    packages=setuptools.find_packages(),
    install_requires=["numpy>=1.26.4",
                      "pandas>=2.2.2",
                      "scikit-learn>=1.2.2",
                      "plotnine>=0.10.1",
                      "statsmodels>=0.14.0",
                      "scipy>=1.10.1"],
    python_requires=">=3.10",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)