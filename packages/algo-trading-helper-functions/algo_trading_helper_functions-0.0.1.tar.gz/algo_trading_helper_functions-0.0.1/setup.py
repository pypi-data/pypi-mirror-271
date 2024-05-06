from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Starting with creating algo trading helper functions'
LONG_DESCRIPTION = 'A package that allows to do algo trading using these helper functions.'

# Setting up
setup(
    name="algo_trading_helper_functions",
    version=VERSION,
    author="Kiddo (Dhaval Chheda)",
    author_email="<kiddo.dhaval@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'pandas-ta'],
    keywords=['python', 'algo', 'trading', 'candlestick patterns', 'zerodha', 'kite'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)