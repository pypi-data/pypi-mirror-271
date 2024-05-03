from setuptools import setup, find_packages

setup(
    name='zern',
    version='1.0.0',
    author='Harsha Avapati',
    author_email='harshaavapati@gmail.com',
    description='An unofficial client library using Zerodha web api for live data and historical data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ExBlacklight/Zern',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
