# -*- coding: utf-8 -*-
from prodam.portal.browser.viewlets.analytics import AnalyticsViewlet
from prodam.portal.testing import INTEGRATION_TESTING

import unittest


class AnalyticsViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.qi = self.portal['portal_quickinstaller']
        self.st = self.portal['portal_setup']

    def viewlet(self):
        viewlet = AnalyticsViewlet(self.portal, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_analyticsviewlet(self):
        expected = u'<div id="plone-analytics"></div>'
        viewlet = self.viewlet()
        self.assertEqual(viewlet.render(), expected)
