# Generated by Django 3.2.4 on 2021-06-11 13:22

import calaccess_processed.proxies
import calaccess_processed_elections.proxies.calaccess_scraped.base
from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("elections", "0008_auto_20181029_1527"),
        ("calaccess_scraped", "0003_auto_20210426_2334"),
        ("calaccess_raw", "0018_auto_20210426_2015"),
        ("core", "0006_merge_20200103_1432"),
    ]

    operations = [
        migrations.CreateModel(
            name="OCDBallotMeasureContestIdentifierProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.ballotmeasurecontestidentifier",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDBallotMeasureContestOptionProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.ballotmeasurecontestoption",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDBallotMeasureContestProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.ballotmeasurecontest",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDBallotMeasureContestSourceProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.ballotmeasurecontestsource",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDCandidacyProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.candidacy",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDCandidacySourceProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.candidacysource",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDCandidateContestPostProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.candidatecontestpost",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDCandidateContestProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.candidatecontest",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDCandidateContestSourceProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.candidatecontestsource",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDDivisionProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.division", calaccess_processed.proxies.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name="OCDElectionIdentifierProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.electionidentifier",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDElectionProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.election",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDElectionSourceProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.electionsource",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDJurisdictionProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.jurisdiction", calaccess_processed.proxies.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name="OCDMembershipProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.membership", calaccess_processed.proxies.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name="OCDOrganizationIdentifierProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "core.organizationidentifier",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDOrganizationNameProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "core.organizationname",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDOrganizationProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.organization", calaccess_processed.proxies.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name="OCDPartyProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.organization", calaccess_processed.proxies.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name="OCDPersonIdentifierProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "core.personidentifier",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDPersonNameProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.personname", calaccess_processed.proxies.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name="OCDPersonProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.person", calaccess_processed.proxies.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name="OCDPostProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("core.post", calaccess_processed.proxies.OCDProxyModelMixin),
        ),
        migrations.CreateModel(
            name="OCDRetentionContestIdentifierProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.retentioncontestidentifier",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDRetentionContestOptionProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.retentioncontestoption",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDRetentionContestProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.retentioncontest",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="OCDRetentionContestSourceProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "elections.retentioncontestsource",
                calaccess_processed.proxies.OCDProxyModelMixin,
            ),
        ),
        migrations.CreateModel(
            name="RawFilerToFilerTypeCdProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("calaccess_raw.filertofilertypecd",),
        ),
        migrations.CreateModel(
            name="ScrapedCandidateElectionProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                calaccess_processed_elections.proxies.calaccess_scraped.base.ScrapedElectionProxyMixin,
                "calaccess_scraped.candidateelection",
            ),
        ),
        migrations.CreateModel(
            name="ScrapedCandidateProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "calaccess_scraped.candidate",
                calaccess_processed_elections.proxies.calaccess_scraped.base.ScrapedNameMixin,
            ),
        ),
        migrations.CreateModel(
            name="ScrapedIncumbentElectionProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                calaccess_processed_elections.proxies.calaccess_scraped.base.ScrapedElectionProxyMixin,
                "calaccess_scraped.incumbentelection",
            ),
        ),
        migrations.CreateModel(
            name="ScrapedIncumbentProxy",
            fields=[],
            options={
                "ordering": ["-session"],
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                "calaccess_scraped.incumbent",
                calaccess_processed_elections.proxies.calaccess_scraped.base.ScrapedNameMixin,
            ),
        ),
        migrations.CreateModel(
            name="ScrapedPropositionElectionProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=(
                calaccess_processed_elections.proxies.calaccess_scraped.base.ScrapedElectionProxyMixin,
                "calaccess_scraped.propositionelection",
            ),
        ),
        migrations.CreateModel(
            name="ScrapedPropositionProxy",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("calaccess_scraped.proposition",),
            managers=[
                ("ballot_measures", django.db.models.manager.Manager()),
            ],
        ),
    ]
