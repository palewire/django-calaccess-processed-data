# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-22 22:04
from __future__ import unicode_literals

import calaccess_processed.models.proxies.opencivicdata.base
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('elections', '0002_auto_20170731_2047'),
        ('calaccess_processed', '0007_ocdflatcandidacyproxy'),
    ]

    operations = [
        migrations.CreateModel(
            name='OCDFlatBallotMeasureContestProxy',
            fields=[
                ('ballotmeasurecontest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elections.BallotMeasureContest')),
            ],
            options={
                'ordering': ('election', 'name'),
                'abstract': False,
            },
            bases=('elections.ballotmeasurecontest', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name='OCDFlatRetentionContestProxy',
            fields=[
                ('retentioncontest_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='elections.RetentionContest')),
            ],
            options={
                'ordering': ('election', 'name'),
                'abstract': False,
            },
            bases=('elections.retentioncontest', calaccess_processed.models.proxies.opencivicdata.base.OCDProxyModelMixin),
        ),
    ]
