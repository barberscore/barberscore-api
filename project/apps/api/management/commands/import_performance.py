import os
import csv
from unidecode import unidecode

from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    Chorus,
    Contest,
    Appearance,
)


class Command(BaseCommand):
    help = "Command to import contestants"
    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--file",
            dest="filename",
            help="specify import file",
            metavar="FILE"
        ),
    )

    def c(self, input):
        return unidecode(input.strip())

    def handle(self, *args, **options):
        # make sure file option is present
        if options['filename'] is None:
            raise CommandError("Option `--file=...` must be specified.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']):
            raise CommandError("File does not exist at the specified path.")

        # print file
        print "Path: `%s`" % options['filename']

        # open the file
        with open(options['filename']) as csv_file:
            reader = csv.reader(csv_file)
            contest = Contest.objects.get(
                year=2015,
                kind=Contest.CHORUS,
                district__name='BHS',
            )
            # next(reader)
            for row in reader:
                try:
                    chorus = Chorus.objects.get(
                        name=self.c(row[1]),
                    )
                except Chorus.DoesNotExist:
                    print('Error importing {0}'.format(row[1]))
                    continue
                gf = Appearance.objects.create(
                    seed=row[0],
                    group=chorus,
                    contest=contest,
                    prelim=row[5],
                )
                print "{0}".format(gf)
        return "Done"
