import os
import transaction
from ZODB import DB
from ZODB.FileStorage import FileStorage
from plone import api

# Path to the Data.fs file
datafs_path = './test_plone_export/var/Data.fs'

# Path where files should be saved
output_dir = 'export'

# Open the Data.fs
storage = FileStorage(datafs_path)
db = DB(storage)
connection = db.open()
root = connection.root()

# Access the Plone site object
app = root['Application']
site = app['Plone']  # Replace 'Plone' with your site ID if different

# Function to save file to the file system
def save_file(file_obj, file_name, output_dir):
    with open(os.path.join(output_dir, file_name), 'wb') as f:
        f.write(file_obj.data)

# Recursively find and save all File content type objects
def extract_files(obj, output_dir):
    for item_id, item in obj.objectItems():
        if item.portal_type == 'File':
            file_obj = item.getField('file').get(item)
            file_name = item.getId()
            save_file(file_obj, file_name, output_dir)
        elif hasattr(item, 'objectItems'):
            extract_files(item, output_dir)

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Extract files from the site
extract_files(site, output_dir)

# Commit the transaction and close the connection
transaction.commit()
connection.close()
db.close()
