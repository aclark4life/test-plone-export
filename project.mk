# Custom Makefile
# Add your custom makefile commands here
#
PROJECT_NAME := test-plone-export
# PIP_INSTALL_PLONE_CONSTRAINTS = https://dist.plone.org/release/5.1-latest/constraints.txt

test:
	$(MAKE) clean git-commit-clean git-ignore git-commit-ignore plone-install plone-instance
	$(MAKE) git-commit-init
	.venv/bin/zconsole run backend/etc/zope.conf create_plone_site.py classic
	$(MAKE) dump

dump:
	.venv/bin/zconsole run backend/etc/zope.conf  export.py

d:
	$(MAKE) dump

create-plone-site:
	.venv/bin/zconsole run backend/etc/zope.conf create_plone_site.py classic

serve:
	$(MAKE) plone-serve


init:
	$(MAKE) git-commit-clean git-ignore git-commit-ignore plone-install plone-instance
