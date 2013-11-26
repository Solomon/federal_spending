from federal_spending.usaspending.models import Grant
from federal_spending.usaspending.scripts.usaspending.grants_loader import Loader
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):

    @transaction.commit_on_success
    def handle(self, grant_path, **options):
        #print "Current number of rows in grant table: {0}".format(Grant.objects.all().count())
        
        Loader().insert_faads(grant_path)
        #transaction.set_dirty()

        #print "New number of rows in grant table: {0}".format(Grant.objects.all().count())