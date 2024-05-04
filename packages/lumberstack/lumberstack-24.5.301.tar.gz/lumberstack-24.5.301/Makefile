.PHONY : build upload-test upload install-test install upgrade-test upgrade update-test update

build:
	python -m build

upload-test:
	twine upload --skip-existing --repository testpypi dist/*

upload:
	twine upload --skip-existing --repository pypi dist/*

install-test:
	pip install --index-url https://test.pypi.org/simple/ --no-deps lumberstack

install:
	pip install lumberstack

upgrade-test:
	pip install -U --index-url https://test.pypi.org/simple/ --no-deps lumberstack

upgrade:
	pip install -U lumberstack

update-test: build upload-test upgrade-test

update: build upload upgrade
