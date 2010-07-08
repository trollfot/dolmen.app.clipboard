# -*- coding: utf-8 -*-

import grokcore.viewlet as grok
from dolmen import menu
from zope.location import ILocation
from dolmen.app.layout import MenuViewlet, AboveBody


class CopyPasteMenu(menu.Menu):
    grok.name('copypaste')
    grok.title('Clipboard')
    grok.context(ILocation)
    menu_class = u"menu additional-actions"


class CopyPasteViewlet(MenuViewlet):
    grok.order(30)
    grok.viewletmanager(AboveBody)
    grok.context(ILocation)
    grok.require("dolmen.content.View")
    menu_factory = CopyPasteMenu
