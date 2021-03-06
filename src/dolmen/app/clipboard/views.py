# -*- coding: utf-8 -*-

import grok
import dolmen.app.security.content as security

from dolmen import menu
from dolmen.app.clipboard import MF as _
from dolmen.app.clipboard import actions
from dolmen.app.clipboard.menu import CopyPasteMenu
from zope.location import ILocation
from zope.container.interfaces import IContainer


@menu.menuentry(CopyPasteMenu)
class ClearClipBoard(grok.View):
    grok.title(_(u"Clear clipboard"))
    grok.context(ILocation)
    grok.require(security.CanEditContent)

    def render(self):
        """Clears the clipboard.
        """
        clipboard = actions.getPrincipalClipboard(self.request)
        clipboard.clearContents()
        self.flash(_(u"clipboard_cleared", u"Clipboard cleared"))
        return self.redirect(self.url(self.context))


@menu.menuentry(CopyPasteMenu)
class CopyToClipboard(grok.View):
    grok.title(_(u"Copy"))
    grok.context(ILocation)
    grok.require(security.CanCopyContent)

    def render(self):
        """Copies an object to the clipboard.
        """
        copied, errors = actions.addToClipboard(
            self.request, [self.context], action=actions.COPY)

        if copied:
            self.flash(_(u"object_copied",
                         u"Object '${name}' copied to clipboard.",
                         {"name": self.context.__name__}))
        if errors:
            self.flash(_(u"object_copy_error",
                         "Object '${name}' cannot be copied",
                         mapping={"name": self.context.title}))

        return self.redirect(self.url(self.context))


@menu.menuentry(CopyPasteMenu)
class CutToClipboard(grok.View):
    grok.title(_(u"Cut"))
    grok.context(ILocation)
    grok.require(security.CanCutContent)

    def render(self):
        """Copies an object to the clipboard.
        """
        moved, errors = actions.addToClipboard(
            self.request, [self.context], action=actions.CUT)

        if moved:
            self.flash(_(u"object_moved",
                         u"Object '${name}' cut to clipboard.",
                         {"name": self.context.__name__}))
        if errors:
            self.flash(
                _(u"object_move_error",
                  u"Object '${name}' cannot be moved.",
                  mapping={"name": self.context.__name__}))

        return self.redirect(self.url(self.context))


@menu.menuentry(CopyPasteMenu)
class HandlePaste(grok.View):
    grok.title(_(u"Paste"))
    grok.context(IContainer)
    grok.require(security.CanPasteContent)

    def render(self):
        """Paste an object from the clipboard.
        """
        pasted, errors = actions.processClipboard(self.request, self.context)

        if len(errors):
            names = [error.__name__ for error in errors]
            self.flash(_("paste_errors",
                         default=u"Couldn't paste : ${names}",
                         mapping={"names": ', '.join(names)}))

        if len(pasted):
            names = [item.__name__ for item in pasted]
            self.flash(_(u"object_pasted",
                         u"Object(s) ${names} pasted with success.",
                         mapping={"names": ', '.join(names)}))

        return self.redirect(self.url(self.context))
