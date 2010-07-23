# -*- coding: utf-8 -*-

import grokcore.viewlet as grok
from dolmen import menu
from zope.location import ILocation
from dolmen.app.layout import MenuViewlet, AboveBody
from dolmen.app.clipboard import MF as _

class CopyPasteMenu(menu.Menu):
    grok.name('copypaste')
    grok.title(_('Clipboard'))
    grok.context(ILocation)
    menu_class = u"menu additional-actions"


class CopyPasteViewlet(MenuViewlet):
    grok.order(30)
    grok.viewletmanager(AboveBody)
    grok.context(ILocation)
    grok.require("dolmen.content.View")
    menu_factory = CopyPasteMenu
