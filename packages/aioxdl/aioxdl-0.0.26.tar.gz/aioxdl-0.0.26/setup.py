from setuptools import setup, find_packages
from aioxdl import appname, version, install, contact, classis

with open("README.md", "r") as o:
    description = o.read()

setup(
    name=appname,
    license='MIT',
    version=version,
    classifiers=classis,
    author_email=contact,
    python_requires='~=3.10',
    packages=find_packages(),
    install_requires=install,
    author='Clinton-Abraham',
    long_description=description,
    description='Python fast downloader',
    url='https://github.com/Clinton-Abraham',
    keywords=['python', 'downloader', 'aiohttp'],
    long_description_content_type="text/markdown")
