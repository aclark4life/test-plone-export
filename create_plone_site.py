# from Products.CMFPlone.factory import addPloneSite
# from transaction import commit
# 
# 
# def create_plone_site(app):
#     site_id = "Plone"
# 
#     # Check if the site already exists
#     if site_id not in app.objectIds():
#         # Create the Plone site with default settings
#         addPloneSite(app, site_id, title="My New Plone Site")
# 
#         # Commit the transaction to save the changes
#         commit()
# 
#         print(f"Plone site '{site_id}' created successfully.")
#     else:
#         print(f"Plone site '{site_id}' already exists.")
# 
# 
# # This is the entry point for zconsole run
# if __name__ == "__main__":
#     app = globals().get("app")
#     create_plone_site(app)

from Products.CMFPlone.factory import addPloneSite
from transaction import commit

def create_plone_site(app):
    site_id = 'Plone'

    # Check if the site already exists
    if site_id not in app.objectIds():
        # Define the add-ons to be installed with the site creation.
        # In this case, we ensure Volto-related add-ons are not included.
        add_on_profiles = [
            'Products.CMFPlone:plone',  # Classic Plone UI
            'plonetheme.barceloneta:default',  # Default theme for classic UI
        ]

        # Create the Plone site with the specified add-ons
        addPloneSite(
            app,
            site_id,
            title="My Classic Plone Site",
            extension_ids=add_on_profiles,
            setup_content=True  # Optional: Create default content (home page, etc.)
        )

        # Commit the transaction to save the changes
        commit()

        print(f"Plone site '{site_id}' with the classic UI created successfully.")
    else:
        print(f"Plone site '{site_id}' already exists.")

# This is the entry point for zconsole run
if __name__ == '__main__':
    app = globals().get('app')
    create_plone_site(app)

