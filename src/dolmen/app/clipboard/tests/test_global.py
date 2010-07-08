# -*- coding: utf-8 -*-

import re
import doctest
import unittest

from dolmen.app.clipboard import tests
from zope.app.wsgi.testlayer import BrowserLayer
from zope.testing import renormalizing


FunctionalLayer = BrowserLayer(tests)


checker = renormalizing.RENormalizing([
    # Accommodate to exception wrapping in newer versions of mechanize
    (re.compile(r'httperror_seek_wrapper:', re.M), 'HTTPError:')])


def test_suite():
    suite = unittest.TestSuite()
    readme = doctest.DocFileSuite(
        '../README.txt',
        checker=checker,
        globs={'getRootFolder': FunctionalLayer.getRootFolder},
        optionflags=(doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS))
    readme.layer = FunctionalLayer
    suite.addTest(readme)
    return suite
