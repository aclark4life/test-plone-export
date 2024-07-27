PROJECT_NAME := test-plone-export

serve:
	$(MAKE) plone-serve

.PHONY: export
export:
	echo $(PACKAGE_NAME)
	python export.py
