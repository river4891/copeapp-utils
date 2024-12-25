.PHONY: clean build publish
	
build: clean # build package.
	echo 'build packages...'
	# python -m pip install --upgrade --quiet pip setuptools wheel twine
	# pip install -U .

tests/%.o: tests/%.py
	echo "$^ --> $@"
	rm -rf build dist  *.egg-info src/*.egg-info

publish: build # publish package to pypi.org
	python -m twine check dist/*
	python -m twine upload dist/*

clean: # clean build temp files.
	rm -rf build dist  *.egg-info src/*.egg-info
