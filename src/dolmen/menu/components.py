# -*- coding: utf-8 -*-

import grokcore.view
from grokcore.component import baseclass
from grokcore import view, viewlet
from zope.location.interfaces import ILocation
from dolmen.menu.interfaces import IMenu, IMenuEntry
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.interface import implements
from zope.component import getAdapters


class Menu(viewlet.ViewletManager):
    """
    """
    baseclass()
    implements(IMenu)

    template = grokcore.view.PageTemplateFile("templates/genericmenu.pt")

    actions = None
    menu_class = u"menu"
    entry_class = u"entry"

    def filter(self, viewlets):
        pass

    
    def _get_entries(self, actions):
        if not actions:
            return []

        url = absoluteURL(self.context, self.request)
        selected = getattr(self.view, '__name__', None)
        entries = []

        for action in actions:
            name = action.__name__
            title = view.title.bind().get(action) or name
            is_selected = name == selected
            entries.append({
                    'url': "%s/%s" % (url, name),
                    'title': title,
                    'selected': is_selected,
                    'css': (is_selected and
                            self.entry_class + ' selected' or
                            self.entry_class)})
        return entries


    def update(self):
        self.__updated = True
        self.title = view.title.bind().get(self) or self.__name__

        # Find all content providers for the region
        viewlets = getAdapters(
            (self.context, self.request, self.__parent__, self),
            IMenuEntry)

        viewlets = self.sort(viewlets)

        # Just use the viewlets from now on
        self.viewlets=[]
        for name, viewlet in viewlets:
            if ILocation.providedBy(viewlet):
                viewlet.__name__ = name
            self.viewlets.append(viewlet)

        self._updateViewlets()
        self.actions = self._get_entries(self.viewlets)

    def render(self):
        return self.template.render(self)


class MenuEntry(viewlet.Viewlet):
    """
    """
    baseclass()
