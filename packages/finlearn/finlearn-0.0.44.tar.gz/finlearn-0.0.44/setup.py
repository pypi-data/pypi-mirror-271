from setuptools import setup, find_packages

# Package metadata
NAME = 'finlearn'
DESCRIPTION = 'A one-stop package for entire financial analysis and market prediction using Deep Learning'
VERSION = '0.0.44'
AUTHOR = 'Ankit Dutta'
AUTHOR_EMAIL = 'ankitduttaiitkgp@gmail.com'
#URL = 'https://github.com/your_username/your_repository'
LICENSE = 'Apache 2.0'

# Read long description from README file
with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()

# Define dependencies
INSTALL_REQUIRES = [
    'plotly',
    'yfinance',
    'matplotlib'
    # Add more dependencies as needed
]

# Define additional classifiers
CLASSIFIERS = [
    'Programming Language :: Python :: 3',
    # Add more classifiers as needed
]

# Call setup() function to define the package
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
)
