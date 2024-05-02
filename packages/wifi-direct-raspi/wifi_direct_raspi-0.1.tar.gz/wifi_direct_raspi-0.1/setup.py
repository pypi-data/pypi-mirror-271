import os
from setuptools import setup
from setuptools.command.install import install
import subprocess

class InstallConfig(install):
    def run(self):
        install.run(self)
        subprocess.run(['sudo', 'python', 'run_conf.py'])

def __read__(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()

setup (
    name='wifi_direct_raspi',
    version='0.1',
    description = "Wi-Fi Direct Library for Raspberry Pi",
    readme = "README.md",
    author="Tatiana Reimer", 
    author_email="tatireimer99@gmail.com",
    long_description=__read__('README.md'),
    url='https://www.python.org/sigs/distutils-sig/',
    cmdclass={
        'install': InstallConfig,
    },
)