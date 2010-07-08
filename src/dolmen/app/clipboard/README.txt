********************
dolmen.app.clipboard
********************

``dolmen.app.clipboard`` provides a useable "clipboard", that allows
you to cut, copy and paste your objects.

Initial Grok imports
====================

  >>> import grok
  >>> from grokcore.component.testing import grok_component


Setting up contents
===================

In order to test our clipboard, we need to create contents, that will
allow us to cut/copy/paste them around.

  >>> root = getRootFolder()
  >>> root['item'] = grok.Model()
  >>> root['folder'] = grok.Container()


Accessing the clipboard
=======================

The clipboard is user dependent, meaning that all users have their own
clipboard. To access it, we can use the convenient method
`getPrincipalClipboard`, that fetches out the clipboard, if provided
the request::

  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()

  >>> from dolmen.app.clipboard import getPrincipalClipboard

No principal
------------

If there's no principal, the method returns nothing::

  >>> print request.principal
  None

  >>> clipboard = getPrincipalClipboard(request)
  >>> print clipboard
  None

Valid principal
---------------

Principals annotations
~~~~~~~~~~~~~~~~~~~~~~

  >>> from zope.component import provideUtility
  >>> from zope.principalannotation.utility import PrincipalAnnotationUtility
  >>> from zope.principalannotation.interfaces import IPrincipalAnnotationUtility

  >>> pr_anno = root['annotations'] = PrincipalAnnotationUtility()
  >>> provideUtility(pr_anno, IPrincipalAnnotationUtility)

Principal's clipboard
~~~~~~~~~~~~~~~~~~~~~

  >>> from zope.security.testing import Principal, Participation
  >>> from zope.security.management import newInteraction, endInteraction

  >>> manager = Principal('zope.mgr')
  >>> request.setPrincipal(manager)

  >>> clipboard = getPrincipalClipboard(request)
  >>> print clipboard
  <zope.copypastemove.PrincipalClipboard object at ...>


Copying
=======
  
