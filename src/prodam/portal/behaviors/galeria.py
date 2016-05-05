from plone.autoform.interfaces import IFormFieldProvider
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope.interface import provider


@provider(IFormFieldProvider)
class IGaleria(model.Schema):
    """Behavior interface to make a type support related items.
    """

    relatedItems = RelationList(
        title=u"Related Items",
        default=[],
        value_type=RelationChoice(title=u"Related", source=ObjPathSourceBinder(portal_type='Image')),
        required=False,)
