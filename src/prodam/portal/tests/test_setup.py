# -*- coding: utf-8 -*-
from plone.browserlayer.utils import registered_layers
from prodam.portal.testing import INTEGRATION_TESTING
import unittest

PROFILE_ID = 'prodam.portal:default'


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.st = self.portal['portal_setup']

    def test_browser_layer(self):
        layers = [l.getName() for l in registered_layers()]
        self.assertTrue('IProdamPortal' in layers,
                        'add-on layer was not installed')
