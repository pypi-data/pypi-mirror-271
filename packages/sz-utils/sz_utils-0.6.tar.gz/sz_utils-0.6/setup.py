from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='sz-utils',
    version='0.6',
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    author='Peng Zhou',
    author_email='zhoupeng23@nuaa.edu.cn',
    description='A simple example library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/PeterouZh',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
