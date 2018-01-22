# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.menu'
version = '3.0-crom'
readme = open("README.txt").read()
history = open(join('docs', 'HISTORY.txt')).read()


install_requires = [
    'crom',
    'cromlech.browser >= 0.5',
    'cromlech.i18n',
    'dolmen.template >= 0.2',
    'dolmen.viewlet >= 0.4',
    'setuptools',
    'zope.interface',
    'zope.location',
    'zope.schema',
    ]


tests_require = [
    'pytest',
    'cromlech.browser [test]',
    'cromlech.location',
    ]


setup(name=name,
      version=version,
      description='Dolmen menu components',
      long_description=readme + '\n\n' + history,
      keywords='Dolmen Menu',
      author='The Dolmen team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Other Audience',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
      )
