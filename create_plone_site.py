from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest
from zope.component.hooks import setSite
from Products.CMFPlone.factory import addPloneSite
from Products.CMFPlone.utils import get_installer

# Assume 'app' is the Zope application server root
app = makerequest(app)

# Set the admin user as the current user
user_id = 'admin'  # Replace with your actual admin user ID
user = app.acl_users.getUserById(user_id)
if not user:
    raise ValueError(f"User '{user_id}' not found")

newSecurityManager(None, user)

# Create the Plone site
site_id = 'MyPloneSite'
site_title = 'My Plone Site'
language = 'en'

# Check if the site already exists
if site_id not in app.objectIds():
    addPloneSite(
        app,
        site_id,
        title=site_title,
        extension_ids=('plonetheme.classic:default',),  # Add your theme and other profiles
        setup_content=True,
        default_language=language,
    )

# Get the created site
site = app[site_id]

# Set the site context
setSite(site)

# Install additional products or themes
installer = get_installer(site)
installer.install_product('plonetheme.classic')

# Commit the transaction to save changes
import transaction
transaction.commit()

# Now your Plone site is created programmatically with a classic theme.
