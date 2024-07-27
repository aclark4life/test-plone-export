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
    results = catalog.unrestrictedSearchResults()
    
    print(f"Found {len(results)} content objects to export.")
    
    for brain in results:
        obj = brain.getObject()
        relative_path = '/'.join(obj.getPhysicalPath()[2:])  # Get path relative to Plone site
        file_path = os.path.join(base_path, relative_path)
        
        print(f"Processing object at {relative_path} with ID {obj.getId()} and type {obj.portal_type}.")
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        print(f"Created directories for {os.path.dirname(file_path)}.")
        
        # Write content to file
        content = f"Title: {obj.Title()}\n\nDescription: {obj.Description()}\n\nText: {obj.getText()}"
        write_content_to_file(file_path + '.txt', content)
        print(f"Exported: {file_path}.txt")

def main(app):
    site = app.Plone
    setSite(site)
    
    export_base_path = 'export'  # Change this to the desired export directory
    if not os.path.exists(export_base_path):
        os.makedirs(export_base_path)
        print(f"Created export base directory at {export_base_path}.")
    
    traverse_and_export(site, export_base_path)
    transaction.commit()
    print("Export completed.")

if __name__ == '__main__':
    main(app)
