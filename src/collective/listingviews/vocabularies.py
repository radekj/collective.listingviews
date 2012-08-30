from zope.schema.vocabulary import SimpleVocabulary
from collective.listingviews.interfaces import IListingDefinition
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite


class LVVocabulary(SimpleVocabulary):
    """
    Don't error out if you can't find it right away
    and default to the default value...
    This prevents any issues if a field
    is removed and the user had it selected.
    """

    def __init__(self, terms, *interfaces, **config):
        try:
            super(LVVocabulary, self).__init__(terms, *interfaces)
        except:
            import pdb
            pdb.set_trace()
            raise
        if 'default' in config:
            self.default = config['default']
        else:
            self.default = None

    def getTerm(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        try:
            return self.by_value[value]
        except KeyError:
            return self.by_value[self.default]
        except:
            raise LookupError(value)


def ListingViewVocabulary(context):
    terms = []
    registry = queryUtility(IRegistry)
    if registry is not None:
        facets = sorted(registry.collectionOfInterface(IListingDefinition,
            prefix='collective.listingviews.view').items())
        for view, fields in facets:
            name = getattr(fields, 'name', '')
            terms.append(SimpleVocabulary.createTerm(view, view, name))
    return SimpleVocabulary(terms)


def MetadataVocabulary(context):
    terms = []
    portal = getSite()
    catalog = getToolByName(portal, 'portal_catalog')
    # should use schema or indexes
    for name in catalog.schema():
        terms.append(SimpleVocabulary.createTerm(name, name, name))
    return SimpleVocabulary(terms)
