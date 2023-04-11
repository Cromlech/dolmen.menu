# -*- coding: utf-8 -*-

import martian
import dolmen.menu
from cromlech.browser import IRequest
from dolmen.menu.declarations import get_default_name
from zope import component, interface
from zope.interface.verify import verifyClass


def generate_entry(bdict):
    """instanciat an Entry from parameters"""
    id = bdict['__component_name__'] = bdict['__name__'] = str(bdict['name'])
    entry = type(id, (dolmen.menu.Entry,), bdict)
    entry.__name__ = id
    return id, entry


def register_entry(factory, menu, infos, config=None):
    """Registration for class methods"""
    # We get the values from the directives
    values = dolmen.menu.get_entry_values(factory, **infos)

    # We pop the values issued from directives.
    context = values.pop('context')
    view = values.pop('view')
    request = values.pop('request')
    order = values.pop('order')

    # We generate the entry.
    entry_name, entry = generate_entry(values)

    # If order was not from a directive, we set it back, for later sorting.
    if not isinstance(order, tuple):
        dolmen.menu.order.set(entry, (order, 1))

    # We enqueue our component in the registry config.
    config.action(
        discriminator=('menuentry', context, request, view, menu, entry_name),
        callable=component.provideAdapter,
        args=(entry, (context, request, view, menu),
              dolmen.menu.IMenuEntry, entry_name))


class PreAdapterDecoratorGrokker(martian.GlobalGrokker):
    """Call registrators that were annotateid in the module
    by the directives

    see :py:func:`declarations.function_menu_entry()`
    """
    martian.priority(1000)

    def grok(self, name, module, module_info, config, **kw):
        callbacks = module_info.getAnnotation('dolmen.menufunctions', [])
        for register in callbacks:
            register()
        return True


class MenuEntryGrokker(martian.GlobalGrokker):
    """Call registrators that were annotateid in the module
    by the directives

    see :py:func:`declarations.global_menuentry()`
    """

    def grok(self, name, module, module_info, config, **kw):
        callbacks = module_info.getAnnotation('dolmen.menuclasses', [])
        for register in callbacks:
            register(register_entry, config)
        return True


class ViewletMenuEntriesGrokker(martian.ClassGrokker):
    """Grokker for menu entries"""
    martian.component(dolmen.menu.Entry)
    martian.directive(dolmen.menu.context)
    martian.directive(dolmen.menu.view, default=interface.Interface)
    martian.directive(dolmen.menu.request, default=IRequest)
    martian.directive(dolmen.menu.name, get_default=get_default_name)
    martian.directive(dolmen.menu.menu, default=None)

    def execute(self, factory, config, context, menu, view, request,
                name, **kw):
        """Context and menu are mandatory. Menu directive may refer either
        to a class or interface.

        MenuEntry is a viewlet managed by its Menu, so a named adapter of
        (context, request, view, viewletmanager) to
        :py:class:`menu.IMenuEntry`
        """

        if not context:
            raise ValueError("No Context")

        if not menu:
            raise ValueError("No menu")

        if interface.interfaces.IInterface.providedBy(menu):
            if not menu.isOrExtends(dolmen.menu.IMenu):
                raise ValueError("Invalid menu type")
        else:
            if not dolmen.menu.IMenu.implementedBy(menu):
                raise ValueError("Invalid menu type")

        factory.__name__ = factory.__component_name__ = name
        verifyClass(dolmen.menu.IMenuEntry, factory)
        # We enqueue our component in the registry config.
        config.action(
            discriminator=('menu-entry', context, request,
                           view, menu, name),
            callable=component.provideAdapter,
            args=(factory, (context, request, view, menu),
                  dolmen.menu.IMenuEntry, name))

        return True
