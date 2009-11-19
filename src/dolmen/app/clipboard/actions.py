# -*- coding: utf-8 -*-

import grok
import megrok.menu
from dolmen.app.site import IDolmen
import dolmen.content as content
import dolmen.app.security.content as security
from dolmen.app.layout import MenuViewlet, AboveBody

from zope.intid import IIntIds
from zope.interface import Interface
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.annotation.interfaces import IAnnotations
from zope.copypastemove.interfaces import IObjectCopier, IObjectMover
from zope.copypastemove.interfaces import IPrincipalClipboard
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.container.interfaces import DuplicateIDError

_ = MessageFactory("dolmen.app.clipboard")


def getPrincipalClipboard(request):
    """Return the clipboard based on the request.
    """
    user = request.principal
    annotations = IAnnotations(user, None)
    return IPrincipalClipboard(annotations, None)


class IClipboardDependantAction(Interface):
    """Marker interface for the actions that need a filled clipboard.
    """


class AvailableClipboard(grok.View):
    grok.context(Interface)
    
    def render(self):
        clipboard = getPrincipalClipboard(self.request)
        return bool(clipboard.getContents())


class CopyPasteMenu(megrok.menu.Menu):
    megrok.menu.name('copypaste')
    megrok.menu.title('Clipboard')


class CopyPasteViewlet(MenuViewlet):
    grok.order(30)
    grok.viewletmanager(AboveBody)
    grok.context(content.IBaseContent)
    grok.require("dolmen.content.View")

    menu_name = "copypaste"
    menu_class = "menu additional-actions"


class ClearClipBoard(grok.View):
    grok.title(_(u"Clear clipboard"))
    grok.context(content.IBaseContent)
    grok.require("dolmen.content.View")
    megrok.menu.menuitem(CopyPasteMenu, filter="context/@@availableclipboard")

    def render(self):
        """Clears the clipboard.
        """
        clipboard = getPrincipalClipboard(self.request)
        clipboard.clearContents()
        self.flash(_(u"clipboard_cleared", u"Clipboard cleared"))
        return self.redirect(absoluteURL(self.context, self.request))


class CopyToClipboard(grok.View):
    grok.title(_(u"Copy"))
    grok.context(content.IBaseContent)
    grok.require(security.CanCopyContent)
    megrok.menu.menuitem(CopyPasteMenu)

    def render(self):
        """Copies an object to the clipboard.
        """
        copier = IObjectCopier(self.context)
        if not copier.copyable():
            self.flash(_("Object '${name}' cannot be copied",
                         mapping={"name": self.context.title}))
            return self.redirect(absoluteURL(self.context, self.request))

        intids = getUtility(IIntIds)
        uid = intids.getId(self.context)
        clipboard = getPrincipalClipboard(self.request)
        clipboard.clearContents()
        clipboard.addItems("copy", [uid])
        self.flash(_(u"object_copied",
                     u"Object '${name}' copied to clipboard",
                     {"name": self.context.title}))
        return self.redirect(absoluteURL(self.context, self.request))


class CutToClipboard(grok.View):
    grok.title(_(u"Cut"))
    grok.context(content.IBaseContent)
    grok.require(security.CanCutContent)
    megrok.menu.menuitem(CopyPasteMenu)

    def render(self):
        """Copies an object to the clipboard.
        """
        mover = IObjectMover(self.context)
        if not mover.moveable():
            self.flash(_("Object '${name}' cannot be moved",
                         mapping={"name": self.context.title}))
            return self.redirect(absoluteURL(self.context, self.request))

        intids = getUtility(IIntIds)
        uid = intids.getId(self.context)
        clipboard = getPrincipalClipboard(self.request)
        clipboard.clearContents()
        clipboard.addItems("cut", [uid])
        self.flash(_(u"object_cut",
                     u"Object '${name}' cut to clipboard",
                     {"name": self.context.title}))
        return self.redirect(absoluteURL(self.context, self.request))

    
class HandlePaste(grok.View):
    grok.title(_(u"Paste"))
    grok.context(content.IContainer)
    grok.require(security.CanPasteContent)
    grok.implements(IClipboardDependantAction)
    megrok.menu.menuitem(CopyPasteMenu, filter="context/@@availableclipboard")

    def update(self):
        self.errors = []

    def copy_action(self, obj):
        copier = IObjectCopier(obj)
        try:
            copier.copyTo(self.context)
        except DuplicateIDError:
            self.errors.append(self.context.title)

    def move_action(self, obj):
        mover = IObjectMover(obj)
        try:
            mover.moveTo(self.context)
            return True
        except DuplicateIDError:
            self.errors.append(self.context.title)
            return False
 
    def render(self):
        """Paste an object from the clipboard.
        """
        clipboard = getPrincipalClipboard(self.request)
        items = clipboard.getContents()
        intids = getUtility(IIntIds)
        clear = False
        
        for item in items:
            obj = intids.queryObject(item['target'])
            if obj is None:
                continue

            if item['action'] == 'copy':
                self.copy_action(obj)

            elif item['action'] == 'cut':
                moved = self.move_action(obj)
                if moved is True:
                    clipboard.clearContents()

            elif item['action'] == 'cut':
                self.cut_action(obj)

        if clear is True:
            clipboard.clearContents()

        if len(self.errors):
            self.flash(_("paste_errors",
                         default=u"Couldn't paste : ${names}",
                         mapping={"names": ', '.join(self.errors)}))
            return self.redirect(absoluteURL(self.context, self.request))

        self.flash(_(u"object_pasted",
                     u"Object(s) pasted with success."))
        return self.redirect(absoluteURL(self.context, self.request))
