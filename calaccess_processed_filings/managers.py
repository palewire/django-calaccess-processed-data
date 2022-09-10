"""Custom manager for loading raw data in to "filings" models."""
import itertools

from django.db.models import Q
from django.db import connection

from calaccess_processed.managers import BulkLoadSQLManager


class FilingsManager(BulkLoadSQLManager):
    """
    Utilities for more quickly loading bulk data.
    """

    app_name = "calaccess_processed_filings"

    def get_sql(self):
        """
        Return string of raw sql for loading the model.
        """
        with open(self.sql_path, "r") as fp:
            sql = fp.read()
        return sql

    @property
    def sql_path(self):
        """
        Return the path to the .sql file with the model's loading query.
        """
        file_name = f"load_{self.model._meta.model_name}_model"
        return self.get_sql_path(file_name)

    def load(self):
        """
        Load the model by executing its corresponding raw SQL query.

        Temporarily drops any constraints or indexes on the model.
        """
        # Drop constraints and indexes to speed loading
        self.get_queryset().drop_constraints()
        self.get_queryset().drop_indexes()

        # Run the actual loader SQL
        with connection.cursor() as c:
            c.execute(self.get_sql())

        # Restore the constraints and index that were dropped
        self.get_queryset().restore_constraints()
        self.get_queryset().restore_indexes()


class Form501FilingManager(FilingsManager):
    """
    A custom manager for Form 501 filings.
    """

    def without_candidacy(self):
        """
        Returns Form 501 filings that do not have an OCD Candidacy yet.
        """
        from calaccess_processed_elections.proxies import OCDCandidacyProxy

        matched_qs = OCDCandidacyProxy.objects.matched_form501_ids()
        matched_list = [i for i in itertools.chain.from_iterable(matched_qs)]
        return self.get_queryset().exclude(
            Q(filing_id__in=matched_list) | Q(office__icontains="RETIREMENT")
        )
