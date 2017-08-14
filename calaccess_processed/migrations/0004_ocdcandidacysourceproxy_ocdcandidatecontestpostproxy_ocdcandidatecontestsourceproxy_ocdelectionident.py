# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-14 17:06
from __future__ import unicode_literals

import calaccess_processed.models.proxies.opencivicdata.base
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0002_auto_20170731_2047'),
        ('calaccess_processed', '0003_auto_20170811_2020'),
    ]

    operations = [
        migrations.CreateModel(
            name='OCDCandidacySourceProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('elections.candidacysource', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name='OCDCandidateContestPostProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('elections.candidatecontestpost', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name='OCDCandidateContestSourceProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('elections.candidatecontestsource', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name='OCDElectionIdentifierProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('elections.electionidentifier', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name='OCDElectionSourceProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('elections.electionsource', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
    ]
