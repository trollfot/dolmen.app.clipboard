# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.app.clipboard'
version = '0.1'
readme = open(join('src', 'dolmen', 'app', 'clipboard', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'grok',
    'grokcore.viewlet',
    'dolmen.app.layout',
    'dolmen.app.security',
    'zope.container',
    'zope.i18nmessageid',
    'zope.interface',
    'zope.location',
    'zope.principalannotation',
    'dolmen.menu',
    'setuptools',
    'zope.annotation',
    'zope.component',
    'zope.copy>=3.5.0',
    'zope.copypastemove',
    'zope.intid',
    ]

tests_require = [
    'grokcore.component',
    'zope.container',
    'zope.publisher',
    'zope.site',
    'zope.securitypolicy',
    'zope.pluggableauth',
    'zope.principalregistry',
    'zope.app.appsetup',
    'zope.app.publication',
    'zope.app.wsgi >= 3.9.2',
    'zope.browserpage',
    'zope.i18n',
    'zope.testing',
    'zope.principalannotation',
    'zope.security',
    ]

setup(name = name,
      version = version,
      description = 'Clipboard copy/paste for Dolmen applications',
      long_description = readme[readme.find('\n\n'):] + '\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = 'http://gitweb.dolmen-project.org/',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen', 'dolmen.app'],
      include_package_data=True,
      zip_safe=False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
