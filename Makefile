.PHONY: default, lint

default:
	python -m HoundSploitBash
lint:
	pylint HoundSploitBash
pep8:
	autopep8 HoundSploitBash --in-place --recursive --aggressive --aggressive
