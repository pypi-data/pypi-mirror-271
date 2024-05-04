from setuptools import setup

DEPENDENCIES = ['setuptools']

VERSION = "0.0.4-alpha1"
DOC = ""

setup(
    name='WGSE-NG',
    packages=['wgse'],
    author='Multiple',
    author_email='',
    description='Whole Genome Sequencing data manipulation tool',
    long_description='Whole Genome Sequencing data manipulation tool',
    install_requires=DEPENDENCIES,
    entry_points = {},
    url='https://github.com/chaplin89/WGSE-NG',
    version=VERSION,
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.12',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
      ],
    keywords='bioinformatics'
)