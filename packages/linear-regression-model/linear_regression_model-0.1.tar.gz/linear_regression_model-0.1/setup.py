from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description_md = f.read()

setup(
    name='linear_regression_model',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "scikit-learn"
    ],
    long_description=description_md,
    long_description_content_type="text/markdown"
)
