# -*- coding: utf-8 -*-

import urllib
from os import path

import dolmen.viewlet
from .directives import title, description
from .interfaces import IMenu, IMenuEntry
from crom.utils import sort_components
from cromlech.browser import IRequest, IURL
from cromlech.i18n import getLocalizer
from dolmen.template import TALTemplate
from dolmen.viewlet import query_components
from zope.interface import implementer, Interface
from zope.location import Location
from zope.schema.fieldproperty import FieldProperty


template_dir = path.join(path.dirname(__file__), 'templates')

default_menu_template = TALTemplate(
    filename=path.join(template_dir, "menu.pt"))

default_entry_template = TALTemplate(
    filename=path.join(template_dir, "entry.pt"))


@implementer(IMenu)
class Menu(dolmen.viewlet.ViewletManager):
    """Viewlet Manager working as a menu.

    template may be provided as an attribute or will be search as an
    adapter of the menu and the request to IPageTemplate
    """
    template = default_menu_template

    viewlets = tuple()
    menu_class = FieldProperty(IMenu['menu_class'])
    entry_class = FieldProperty(IMenu['entry_class'])
    context_url = FieldProperty(IMenu['context_url'])
    menu_context = FieldProperty(IMenu['menu_context'])

    @property
    def id(self):
        """id for eg. html id attribute.
        """
        component_name = getattr(self, '__component_name__', None)
        if component_name is None:
            return self.__class__.__name__.lower()
        return component_name

    @property
    def title(self):
        return title.get(self)
    
    @property
    def entries(self):
        return self.viewlets

    def setMenuContext(self, item):
        self.menu_context = item

    def getMenuContext(self):
        return self.menu_context or self.context

    def update(self):
        # We get the real context
        menu_context = self.getMenuContext()

        # Get the MenuContext and calculate its url
        self.context_url = str(IURL(menu_context, self.request))

        # Get the viewlets, sort them and update them
        self.viewlets = sort_components(list(query_components(
            menu_context, self.request, self.view, self,
            interface=IMenuEntry)))


@implementer(IMenuEntry)
class Entry(dolmen.viewlet.Viewlet):
    """The menu entry viewlet

    template may be provided as an attribute or will be search as an
    adapter of the menu and the request to IPageTemplate
    """
    params = None
    template = default_entry_template

    def __repr__(self):
        return  "<menu.menuentry `%s` for menu `%s`>" % (
            self.__component_name__, self.manager.__class__.__name__)

    def namespace(self):
        """Objects that will be available in template"""
        namespace = {}
        namespace['context'] = self.context
        namespace['request'] = self.request
        namespace['view'] = self.view
        namespace['entry'] = self
        namespace['viewlet'] = self
        namespace['menu'] = self.manager
        return namespace

    @property
    def selected(self):
        """Does current page corresponds to this menu entry ?

        Permits to eg. highlith entry

        You may override this if you do not use default strategy of view name
        matching last part of target url
        """
        if self.__component_name__ == self.view.__component_name__:
            return True
        return False

    @property
    def url(self):
        """The url the menu entry is pointing at

        Default appends menu entry name to current page url, as it is often the
        case for an action on an object (eg. edit is /path/to/objetc/edit)

        You may override for a different strategy
        """
        url = "%s/%s" % (self.manager.context_url, self.__component_name__)
        if self.params:
            url += '?' + urllib.urlencode(self.params, doseq=True)
        return url

    @property
    def title(self):
        return title.get(self)

    @property
    def permission(self):
        try:
            import grokcore.security
            return grokcore.security.require.bind().get(self)
        except ImportError:
            return None

    @property
    def description(self):
        return description.get(self)
