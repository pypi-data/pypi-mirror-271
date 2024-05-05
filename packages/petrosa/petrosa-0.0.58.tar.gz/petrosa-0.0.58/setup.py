from setuptools import setup, find_packages
import os

def read(*paths, **kwargs):
    """Read the contents of a text file safely."""
    content = ""
    with open(os.path.join(*paths), encoding=kwargs.get("encoding", "utf-8")) as f:
        content = f.read()
    return content


setup(
    name="petrosa",  # Replace with your project's name
    version="0.0.58",  # Replace with your project's version
    description="Human-Robot-Quant for markets",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,  # Include data files from your packages
    install_requires=[
        "pandas",
        "pymongo",
        "kafka-python",
        "requests",
        "mysql-connector",
        "opentelemetry-distro",
        "opentelemetry-exporter-otlp",
    ],
    classifiers=[
        # Add relevant classifiers from https://pypi.org/classifiers/
    ],
)
