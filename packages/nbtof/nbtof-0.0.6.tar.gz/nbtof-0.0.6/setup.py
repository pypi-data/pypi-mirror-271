from setuptools import setup

DESCRIPTION = "nbtof: transfering notebook to function"
NAME = 'nbtof'
AUTHOR = 'Haruka Nodaka'
AUTHOR_EMAIL = 'haruka.nodaka@gmail.com'
URL = 'https://github.com/Nodaka/nbtof'
LICENSE = 'MIT'
DOWNLOAD_URL = 'https://github.com/Nodaka/nbtof'
VERSION = "0.0.6"
PYTHON_REQUIRES = ">=3.9"

INSTALL_REQUIRES = [
#    'pandas',
#    'nbconvert',
#    'jupyter',
]

PACKAGES = [
    'nbtof',
]

CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development :: Code Generators',
    'Framework :: Jupyter',
]

with open('README.md', 'r', encoding="utf-8") as fp:
    readme = fp.read()
long_description = readme
long_description_content_type = "text/markdown"

setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    license=LICENSE,
    url=URL,
    version=VERSION,
    download_url=DOWNLOAD_URL,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    classifiers=CLASSIFIERS
    )