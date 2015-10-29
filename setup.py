import os
from setuptools import setup

PACKAGE = 'opsim4'

MAJOR = 0
MINOR = 1
PATCH = 'dev'

try:
    VERSION = "%d.%d.%d" % (MAJOR, MINOR, PATCH)
except TypeError:
    VERSION = "%d.%d.%s" % (MAJOR, MINOR, PATCH)

def write_version(filename="version.py"):
    with open(os.path.join(PACKAGE, filename), 'w') as vfile:
        vfile.write("version = '{}'".format(VERSION)+os.linesep)

if __name__ == '__main__':
    write_version()
    setup(name=PACKAGE,
          version=VERSION,
          description='OpSim version 4 Configuration UI',
          author='Michael Reuter',
          author_email='mareuter@lsst.org',
          url='https://github.com/mareuter/opsim4_config_ui',
          license='GPL',
          long_description=os.linesep+open("README.rst").read(),
          packages=[PACKAGE],
          package_dir={PACKAGE: PACKAGE},
          scripts=['scripts/opsim4_config_ui'],
          )
