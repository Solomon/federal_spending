from django.core.management.base import CommandError, BaseCommand
from django.db import connections, transaction
from optparse import make_option
from django.conf import settings
from us_spending.usaspending.scripts.usaspending.config import INDEX_COLS_BY_TABLE


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('-t', '--table',
            action='store',
            dest='table',
            help='Table to create partition for'
        ),
        make_option('-y', '--fiscal-year',
            action='store',
            dest='fiscal_year',
            help='Fiscal year to create partition for'
        ),
    )

    @transaction.commit_on_success
    def handle(self, *args, **kwargs):
        """
        Takes a relation name and a fiscal year and creates a partition for it.
        Current relation names for spending data are:
            usaspending_contract
            usaspending_grant
        """

        fiscal_year = kwargs['fiscal_year']

        if kwargs['table']:
            self.create_partition(fiscal_year, kwargs['table'])
        else:
            if fiscal_year == 'all':
                for fy in settings.FISCAL_YEARS:
                    self.create_partition(fy, 'usaspending_contract')
                    self.create_partition(fy, 'usaspending_grant')
            else:
                raise CommandError("You must specify a table or specify 'all'")

    def create_partition(self, fiscal_year, base_table):
        partition_name = '{}_{}'.format(base_table, fiscal_year)

        create_stmt = """
            create table {} (
                check ( fiscal_year = {} )
            ) inherits ({})
        """.format(partition_name, fiscal_year, base_table)
        print create_stmt

        c = connections['default'].cursor()
        c.execute(create_stmt)
        print "table created"
        
        a = """for i, colname in enumerate(INDEX_COLS_BY_TABLE[base_table]):
            if 'using' in colname or '(' in colname:
                idx_stmt = 'create index {0} on {1} {2}; commit;'.format(
                    partition_name + '_{0}'.format(i),
                    partition_name,
                    colname
                )
            else:
                idx_stmt = 'create index {0} on {1} ({2}); commit;'.format(
                    partition_name + '_{0}'.format(i),
                    partition_name,
                    colname
                )
            c.execute(idx_stmt)"""