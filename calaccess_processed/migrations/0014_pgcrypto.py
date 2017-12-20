from __future__ import unicode_literals
from django.db import migrations
from calaccess_processed.postgres import CryptoExtension


class Migration(migrations.Migration):

    dependencies = [
        ('calaccess_processed', '0013_auto_20171114_1957'),
    ]

    operations = [CryptoExtension(),]
