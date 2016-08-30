import os
from setuptools import setup

PACKAGE = 'opsim4'

MAJOR = 0
MINOR = 8
PATCH = 0

MODULE = "lsst.sims.{}".format(PACKAGE)

VERSION = "%d.%d.%d" % (MAJOR, MINOR, PATCH)

def write_version(filename="version.py"):
    parts = MODULE.split('.')
    parts.append(filename)
    with open(os.path.join(*parts), 'w') as vfile:
        vfile.write("__version__ = '{0}'".format(VERSION) + os.linesep)
        vfile.write("__version_info__ = ({0}, {1}, {2})".format(MAJOR, MINOR, PATCH) + os.linesep)
        vfile.write(os.linesep)
        vfile.write("__all__ = ('__version__', '__version_info__')" + os.linesep)

if __name__ == '__main__':
    write_version()
    setup(name=PACKAGE,
          version=VERSION,
          description='OpSim version 4 Configuration UI',
          author='Michael Reuter',
          author_email='mareuter@lsst.org',
          url='https://github.com/lsst-sims/opsim4_config_ui',
          license='MIT',
          long_description=os.linesep + open("README.rst").read(),
          packages=[
              'lsst',
          ],
          package_dir={'lsst':
                       'lsst'},
          scripts=['scripts/opsim4_config_ui'],
          )
