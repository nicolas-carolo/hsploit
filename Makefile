.PHONY: default, lint

default:
	python -m hsploit
lint:
	pylint hsploit
pep8:
	autopep8 hsploit --in-place --recursive --aggressive --aggressive
