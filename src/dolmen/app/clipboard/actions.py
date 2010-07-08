# -*- coding: utf-8 -*-

import grok
import dolmen.app.security.content as security

from dolmen.app.clipboard import MF as _

from zope.intid import IIntIds
from zope.interface import Interface, Attribute, implements
from zope.location import ILocation
from zope.container.interfaces import IContainer
from zope.component import getUtility
from zope.annotation.interfaces import IAnnotations
from zope.copypastemove.interfaces import IObjectCopier, IObjectMover
from zope.copypastemove.interfaces import IPrincipalClipboard
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.container.interfaces import DuplicateIDError, InvalidItemType


class IClipboardAction(Interface):
    name = Attribute('Name of the action')
    mesg = Attribute('Human readable message linked to the action')


def copy_action(item, container):
    copier = IObjectCopier(item)
    try:
        copier.copyTo(container)
        return True
    except (KeyError, DuplicateIDError, InvalidItemType):
        return False


def move_action(item, container):
    mover = IObjectMover(item)
    try:
        mover.moveTo(container)
        return True
    except (KeyError, DuplicateIDError, InvalidItemType):
        return False


class ClipboardAction(object):
    implements(IClipboardAction)
    
    def __init__(self, name, mesg, processor):
        self.name = name
        self.mesg = mesg
        self.func = processor

    def process(self, item, container):
        return self.func(item, container)

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return '<ClipboardAction %r>' % self.name


CUT = ClipboardAction('CUT', _('Cut'), move_action)
COPY = ClipboardAction('COPY', _('Copy'), copy_action)


def getPrincipalClipboard(request):
    """Return the clipboard based on the request.
    """
    user = request.principal
    annotations = IAnnotations(user, None)
    return IPrincipalClipboard(annotations, None)


def addToClipboard(request, items, action=COPY, clear=True):
    assert len(items)
    assert isinstance(items, list)
    assert IClipboardAction.providedBy(action)
    
    intids = getUtility(IIntIds)
    ids = list()
    added = list()
    errors = list()


    for item in items:
        uid = intids.queryId(item)
        if uid is None:
            errors.append(item)
        else:
            added.append(item)
            ids.append(uid)

    if ids:
        clipboard = getPrincipalClipboard(request)
        if clear is True:
            # We clear the clipboard before filling it.
            clipboard.clearContents()
        clipboard.addItems(action, ids)
 
    return added, errors


def processClipboard(request, container):
    """Paste objects from the clipboard.
    """
    clipboard = getPrincipalClipboard(request)
    contents = clipboard.getContents()

    intids = getUtility(IIntIds)
    errors = list()
    pasted = list()

    for content in contents:
        action = content['action']
        target = content['target']

        item = intids.queryObject(target)
        if item is None:
            continue

        result = action.process(item, container)

        if result is False:
            errors.append(item)
        else:
            pasted.append(item)
    
    return pasted, errors
