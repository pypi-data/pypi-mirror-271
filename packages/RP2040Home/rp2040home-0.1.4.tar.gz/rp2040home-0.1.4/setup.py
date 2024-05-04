from setuptools import setup, find_packages
from pathlib import Path
import os

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
release_version = os.environ.get("RELEASE_VERSION", "0.1.0")

setup(
name='RP2040Home',
version=release_version,
author='Ellington S',
author_email='',
description='MQTT Client for RP2040 based boards which integrates into Home Assistant',
long_description=long_description,
long_description_content_type='text/markdown',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
