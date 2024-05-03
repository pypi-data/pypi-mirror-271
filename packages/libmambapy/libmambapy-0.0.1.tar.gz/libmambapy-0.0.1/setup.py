# Always prefer setuptools over distutils
from setuptools import setup, find_packages

company = "aws-samples--aws-ai-ml-workshop-kr"
name = "libmambapy"
version = "0.0.1"

from setuptools import setup

setup(
    name=name,
    version=version,
    author="Kotko Vladyslav",
    author_email="m@kotko.org",
    description="",
    packages=find_packages(),
    install_requires=['requests'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        ]
)

