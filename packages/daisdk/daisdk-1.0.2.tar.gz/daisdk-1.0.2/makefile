include public/build/build.mk
SHELL := /bin/bash

sdk:
	python3 setup.py sdist bdist_wheel

sdk-nuitka:
	python3 setup.py bdist_nuitka

clean:
	rm -rf build dist daisdk.egg-info
