import os
import transaction
from zope.component.hooks import setSite
from Products.CMFCore.utils import getToolByName

# Function to write content to file
def write_content_to_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)

# Function to traverse and export content
def traverse_and_export(context, base_path):
    catalog = getToolByName(context, 'portal_catalog')
    
    # Debug: print catalog details
    print(f"Catalog found: {catalog}")
    
    # Comprehensive query to include multiple content types and nested content
    query = {
        'portal_type': ['Document', 'News Item', 'File', 'Folder'],  # Adjust content types as needed
        'path': '/'.join(context.getPhysicalPath())
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
            relative_path = '/'.join(obj.getPhysicalPath()[2:])  # Get path relative to Plone site
            file_path = os.path.join(base_path, relative_path)
            
            # Debug: print object details
            print(f"Processing object at {relative_path} with ID {obj.getId()} and type {obj.portal_type}.")
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            print(f"Created directories for {os.path.dirname(file_path)}.")
            
            # Write content to file based on type
            content = f"Title: {obj.Title()}\n\nDescription: {obj.Description()}\n\n"
            if obj.portal_type in ['Document', 'News Item']:
                content += f"Text: {obj.getText()}"
            elif obj.portal_type == 'File':
                content += f"File: {obj.getFile().data}"
            
            write_content_to_file(file_path + '.txt', content)
            print(f"Exported: {file_path}.txt")
        
        except Exception as e:
            print(f"Error processing object at {brain.getPath()}: {e}")

def main(app):
    try:
        site = app.Plone
        setSite(site)
        
        # Debug: print site details
        print(f"Connected to Plone site: {site}")
        
        export_base_path = 'export'  # Change this to the desired export directory
        if not os.path.exists(export_base_path):
            os.makedirs(export_base_path)
            print(f"Created export base directory at {export_base_path}.")
        
        traverse_and_export(site, export_base_path)
        transaction.commit()
        print("Export completed.")
    
    except AttributeError:
        print("Error: Could not find the Plone site at app.Plone.")
        print("Make sure the Plone site exists and is correctly referenced.")

if __name__ == '__main__':
    main(app)
