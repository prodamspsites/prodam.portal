# -*- coding: utf-8 -*-
from prodam.portal.browser.viewlets.analytics import AnalyticsViewlet
from prodam.portal.browser.viewlets.logo import LogoViewlet
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


class LogoViewletTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.portal.title = u'Prefeitura de São Paulo'
        self.portal.description = u'Portal da Prefeitura de São Paulo'

    def viewlet(self):
        viewlet = LogoViewlet(self.portal, self.request, None, None)
        viewlet.update()
        return viewlet

    def test_title(self):
        expected = self.portal.title
        viewlet = self.viewlet()
        self.assertEqual(viewlet.title(), expected)

    def test_description(self):
        expected = self.portal.description
        viewlet = self.viewlet()
        self.assertEqual(viewlet.description(), expected)

    def test_portal(self):
        expected = self.portal
        viewlet = self.viewlet()
        self.assertEqual(viewlet.portal(), expected)
