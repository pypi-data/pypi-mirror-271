from setuptools import setup
import pypandoc


try:
    description=pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    description=open('README.md').read()
setup(
	name='TeleCryptoBot',
	version='1.3',
	author='vh1dz',
	author_email='vh1dz@vh1dz.ru',
	description='Библиотека для удобного использования API CryptoPay',
    long_description=description,
	url='https://github.com/vh1dz/TeleCryptoBot',
	packages=['TeleCryptoBot'],
    install_requires=['pypandoc==1.5', 'pydantic>=2.3.0'],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)