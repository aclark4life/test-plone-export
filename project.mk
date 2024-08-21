PROJECT_NAME := test-plone-export
# PIP_INSTALL_PLONE_CONSTRAINTS = https://dist.plone.org/release/5.1-latest/constraints.txt

test:
	$(MAKE) clean git-commit-clean git-ignore git-commit-ignore plone-install plone-instance
	$(MAKE) git-commit-init

dump:
	.venv/bin/zconsole run backend/etc/zope.conf  export.py
