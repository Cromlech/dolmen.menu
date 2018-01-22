"""

Groking::

  >>> from crom import testing, configure

  >>> import dolmen.menu
  >>> import cromlech.location
  >>> from dolmen.menu.tests import test_menu

  >>> testing.setup()
  >>> configure(dolmen.menu, cromlech.location, test_menu)

A root of publication to compute url::

  >>> from zope.location.location import Location
  >>> from zope.interface import directlyProvides
  >>> from cromlech.browser import IPublicationRoot

  >>> root = Location()
  >>> directlyProvides(root, IPublicationRoot)
  >>> context = Location()
  >>> context.__parent__, context.__name__ = root, 'test'

  >>> from cromlech.browser.testing import TestRequest
  >>> request = TestRequest()

A very basic view is used as a context for the menu::

  >>> someview = SomeView(context, request)
  >>> mymenu = dolmen.menu.IMenu(context, request, someview, name="mymenu")

Use it ::

  >>> mymenu.update()
  >>> mymenu.viewlets
  [<menu.menuentry `other` for menu `MyMenu`>, <menu.menuentry `someview` for menu `MyMenu`>, <menu.menuentry `standaloneentry` for menu `MyMenu`>]

  >>> print(mymenu.render())  # doctest: +NORMALIZE_WHITESPACE
  <dl id="mymenu" class="menu">
    <dt>My nice menu</dt>
    <dd>
      <ul>
        <li class="entry">
          <a href="http://localhost/test/other"
             title="Nice view" alt="Another entry">Nice view</a>
        </li>
        <li class="entry">
          <a href="http://localhost/test/someview" class="selected"
             title="Nice view" alt="This is a nice view.">Nice view</a>
        </li>
        <li class="entry">
          <a href="/" title="Standalone" alt="Link to the root">Standalone</a>
        </li>
      </ul>
    </dd>
  </dl>

  >>> testing.teardown()

"""

from cromlech.browser import IView
from dolmen.menu import components, directives, grokkers
from zope.interface import implementer, Interface


@grokkers.menu_component
@directives.title('My nice menu')
class MyMenu(components.Menu):
    pass


@implementer(IView)
@grokkers.menuentry
@directives.menu(MyMenu)
@directives.title('Nice view')
@directives.description('This is a nice view.')
@grokkers.configured_menuentry(description="Another entry", name="other")
class SomeView(object):

    __component_name__ = 'someview'

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def render(self, *args, **kwargs):
        return u"I'm a simple view"


@grokkers.menuentry_component
@directives.menu(MyMenu)
class StandaloneEntry(components.Entry):
    url = '/'
    title = u'Standalone'
    description = u'Link to the root'
