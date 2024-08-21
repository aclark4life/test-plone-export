from Products.CMFPlone.factory import addPloneSite
from transaction import commit


def create_plone_site(app):
    site_id = "Plone"

    # Check if the site already exists
    if site_id not in app.objectIds():
        # Create the Plone site with default settings
        addPloneSite(app, site_id, title="My New Plone Site")

        # Commit the transaction to save the changes
        commit()

        print(f"Plone site '{site_id}' created successfully.")
    else:
        print(f"Plone site '{site_id}' already exists.")


# This is the entry point for zconsole run
if __name__ == "__main__":
    app = globals().get("app")
    create_plone_site(app)
