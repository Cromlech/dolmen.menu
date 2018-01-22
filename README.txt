===========
dolmen.menu
===========

``dolmen.menu`` aims to provide the most flexible and explicit way to
create and manage menus and their entries with Cromlech.


You have to know that...
========================

* ``dolmen.menu`` only works on Python3.4+.

* ``dolmen.menu`` does not support sub-menus, out of the box. The
  implementation of such feature is left to your discretion.


Components
==========

``dolmen.menu`` provides two components:

* Menu : the menu implementation is based on the zope "content
  provider" notion and is using the ``dolmen.viewlet`` package.
  It is a specific ViewletManager.

* Entry: a menu item is called an entry. It's a viewlet, and as such, a multi
  adapter registered for a Menu component.


Examples
--------

A menu component::

  >>> @dolmen.menu.menu_component
  ... @dolmen.menu.title('My nice menu')
  ... class MyMenu(dolmen.menu.Menu):
  ...     pass

A menu entry::

  >>> @dolmen.menu.menuentry_component
  ... @dolmen.menu.menu(MyMenu)
  ... class StandaloneEntry(dolmen.menu.Entry):
  ...     url = '/'
  ...     title = 'Standalone'
  ...     description = 'Link to the root'


Registration
============

In order to use any component as menu entries, we get two
registration ways.

class decorator
---------------

A class decorator allows you to decorate any View class, in order to
register it as a menu entry::

  >>> @dolmen.menu.menu_component
  ... class TestEntry(ViewClass):
  ...    def render(self):
  ...        return u"A simple entry"


Module level directive
----------------------

A  directive allows you register classes you can't decorate
(from a foreign package, for instance), explicitly::

  >>> class SomeView(ViewClass):
  ...    def render(self):
  ...        return u"I'm a view and I want to be a menu entry"

  >>> dolmen.menu.configured_menuentry(context=SomeView, menu=MyMenu, order=2)
