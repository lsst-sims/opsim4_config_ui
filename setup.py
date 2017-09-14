import os
from setuptools import Command, setup
import stat
import subprocess

PACKAGE = 'opsim4'

MAJOR = 0
MINOR = 7
PATCH = 0

MODULE = "lsst.sims.{}".format(PACKAGE)

VERSION = "%d.%d.%d" % (MAJOR, MINOR, PATCH)

def is_newer(src, target):
    """Function to check timestamps for file creation
    """
    if not os.path.exists(target):
        return True
    src_mtime = os.stat(src)[stat.ST_MTIME]
    target_mtime = os.stat(target)[stat.ST_MTIME]
    return src_mtime > target_mtime

def exec_cmd(cmd):
    """Function to run command calls
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, _) = proc.communicate()
    proc.wait()
    if proc.returncode:
        print(stdout)

class BuildRccCommand(Command):
    description = "Build PyQt resources"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        qtr = "image_resources.qrc"
        parts = MODULE.split('.')
        parts.append("image_resources.py")
        pyqtr = os.path.join(*parts)

        if is_newer(qtr, pyqtr):
            # print(qtr, pyqtr)
            pyrcc_cmd = ["pyrcc5"]
            pyrcc_cmd.extend(["-o", "{}".format(pyqtr), "{}".format(qtr)])
            print(" ".join(pyrcc_cmd))
            exec_cmd(pyrcc_cmd)

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
          cmdclass={'build_rcc': BuildRccCommand},
          packages=[
              'lsst',
          ],
          package_dir={'lsst':
                       'lsst'},
          scripts=['scripts/opsim4_config_ui'],
          )
