
.PHONY: bootstrap docs rs runserver shell sh test

bootstrap:
	createdb calaccess_processed -U postgres
	psql -c 'CREATE EXTENSION IF NOT EXISTS pgcrypto;' -U postgres
	python example/manage.py migrate
	python example/manage.py runserver

docs:
	cd docs && make livehtml

rs:
	python example/manage.py runserver

runserver:
	python example/manage.py runserver

sh:
	python example/manage.py shell

shell:
	python example/manage.py shell

ship:
	rm -rf build/
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing

test:
	flake8 calaccess_processed
	coverage run example/manage.py test calaccess_processed
	coverage report -m
