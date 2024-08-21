from zope.component import getUtility
from plone.site import addPloneSite
from plone.registry.interfaces import IRegistry
from plone.registry.record import Record
from plone.registry.field import TextLine

def create_plone_site(app):
    site_id = 'Plone'

    # Check if the site already exists
    if site_id not in app.objectIds():
        # Create the Plone site
        addPloneSite(app, site_id)

        # Configure site settings if necessary
        site = app[site_id]
        setup_site(site)

        print(f"Plone site '{site_id}' created successfully.")
    else:
        print(f"Plone site '{site_id}' already exists.")

def setup_site(site):
    # Example: Set a registry record
    registry = getUtility(IRegistry, context=site)
    record_name = 'plone.site_title'
    if record_name not in registry:
        registry.records[record_name] = Record(TextLine(title=u"Site Title"))
    
    registry[record_name] = u"My New Plone Site"

# This is the entry point for zconsole run
if __name__ == '__main__':
    app = globals().get('app')
    create_plone_site(app)
