import pathlib
import re
import setuptools


setuptools.setup(
    name='skybridge',
    version='0.1.0',
    description='Fast client and server for sending array data.',
    url='http://github.com/danijar/skybridge',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=['skybridge'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
