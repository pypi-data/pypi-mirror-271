
from distutils.core import setup
from setuptools import find_packages

with open("README.MD", "r") as f:
  long_description = f.read()

setup(name='glcl',
      version='0.0.7',
      description='glcl for python studio',
      long_description=long_description,
      author='glsite.com',
      author_email='admin@glsite.com',
      url='',
      install_requires=[],
      license='MIT License',
      platforms=["all"],
      packages=['glcl'],
      include_package_data=True,
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Topic :: Software Development :: Libraries'
      ],
      )

