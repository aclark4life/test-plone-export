PROJECT_NAME := test_plone_export

serve:
	$(MAKE) plone-serve

.PHONY: export
export:
	python export.py
