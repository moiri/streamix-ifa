SHELL := /bin/bash

all:
	mkdir -p build/sia
	cp setup.py build/.
	cp sia.py build/sia/__init__.py
	pip install build/.

.PHONY: clean install

install:
	cp check_sia.py /usr/local/bin/smxsia

clean:
	rm -r build
