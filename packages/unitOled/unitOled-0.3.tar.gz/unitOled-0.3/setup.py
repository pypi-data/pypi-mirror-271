import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.3'
PACKAGE_NAME = 'unitOled'
AUTHOR = 'Master'
AUTHOR_EMAIL = 'cesar.bautista@uelectronics.com'
LICENSE = 'MIT'
DESCRIPTION = 'i2c ssd1306 display driver for micropython'
URL = 'https://github.com/Cesarbautista10/ISE_SSD1306/archive/refs/tags/v0.3.tar.gz'
# Read the contents of your README file for the long description
with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Add your required packages to INSTALL_REQUIRES list
INSTALL_REQUIRES = []

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    url=URL,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',  # Specify the type of content
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)