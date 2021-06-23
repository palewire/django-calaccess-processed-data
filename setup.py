#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from distutils.core import Command


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            INSTALLED_APPS=('calaccess_processed',),
            MIDDLEWARE_CLASSES=()
        )
        from django.core.management import call_command
        import django
        django.setup()
        call_command('test', 'calaccess_processed')


setup(
    name='django-calaccess-processed-data',
    version='0.4.2',
    license='MIT',
    description='A Django app to transform and refine campaign finance data from the California Secretary of State’s \
CAL-ACCESS database',
    long_description=read('README.rst'),
    url='http://django-calaccess.californiacivicdata.org',
    author='California Civic Data Coalition',
    author_email='b@palewi.re',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # because we're including static files
    install_requires=(
        'django-calaccess-raw-data==4.0.0',
        'django-calaccess-scraped-data==3.1.0',
        'django>=3.2.*',
        'ccdc-opencivicdata==0.0.1',
        'django-internetarchive-storage',
        'pytz',
    ),
    cmdclass={'test': TestCommand,},
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'License :: OSI Approved :: MIT License',
    ),
)
