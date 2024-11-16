# setup.py
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dataauto',
    version='1.0.2',
    author='Pachigulla Ramtej',
    author_email='ram.pachi.tej@example.com',
    description='An open-source tool for automating data analysis tasks.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/r4mp4g3r/dataauto',
    packages=find_packages(),
    install_requires=[
        'click>=8.1.3',
        'pandas>=1.5.3',
        'numpy>=1.25.0',
        'matplotlib>=3.7.1',
        'seaborn>=0.12.2',
    ],
    entry_points='''
        [console_scripts]
        dataauto=dataauto.cli:cli
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)