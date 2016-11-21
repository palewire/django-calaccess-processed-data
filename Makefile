
.PHONY: docs rs runserver shell sh test

docs:
	cd docs && make livehtml

rs:
	python example/manage.py runserver

runserver:
	python example/manage.py runserver

shell:
	python example/manage.py shell

sh:
	python example/manage.py shell

test:
	flake8 calaccess_raw
	coverage run example/manage.py test calaccess_processed
	coverage report -m
