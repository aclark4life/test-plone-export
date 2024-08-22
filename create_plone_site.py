import sys
from Products.CMFPlone.factory import addPloneSite
from transaction import commit
from plone.namedfile.file import NamedBlobFile

def create_plone_site(app, ui_type="classic", pdf_path=None):
    site_id = "Plone"

    # Check if the site already exists
    if site_id not in app.objectIds():
        # Determine the add-on profiles to install based on the UI type
        if ui_type == "classic":
            add_on_profiles = [
                "Products.CMFPlone:plone",  # Classic Plone UI
                "plonetheme.barceloneta:default",  # Default theme for classic UI
                "plone.app.dexterity:default"  # Dexterity content types
            ]
            title = "My Classic Plone Site"
        elif ui_type == "volto":
            add_on_profiles = [
                "Products.CMFPlone:plone",  # Base Plone setup
                "plone.restapi:default",  # REST API needed for Volto
                "plone.volto:default",  # Volto frontend
                "plone.app.dexterity:default"  # Dexterity content types
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
        # commit()

        print(f"Plone site '{site_id}' with the {ui_type} UI created successfully.")
        
        # Add a File with a PDF after site creation
        site = app[site_id]
        item_id = "example-file"
        item_title = "Example File"
        
        if pdf_path:
            try:
                with open(pdf_path, "rb") as pdf_file:
                    pdf_data = pdf_file.read()

                # Create a NamedBlobFile for the PDF data
                pdf_blob = NamedBlobFile(data=pdf_data, filename="file.pdf")

                # Add the File content type
                site.invokeFactory(
                    type_name="File",  # Ensure "File" content type is available
                    id=item_id,
                    title=item_title,
                    file=pdf_blob,
                )
                print(f"File '{item_id}' added to the site '{site_id}' successfully.")
            except Exception as e:
                print(f"Failed to add file: {e}")
        else:
            print("No PDF file path provided. Skipping file addition.")
        
        # Commit the transaction to save the changes
        commit()

    else:
        print(f"Plone site '{site_id}' already exists.")


# This is the entry point for zconsole run
if __name__ == "__main__":
    app = globals().get("app")

    # Print raw arguments for debugging
    print(f"Raw arguments: {sys.argv}")

    # Extract the relevant arguments
    if len(sys.argv) < 5:
        print("Usage: zconsole run create_plone_site.py <classic|volto> [pdf_path]")
        sys.exit(1)

    # The second argument should be the UI type
    ui_type = sys.argv[4].lower()
    # The third argument should be the PDF path if provided
    pdf_path = sys.argv[5] if len(sys.argv) > 5 else None

    # Debug prints to verify parsed arguments
    print(f"UI Type: {ui_type}")
    print(f"PDF Path: {pdf_path}")

    create_plone_site(app, ui_type, pdf_path)
