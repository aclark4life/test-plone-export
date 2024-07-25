import os
import transaction
import logging
from ZODB import DB
from ZODB.FileStorage import FileStorage
from zope.component.hooks import setSite
from plone import api

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Path to the Data.fs file
datafs_path = './test_plone_export/var/Data.fs'

# Path where files should be saved
output_dir = 'export'

# Open the Data.fs
try:
    storage = FileStorage(datafs_path)
    db = DB(storage)
    connection = db.open()
    root = connection.root()
    logging.info("Database opened successfully")
except Exception as e:
    logging.error(f"Failed to open the database: {e}")
    raise

# Access the Plone site object
try:
    app = root['Application']
    site = app['Plone']  # Replace 'Plone' with your site ID if different
    setSite(site)
    logging.info("Plone site accessed successfully")
except KeyError as e:
    logging.error(f"Failed to access Plone site: {e}")
    raise

# Function to save file to the file system
def save_file(file_obj, file_name, output_dir):
    try:
        with open(os.path.join(output_dir, file_name), 'wb') as f:
            f.write(file_obj.data)
        logging.info(f"Saved file: {file_name}")
    except Exception as e:
        logging.error(f"Failed to save file {file_name}: {e}")

# Recursively find and save all File content type objects
def extract_files(obj, output_dir):
    for item_id, item in obj.objectItems():
        if item.portal_type == 'File':
            try:
                file_obj = item.getField('file').get(item)
                file_name = item.getId()
                save_file(file_obj, file_name, output_dir)
            except Exception as e:
                logging.error(f"Error processing file {item_id}: {e}")
        elif hasattr(item, 'objectItems'):
            extract_files(item, output_dir)

# Create output directory if it doesn't exist
try:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    logging.info(f"Output directory {output_dir} created")
except Exception as e:
    logging.error(f"Failed to create output directory: {e}")
    raise

# Extract files from the site
try:
    extract_files(site, output_dir)
    logging.info("File extraction completed")
except Exception as e:
    logging.error(f"Error during file extraction: {e}")

# Commit the transaction and close the connection
try:
    transaction.commit()
    logging.info("Transaction committed")
except Exception as e:
    logging.error(f"Failed to commit transaction: {e}")

try:
    connection.close()
    db.close()
    logging.info("Database connection closed")
except Exception as e:
    logging.error(f"Failed to close database connection: {e}")
