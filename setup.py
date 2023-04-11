# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.menu'
version = '2.4'
readme = open("README.txt").read()
history = open(join('docs', 'HISTORY.txt')).read()


install_requires = [
    'cromlech.browser >= 0.5',
    'cromlech.i18n',
    'dolmen.location >= 0.2',
    'dolmen.template >= 0.2',
    'dolmen.viewlet >= 0.4',
    'grokcore.component',
    'zope.dottedname',  # bug not declared by grokcore.security >= 1.6
    'martian',
    'setuptools',
    'zope.component',
    'zope.interface',
    'zope.location',
    'zope.schema',
    ]

tests_require = [
    'cromlech.browser [test]',
    'zope.configuration',
    ]

tests_security = [
    'dolmen.viewlet [security]',
    'grokcore.security',
    'zope.security',
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
      extras_require={'test': tests_require, 'security': tests_security},
      classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Other Audience',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
      )
