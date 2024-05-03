from setuptools import find_namespace_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='regression_graph',
    version='2',
    description="Python library for regression graphs using coefficents, confidence intervals and p-values",
    packages=find_namespace_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown", 
    author="Saema Khanom",
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'matplotlib',
        'statsmodels',
        'pandas',
    ],
)

