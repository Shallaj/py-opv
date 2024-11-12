from setuptools import setup, find_packages

setup(
    name='pyopv',
    version='0.1.2.1',
    author='Shahin Hallaj, MD',
    author_email='shallaj@health.ucsd.edu',
    description='This package provides a set of tools for checking OPV DICOM compliance and converting OPV DICOM to CSV or JSON.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Shallaj/py-opv',
    packages=find_packages(),
    install_requires=[
        'pydicom',
        'numpy',
        'pandas',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
