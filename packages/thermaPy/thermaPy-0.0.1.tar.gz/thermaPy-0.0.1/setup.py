from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description=f.read()

setup(
    name='thermaPy',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
       'opencv-python>=4.9.0.80',
       'matplotlib>=3.7.2'
    ],
    long_description=description,
    long_description_content_type='text/markdown'   
)