from __future__ import print_function
from setuptools import setup
# from nxp_imu import __version__ as VERSION
from build_utils import get_pkg_version
from build_utils import BuildCommand
from build_utils import PublishCommand
from build_utils import BinaryDistribution

VERSION = get_pkg_version('nxp_imu/__init__.py')
PACKAGE_NAME = 'nxp_imu'
BuildCommand.pkg = PACKAGE_NAME
PublishCommand.pkg = PACKAGE_NAME
PublishCommand.version = VERSION


setup(
	author='Kevin Walchko',
	author_email='walchko@users.noreply.github.com',
	name=PACKAGE_NAME,
	version=VERSION,
	description='python library to use the Adafruit NXP 9-Dof IMU',
	long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
	url='http://github.com/MomsFriendlyRobotCompany/{}'.format(PACKAGE_NAME),
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.6',
		'Topic :: Software Development :: Libraries',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Software Development :: Libraries :: Application Frameworks'
	],
	license='MIT',
	keywords=['raspberry', 'pi', '', 'nxp', 'imu', 'i2c'],
	packages=[PACKAGE_NAME],
	install_requires=['build_utils', 'smbus2'],
	cmdclass={
		'make': BuildCommand,
		'publish': PublishCommand
	}
)
