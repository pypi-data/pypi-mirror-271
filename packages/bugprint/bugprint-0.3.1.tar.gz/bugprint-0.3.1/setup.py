from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.3.1'
DESCRIPTION = 'Debug printing made easy.'

# Setting up
setup(
    name="bugprint",
    version=VERSION,
    author="Erik Luu",
    author_email="eeluu19@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[''],
    license="MIT",
    keywords=['python', 'debug', 'print'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
