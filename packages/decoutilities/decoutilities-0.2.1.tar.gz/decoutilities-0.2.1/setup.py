from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
name='decoutilities',
version='0.2.1',
author='Hugo Torres',
author_email='contact@redactado.es',
description='Enhance the readability of your code with decorators and simplify the creation of configuration files.',
packages=find_packages(include=['decoutilities', 'decoutilities.*']),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
long_description=long_description,
long_description_content_type='text/markdown'
)