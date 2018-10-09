.PHONY: docs ship test flake8 settings

docs:
	cd docs && make livehtml

ship:
	rm -rf build/
	python setup.py sdist bdist_wheel
	twine upload dist/* --skip-existing

test:
	coverage manage.py test calaccess_processed
	coverage report -m

flake8:
	flake8 calaccess_processed --exclude=calaccess_processed/migrations/*
	flake8 calaccess_processed_campaignfinance
	flake8 calaccess_processed_elections
	flake8 calaccess_processed_filings --exclude=calaccess_processed_filings/migrations/*
	flake8 calaccess_processed_flatfiles

settings:
	cp example/project/settings_local.py.template example/settings_local.py
