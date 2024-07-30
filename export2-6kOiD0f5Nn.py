import os
import mimetypes
import transaction
from zope.component.hooks import setSite
from Products.CMFCore.utils import getToolByName

# Function to write content to file
def write_content_to_file(filepath, content, binary=False):
    if binary:
        mode = "wb"
    else:
        mode = "w"
    file = open(filepath, mode)
    file.write(content)

# Function to get the correct file extension based on MIME type
def get_file_extension(mime_type):
    return mimetypes.guess_extension(mime_type) or ""

# Function to traverse and export content
def traverse_and_export(context, base_path):
    catalog = getToolByName(context, "portal_catalog")

    # Debug: print catalog details
    print "Catalog found: %s" % catalog

    # Comprehensive query to include multiple content types and nested content
    query = {
        "portal_type": [
            "Document",
            "News Item",
            "File",
            "Folder",
        ],  # Adjust content types as needed
        "path": "/".join(context.getPhysicalPath()),
    }
    results = catalog.unrestrictedSearchResults(query)

    # Debug: print number of results
    print "Found %d content objects to export with query %s." % (len(results), query)

    if len(results) == 0:
        print "No content found in the catalog. Please verify the following:"
        print "- Ensure that there are content objects created in your Plone site."
        print "- Check if the catalog is properly indexed."
        print "- Ensure that you have the necessary permissions to access content."

    for brain in results:
        try:
            obj = brain.getObject()
            relative_path = "/".join(
                obj.getPhysicalPath()[2:]
            )  # Get path relative to Plone site
            file_path = os.path.join(base_path, relative_path)

            # Debug: print object details
            print "Processing object at %s with ID %s and type %s." % (
                relative_path, obj.getId(), obj.portal_type
            )

            # Ensure the directory exists
            if not os.path.exists(os.path.dirname(file_path)):
                os.makedirs(os.path.dirname(file_path))
                print "Created directories for %s." % os.path.dirname(file_path)

            # Write content to file based on type
            if obj.portal_type in ["Document", "News Item"]:
                content = "Title: %s\n\nDescription: %s\n\nText: %s" % (
                    obj.Title(), obj.Description(), obj.getText()
                )
                write_content_to_file(file_path + ".txt", content.encode("utf-8"))
                print "Exported: %s.txt" % file_path
            elif obj.portal_type == "File":
                if hasattr(obj, "file") and obj.file:
                    file_data = obj.file.data
                    mime_type = obj.file.contentType
                    extension = get_file_extension(mime_type)
                    write_content_to_file(file_path + extension, file_data, binary=True)
                    print "Exported: %s%s" % (file_path, extension)
                else:
                    print "Skipping file export for %s due to missing file attribute." % file_path
            else:
                print "Skipping unsupported content type %s at %s" % (obj.portal_type, relative_path)

        except Exception as e:
            print "Error processing object at %s: %s" % (brain.getPath(), str(e))

def main(app):
    try:
        site = app.Plone
        setSite(site)

        # Debug: print site details
        print "Connected to Plone site: %s" % site

        export_base_path = "export"  # Change this to the desired export directory
        if not os.path.exists(export_base_path):
            os.makedirs(export_base_path)
            print "Created export base directory at %s." % export_base_path

        traverse_and_export(site, export_base_path)
        transaction.commit()
        print "Export completed."

    except AttributeError:
        print "Error: Could not find the Plone site at app.Plone."
        print "Make sure the Plone site exists and is correctly referenced."

if __name__ == "__main__":
    main(app)  # noqa
