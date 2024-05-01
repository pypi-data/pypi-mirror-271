
from distutils.core import setup
from setuptools import find_packages

with open("README.MD", "r") as f:
  long_description = f.read()

setup(name='glcl',
      version='0.0.4',
      description='glcl for python studio',
      long_description=long_description,
      author='glsite.com',
      author_email='admin@glsite.com',
      url='',
      install_requires=[],
      license='MIT License',
      packages=["glcl"],
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Topic :: Software Development :: Libraries'
      ],
      )

