release:
	@rm -rf dist/
	@rm -rf build/
	@python setup.py sdist
	@twine upload dist/*
