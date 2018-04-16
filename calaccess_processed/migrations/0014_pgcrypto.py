from __future__ import unicode_literals
from django.db import migrations
from calaccess_processed.postgres import CryptoExtension


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_processed', '0001_squashed_0014_rawfilertofilertypecdproxy_scrapedcandidateelectionproxy_scrapedcandidateproxy_scrapedincumbentelect'),
    ]

    operations = [CryptoExtension(),]
