import os
import mimetypes
import transaction
from optparse import OptionParser
from Products.CMFCore.utils import getToolByName


PORTAL_TYPES = ["File", ]  # Add more types as needed


# Function to write content to file
def write_content_to_file(filepath, content, binary=False):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if binary:
        mode = "wb"
    else:
        mode = "w"
    
    file = open(filepath, mode)
    try:
        file.write(content)
    finally:
        file.close()

# Function to get the correct file extension based on MIME type
def get_file_extension(mime_type):
    return mimetypes.guess_extension(mime_type) or ""

# Function to traverse and export content
def traverse_and_export(context, base_path):
    print "Debug: Starting traverse_and_export"
    
    catalog = getToolByName(context, "portal_catalog")
    if not catalog:
        print "Debug: Could not get 'portal_catalog' tool from context."
        return

    # Debug: print catalog details
    print "Catalog found: %s" % catalog

    # Comprehensive query to include multiple content types and nested content
    query = {
        "portal_type": PORTAL_TYPES, # Adjust content types as needed
        "path": "/".join(context.getPhysicalPath()),
    }
    print "Debug: Query for catalog: %s" % query
    results = catalog.unrestrictedSearchResults(query)

    # Debug: print number of results
    print "Debug: Found %d content objects to export with query %s." % (len(results), query)

    if len(results) == 0:
        print "No content found in the catalog. Please verify the following:"
        print "- Ensure that there are content objects created in your Plone site."
        print "- Check if the catalog is properly indexed."
        print "- Ensure that you have the necessary permissions to access content."

    extensions = []
    for brain in results:
        try:
            obj = brain.getObject()
        except:
            print "Debug: Can't get object"
            continue
        
        # print "Debug: Processing object with ID %s" % obj.getId()
        relative_path = "/".join(
            obj.getPhysicalPath()[2:]
        )  # Get path relative to Plone site
        file_path = os.path.join(base_path, relative_path)

        # Write content to file based on type
        if obj.portal_type == "File":
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

    print "File extensions:"
    print " ".join(extensions)

def main():
    parser = OptionParser(usage="usage: %prog [options] site_name export_base_path")
    parser.add_option("-s", "--site", dest="site_name",
                      help="Name of the Plone site to export from.")
    parser.add_option("-e", "--export", dest="export_base_path",
                      help="Base path where exported files will be saved.")
    (options, args) = parser.parse_args()

    print options, args
    if not options.site_name or not options.export_base_path:
        parser.print_help()
        return

    site_name = options.site_name
    print "Debug: Attempting to find site: %s" % site_name
    
    site = getattr(app, site_name, None)
    if site is None:
        print "Debug: Site %s not found directly. Trying 'Plone'." % site_name
        site = getattr(app, 'Plone', None)
        if site is None:
            raise AttributeError("Site %s not found in app." % site_name)
    
    print "Connected to Plone site: %s" % site

    export_base_path = options.export_base_path
    if not os.path.exists(export_base_path):
        os.makedirs(export_base_path)
        print "Created export base directory at %s." % export_base_path

    traverse_and_export(site, export_base_path)
    transaction.commit()
    print "Export completed."


if __name__ == "__main__":
    main()
