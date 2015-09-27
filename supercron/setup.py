from setuptools import setup

fp = open('pypi.rst', 'r')
pypi_readme = fp.read()
fp.close()

setup(
	name = 'supercron',
	packages = ['supercron', 'tests'],
	version = '0.2.1',
	description ='Intelligent interface to cron in UNIX systems',
	author = 'Anas El Husseini',
	author_email = 'linux.anas@gmail.com',
	license = 'BSD',
	url = 'https://github.com/linostar/SuperCron',
	download_url = 'https://github.com/linostar/SuperCron/tarball/0.2.0',
	keywords = ['cron', 'crontab', 'scheduling'],
	install_requires = ['python-crontab>=1.9.3'],
	long_description = pypi_readme,
	entry_points = {
	'console_scripts': [
	'supercron = supercron.supercron:main',
	],
	},
	classifiers = [
	'Development Status :: 4 - Beta',
	'Environment :: Console',
	'Intended Audience :: End Users/Desktop',
	'Intended Audience :: System Administrators',
	'Topic :: Utilities',
	'Topic :: System :: Systems Administration',
	'License :: OSI Approved :: BSD License',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3.3',
	'Programming Language :: Python :: 3.4',
	'Programming Language :: Python :: 3.5',
	],
)
