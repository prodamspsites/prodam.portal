from AccessControl import getSecurityManager
# from Acquisition import Explicit
from Acquisition.interfaces import IAcquirer

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
# from zope.interface import implementsOnly, implementer
from zope.component import getMultiAdapter
# from zope.i18n import translate

# import z3c.form.interfaces
# import z3c.form.widget
# import z3c.form.util

from plone.app.layout.navigation.interfaces import INavtreeStrategy
# from plone.app.layout.navigation.navtree import buildFolderTree

# from plone.formwidget.autocomplete.widget import \
#    AutocompleteSelectionWidget, AutocompleteMultiSelectionWidget

from Products.CMFCore.utils import getToolByName
# from Products.Five.browser import BrowserView

# from plone.formwidget.contenttree.interfaces import IContentTreeWidget
# from plone.formwidget.contenttree import MessageFactory as _
from plone.formwidget.contenttree.utils import closest_content

from plone.formwidget.contenttree.widget import Fetch


class MyFetch(Fetch):

    recurse_template = ViewPageTemplateFile('templates/input_recurse.pt')

    def __call__(self):
        # We want to check that the user was indeed allowed to access the
        # form for this widget. We can only this now, since security isn't
        # applied yet during traversal.
        print('CAIU AQUI')
        self.validate_access()

        widget = self.context
        context = widget.context

        # Update the widget before accessing the source.
        # The source was only bound without security applied
        # during traversal before.
        widget.update()
        source = widget.bound_source

        # Convert token from request to the path to the object
        token = self.request.form.get('href', None)
        directory = self.context.bound_source.tokenToPath(token)
        level = self.request.form.get('rel', 0)

        navtree_query = source.navigation_tree_query.copy()
        print(navtree_query)
        if widget.show_all_content_types and 'portal_type' in navtree_query:
            del navtree_query['portal_type']

        if directory is not None:
            navtree_query['path'] = {'depth': 1, 'query': directory}

        if 'is_default_page' not in navtree_query:
            navtree_query['is_default_page'] = False

        content = closest_content(context)

        strategy = getMultiAdapter((content, widget), INavtreeStrategy)
        catalog = getToolByName(content, 'portal_catalog')

        children = []
        for brain in catalog(navtree_query):
            newNode = {'item': brain,
                       'depth': -1,  # not needed here
                       'currentItem': False,
                       'currentParent': False,
                       'children': []}
            if strategy.nodeFilter(newNode):
                newNode = strategy.decoratorFactory(newNode)
                children.append(newNode)

        self.request.response.setHeader('X-Theme-Disabled', 'True')
        return self.fragment_template(children=children, level=int(level))

    def validate_access(self):

        content = self.context.form.context

        # If the object is not wrapped in an acquisition chain
        # we cannot check any permission.
        if not IAcquirer.providedBy(content):
            return

        url = self.request.getURL()
        view_name = url[len(content.absolute_url()):].split('/')[1]

        # May raise Unauthorized

        # If the view is 'edit', then traversal prefers the view and
        # restrictedTraverse prefers the edit() method present on most CMF
        # content. Sigh...
        if not view_name.startswith('@@') and not view_name.startswith('++'):
            view_name = '@@' + view_name
        print(view_name)
        view_name = view_name.replace("%20", " ")
        view_instance = content.restrictedTraverse(view_name)
        getSecurityManager().validate(content, content, view_name,
                                      view_instance)
