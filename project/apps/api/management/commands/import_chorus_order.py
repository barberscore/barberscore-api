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
    ChorusPerformance,
    Contest,
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
                level=Contest.INTERNATIONAL,
            )
            # next(reader)
            for row in reader:
                chorus, created = Chorus.objects.get_or_create(
                    name=self.c(row[0]),
                )
                cp = ChorusPerformance.objects.create(
                    chorus=chorus,
                    contest=contest,
                    queue=row[1],
                )
                print "{0}".format(cp)
        return "Done"
