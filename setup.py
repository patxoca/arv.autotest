from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='autotest',
      version=version,
      description="Executa tests al canviar els arxius",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Alexis Roda',
      author_email='alexis.roda.villalonga@gmail.com',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "blessings",
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
