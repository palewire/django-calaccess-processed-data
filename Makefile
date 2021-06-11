.PHONY: docs ship test flake8 settings

docs:
	cd docs && make livehtml

ship:
	rm -rf build/
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/* --skip-existing

test:
	pipenv run coverage run example/manage.py test calaccess_processed
	pipenv run coverage report -m

flake8:
	pipenv run flake8 calaccess_processed --exclude=calaccess_processed/migrations/*
	pipenv run flake8 calaccess_processed_campaignfinance
	pipenv run flake8 calaccess_processed_elections --exclude=calaccess_processed_elections/migrations/*
	pipenv run flake8 calaccess_processed_filings --exclude=calaccess_processed_filings/migrations/*
	pipenv run flake8 calaccess_processed_flatfiles --exclude=calaccess_processed_flatfiles/migrations/*

settings:
	cp example/project/settings_local.py.template example/settings_local.py
