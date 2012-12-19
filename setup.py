from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='csirteerak',
      version=version,
      description="'event registration package for django'",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author="Jatsu Argarate",
      author_email="jargarate@codesyntax.com",
      url='http://www.codesyntax.com/products',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'django-page-cms',
          'django-authority',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
