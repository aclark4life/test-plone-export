import os
import mimetypes
import transaction
from zope.component.hooks import setSite
from Products.CMFCore.utils import getToolByName


PORTAL_TYPES = [
    "File",
]  # Add more types as needed


# Function to write content to file
def write_content_to_file(filepath, content, binary=False):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    mode = "wb" if binary else "w"
    with open(filepath, mode) as file:
        file.write(content)


# Function to get the correct file extension based on MIME type
def get_file_extension(mime_type):
    return mimetypes.guess_extension(mime_type) or ""


# Function to traverse and export content
def traverse_and_export(context, base_path):
    catalog = getToolByName(context, "portal_catalog")

    # Debug: print catalog details
    print(f"Catalog found: {catalog}")

    # Comprehensive query to include multiple content types and nested content
    query = {
        "portal_type": PORTAL_TYPES,
        ],  # Adjust content types as needed
        "path": "/".join(context.getPhysicalPath()),
    }
    results = catalog.unrestrictedSearchResults(query)

    # Debug: print number of results
    print(f"Found {len(results)} content objects to export with query {query}.")

    if len(results) == 0:
        print("No content found in the catalog. Please verify the following:")
        print("- Ensure that there are content objects created in your Plone site.")
        print("- Check if the catalog is properly indexed.")
        print("- Ensure that you have the necessary permissions to access content.")

    for brain in results:
        try:
            obj = brain.getObject()
            relative_path = "/".join(
                obj.getPhysicalPath()[2:]
            )  # Get path relative to Plone site
            file_path = os.path.join(base_path, relative_path)

            # Debug: print object details
            print(
                f"Processing object at {relative_path} with ID {obj.getId()} and type {obj.portal_type}."
            )

            # Write content to file based on type
            if obj.portal_type == "File":
                if hasattr(obj, "file") and obj.file:
                    file_data = obj.file.data
                    mime_type = obj.file.contentType
                    extension = get_file_extension(mime_type)
                    if not file_path.endswith(extension):
                        file_path += extension
                    write_content_to_file(file_path, file_data, binary=True)
                    print(f"Exported: {file_path}")
                else:
                    print(
                        f"Skipping file export for {file_path} due to missing file attribute."
                    )
            else:
                print(
                    f"Skipping unsupported content type {obj.portal_type} at {relative_path}"
                )

        except Exception as e:
            print(f"Error processing object at {brain.getPath()}: {e}")


def main(app):
    try:
        site = app.Plone
        setSite(site)

        # Debug: print site details
        print(f"Connected to Plone site: {site}")

        export_base_path = "export"  # Change this to the desired export directory
        if not os.path.exists(export_base_path):
            os.makedirs(export_base_path)
            print(f"Created export base directory at {export_base_path}.")

        traverse_and_export(site, export_base_path)
        transaction.commit()
        print("Export completed.")

    except AttributeError:
        print("Error: Could not find the Plone site at app.Plone.")
        print("Make sure the Plone site exists and is correctly referenced.")


if __name__ == "__main__":
    main(app)  # noqa
