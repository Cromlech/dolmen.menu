# -*- coding: utf-8 -*-

import crom
from .components import Entry
from .interfaces import IMenu, IMenuEntry
from . import directives
from cromlech.browser import IView, IRequest
from grokker import grokker, directive, validator
from zope.interface import Interface


def generate_entry(**bdict):
    """instanciate an Entry from parameters"""
    id = bdict['__component_name__'] = bdict['__name__'] = str(bdict['name'])
    entry = type(id, (Entry,), bdict)
    entry.__name__ = id
    return id, entry


@grokker
@directive(directives.context)
@directive(directives.request)
@directive(directives.target)
@directive(directives.name)
@directive(crom.registry)
def menu_component(
        scanner, pyname, obj, registry,
        context=Interface, request=IRequest,
        view=IView, target=IMenu, name=None):

    if name is None:
        name = obj.__name__.lower()

    obj.__component_name__ = name

    assert target.isOrExtends(IMenu)

    def register():
        registry.register((context, request, view), target, name, obj)

    scanner.config.action(
        callable=register,
        discriminator=('menu',
                       context, request, view, name, registry))



def registering_menuentry(
        scanner, pyname, obj, registry,
        context, request, view, slot, target, name):

    assert target.isOrExtends(IMenuEntry)

    def register():
        registry.register((context, request, view, slot), target, name, obj)

    scanner.config.action(
        callable=register,
        discriminator=('menuentry',
                       context, request, view, slot, name, registry))


@grokker
@directive(directives.context)
@directive(directives.request)
@directive(directives.view)
@directive(directives.slot)
@directive(directives.target)
@directive(directives.name)
@directive(crom.registry)
def menuentry_component(
        scanner, pyname, obj, registry,
        context=Interface, request=IRequest,
        view=IView, slot=IMenu, target=IMenuEntry, name=None):

    if name is None:
        name = obj.__name__.lower()

    obj.__component_name__ = name
    registering_menuentry(scanner, pyname, obj, registry,
                          context, request, view, slot, target, name)


@grokker
@directive(directives.context)
@directive(directives.request)
@directive(directives.view)
@directive(directives.slot)
@directive(directives.title)
@directive(directives.description)
@directive(directives.target)
@directive(directives.name)
@directive(crom.registry)
def menuentry(
        scanner, pyname, obj, registry,
        context=Interface, request=IRequest, title=None, description=None,
        view=IView, slot=IMenu, target=IMenuEntry, name=None):

    if name is None:
        name = obj.__name__.lower()

    pyname, entry = generate_entry(
        name=name, title=title, description=description)
    registering_menuentry(scanner, pyname, entry, registry,
                          context, request, view, slot, target, name)


CONFIGURATION = frozenset(('name', 'url', 'title', 'description'))


def configured_menuentry(
        context=Interface, request=IRequest, menu=None, **options):

    assert CONFIGURATION >= set(options.keys())

    @grokker
    @directive(directives.context)
    @directive(directives.request)
    @directive(directives.view)
    @directive(directives.slot)
    @directive(directives.title)
    @directive(directives.description)
    @directive(directives.target)
    @directive(directives.name)
    @directive(crom.registry)
    def menu_entry(
            scanner, pyname, obj, registry,
            context=context, request=request, title=None,
            description=None, name=None,
            view=IView, slot=IMenu, target=IMenuEntry):

        if 'name' in options:
            name = options['name']
        else:
            if name is None:
                name = obj.__name__.lower()
                options['name'] = name

        if menu is not None:
            slot = menu

        for opt in CONFIGURATION:
            if not opt in options:
                try:
                    value = eval(opt)
                except NameError:
                    continue
                options[opt] = value

        pyname, entry = generate_entry(**options)
        registering_menuentry(scanner, pyname, entry, registry,
                              context, request, view, slot, target, name)

    return menu_entry
