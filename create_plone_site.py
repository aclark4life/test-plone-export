import sys
from Products.CMFPlone.factory import addPloneSite
from transaction import commit
from plone.namedfile.file import NamedBlobFile

def create_plone_site(app, ui_type="classic"):
    site_id = "Plone"

    # Check if the site already exists
    if site_id not in app.objectIds():
        # Determine the add-on profiles to install based on the UI type
        if ui_type == "classic":
            add_on_profiles = [
                "Products.CMFPlone:plone",  # Classic Plone UI
                "plonetheme.barceloneta:default",  # Default theme for classic UI
            ]
            title = "My Classic Plone Site"
        elif ui_type == "volto":
            add_on_profiles = [
                "Products.CMFPlone:plone",  # Base Plone setup
                "plone.restapi:default",  # REST API needed for Volto
                "plone.volto:default",  # Volto frontend
            ]
            title = "My Volto Plone Site"
        else:
            print(f"Unknown UI type: {ui_type}")
            sys.exit(1)

        # Create the Plone site with the specified add-ons
        addPloneSite(
            app,
            site_id,
            title=title,
            extension_ids=add_on_profiles,
            setup_content=True,  # Optional: Create default content
        )

        # Commit the transaction to save the changes
        commit()

        print(f"Plone site '{site_id}' with the {ui_type} UI created successfully.")
        
        # Add a File with a PDF after site creation
        site = app[site_id]
        file_id = "example-pdf"
        file_title = "Example PDF"
        
        with open("alex-clark-resume.pdf", "rb") as pdf_file:
            pdf_data = pdf_file.read()

        # Create a NamedBlobFile for the PDF data
        pdf_blob = NamedBlobFile(data=pdf_data, filename="file.pdf")

        # Add the File content type
        site.invokeFactory(
            type_name="File",
            id=file_id,
            title=file_title,
            file=pdf_blob,
        )

        # Commit the transaction to save the changes
        commit()

        print(f"PDF file '{file_id}' added to the site '{site_id}' successfully.")
    else:
        print(f"Plone site '{site_id}' already exists.")


# This is the entry point for zconsole run
if __name__ == "__main__":
    app = globals().get("app")

    # The correct argument for UI type should be the last one
    if len(sys.argv) < 2:
        print("Usage: zconsole run create_plone_site.py <classic|volto>")
        sys.exit(1)

    # Get the last argument which should be the UI type
    ui_type = sys.argv[-1].lower()
    create_plone_site(app, ui_type)
