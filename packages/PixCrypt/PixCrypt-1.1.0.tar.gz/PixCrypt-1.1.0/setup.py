from setuptools import setup, find_packages


def readme():
	with open('README.md', 'r') as f:
		return f.read()


setup(
	name='PixCrypt',
	version='1.1.0',
	author='ALhorm',
	author_email='gladkoam@gmail.com',
	description='Library for encrypting text into an image',
	long_description=readme(),
	long_description_content_type='text/markdown',
	packages=find_packages(),
	install_requires=['pillow>=10.0.0'],
	classifiers=[
		'Programming Language :: Python :: 3.11',
	    'License :: OSI Approved :: MIT License',
	    'Operating System :: OS Independent'
	],
	keywords='pixcrypt pillow image encryption python',
	python_requires='>=3.10'
)
