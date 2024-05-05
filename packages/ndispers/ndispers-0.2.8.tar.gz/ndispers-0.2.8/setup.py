from codecs import open

from setuptools import find_packages, setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="ndispers",
    version='0.2.8',
    packages=find_packages(),

    author='Akihiko Shimura',
    author_email='akhksh@gmail.com',
    url='https://github.com/akihiko-shimura/ndispers',
    description='Python package for calculating refractive index dispersion of various materials',
    long_description=long_description,
    long_description_content_type='text/markdown',

    install_requires=['numpy', 
                      'scipy', 
                      'sympy',
                      'mpmath'],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
)
