
from setuptools import setup, find_packages

setup(
    name='pyopv',
    version='0.1.0',
    author='Shahin Hallaj',
    author_email='shallaj@health.ucsd.edu',
    description='This package provides a set of tools for chekcing OPV DICOM compliance and converting OPV DICOM to csv or json.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Shallaj/py_opv',  # Replace with your repository URL
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
