import distutils.core
import sys

if sys.argv[-1] == 'setup.py':
    print("To install, run 'python setup.py install'")
    print()

if sys.version_info[:2] < (2, 6):
    print("PRIMO requires Python version 2.6 or later (%d.%d detected)." %
          sys.version_info[:2])
    sys.exit(-1)

distutils.core.setup(
    name='primo',
    version='1.0',
    description='PRobabilistic Inference MOdules',
    long_description='This project contains probabilistic inference modules for Python. Our aim is to create a library which offers well known probabilistic (graphical) models like Bayesian or temporal networks. A variety of inference algorithms will be implemented soon.',
    author='Manuel Baum, Hendrik Buschmeier, Denis John, Lukas Kettenbach, Max Koch',
    url='https://github.com/mbaumBielefeld/PRIMO',
    download_url='https://github.com/mbaumBielefeld/PRIMO/archive/develop.zip',
    packages = ['primo', 'primo.inference']
)
