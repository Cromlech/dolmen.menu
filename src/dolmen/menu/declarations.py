# -*- coding: utf-8 -*-

import martian
import sys
import types
import zope.interface
import zope.component

from martian.error import GrokImportError
from martian.util import frame_is_module

from cromlech.browser import IRequest
from cromlech.browser.directives import view, request
from dolmen.menu.interfaces import IMenu, IMenuEntry
from grokcore.component import order, title, name, description, context

try:
    import grokcore.security
    SecurityGetter = lambda:grokcore.security.require.bind(default='zope.View')

except ImportError:

    class SecurityGetter(object):
        def get(self, factory):
            return None


def get_default_name(factory, module=None, **data):
    return factory.__name__.lower()


EXTRACTABLES = {
    'name': name.bind(get_default=get_default_name),
    'title': title.bind(get_default=get_default_name),
    'description': description.bind(default=u""),
    'context': context.bind(default=zope.interface.Interface),
    'request': request.bind(default=IRequest),
    'view': view.bind(default=zope.interface.Interface),
    'permission': SecurityGetter(),
    'order': order.bind(),
    }


def get_entry_values(factory, **extras):
    """helper function to get configuration values from args or, as a fallback
    from martian directives"""
    values = {}
    for name, directive in EXTRACTABLES.items():
        if name in extras:
            values[name] = extras.get(name)
        else:
            value = directive.get(factory)
            values[name] = value
    # Keep additional extras
    for name in extras:
        if name not in EXTRACTABLES:
            values[name] = extras.get(name)
    return values


def function_menu_entry(frame, entry, menu, infos):
    """return the registrer of a function as a menu entry.
    """
    def register():
        values = get_entry_values(entry, **infos)
        context = values.get('context')
        view = values.get('view')
        request = values.get('request')
        # add declarations to make function an adapter to IMenuEntry
        adapter = zope.component.adapter(context, request, view, menu)
        implementer = zope.interface.implementer(IMenuEntry)
        adapter(entry)  # declare
        implementer(entry)  # declare
        adapters = frame.f_locals.get('__grok_adapters__', None)
        if adapters is None:
            frame.f_locals['__grok_adapters__'] = adapters = []
        adapters.append(entry)
    return register


def class_menu_entry(frame, entry, menu, infos):
    """return the registrator of a class or a method as a menu entry.
    """
    def register(register_method, config):
        register_method(entry, menu, infos, config)
    return register


def validateMenu(directive, value):
    if not IMenu.implementedBy(value):
        raise ValueError(
            "You can only register a menu item on a IMenu component.")


class menu(martian.Directive):
    scope = martian.CLASS
    store = martian.ONCE
    # validate = validateMenu


class global_menuentry(martian.MultipleTimesDirective):
    """Class declaration as a menu entry"""
    scope = martian.MODULE

    def factory(self, component, menu, **args):
        validateMenu(self, menu)
        if not martian.util.isclass(component):
            raise TypeError(
                "`global_menuentry` can only be used with class components."
                " For functions, use directly zope.component.provideAdapter")

        frame = sys._getframe(2)
        entries = frame.f_locals.get('__dolmen_menuclasses__', None)
        if entries is None:
            frame.f_locals['__dolmen_menuclasses__'] = entries = []
            callback = class_menu_entry
        entries.append(callback(frame, component, menu, args))
        return (component, menu, args)


class menuentry(object):
    """
    Decorator meant to be use on a function to declare it as a menu entry

    Annotates the class for further grokking
    see : meta.PreAdapterDecoratorGrokker and meta.MenuEntryGrokker
    """

    def __init__(self, menu, **args):
        self.menu = menu
        self.infos = args

    def __call__(self, entry):
        frame = sys._getframe(1)
        if not frame_is_module(frame):
            raise GrokImportError(
                "@dolmen.menu.menuentry can only be used at the module level")

        if not self.menu:
            raise GrokImportError(
                "@dolmen.menu.menuentry requires at least one argument.")

        if type(entry) is types.FunctionType:
            entries = frame.f_locals.get('__dolmen_menufunctions__', None)
            if entries is None:
                frame.f_locals['__dolmen_menufunctions__'] = entries = []
            callback = function_menu_entry
        else:
            entries = frame.f_locals.get('__dolmen_menuclasses__', None)
            if entries is None:
                frame.f_locals['__dolmen_menuclasses__'] = entries = []
            callback = class_menu_entry
        entries.append(callback(frame, entry, self.menu, self.infos))
        return entry
