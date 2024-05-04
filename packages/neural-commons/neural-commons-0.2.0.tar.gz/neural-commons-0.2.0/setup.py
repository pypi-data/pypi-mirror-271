import codecs

from setuptools import setup, find_packages

# Define project metadata
NAME = 'neural-commons'
VERSION = '0.2.0'
DESCRIPTION = 'A neural network utility library for PyTorch.'
AUTHOR = 'Jose Solorzano'

REQUIRES = [
    'numpy>=1.23',
    'tqdm>=4.0.0',
    'torch>=2.1.0',
    'transformers>=4.28.0',
    'mpmath==1.3.0',
]

# Long description comes from README
with codecs.open('README.md', 'r', 'utf-8') as f:
    LONG_DESCRIPTION = f.read()

packages = find_packages(".")
print(f"Packages: {packages}")

# Setup configuration
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    packages=packages,
    install_requires=REQUIRES,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.9',
)
