# -*- coding: utf-8 -*-

PROJECTNAME = 'prodam.portal'

DEPS = [
    'archetypes.querywidget',
    'collective.googleanalytics',
    'collective.js.galleria',
    'collective.js.jqueryui',
    'plone.app.blocks',
    'plone.app.collection',
    'plone.app.contenttypes',
    'plone.app.dexterity',
    'plone.app.drafts',
    'plone.app.intid'
    'plone.app.intid',
    'plone.app.iterate',
    'plone.app.jquery',
    'plone.app.jquerytools',
    'plone.app.querystring',
    'plone.app.relationfield',
    'plone.app.theming',
    'plone.app.tiles',
    'plone.app.versioningbehavior',
    'plone.formwidget.autocomplete',
    'plone.formwidget.contenttree',
    'plone.formwidget.querystring',
    'plone.resource',
    'plone.session',
    'plonetheme.classic',
    'Products.Doormat',
    'Products.PloneFormGen',
    'raptus.autocompletewidget',
]


# http://www.tinymce.com/wiki.php/Configuration:formats
TINYMCE_JSON_FORMATS = {'strikethrough': {'inline': 'span',
                                          'classes': 'strikethrough',
                                          'exact': 'true'},
                        'underline': {'inline': 'span',
                                      'classes': 'underline',
                                      'exact': 'true'}}
