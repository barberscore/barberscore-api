import os
import csv
from unidecode import unidecode

from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    Contest,
    Quartet,
    QuartetPerformance,
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
            contest = Contest.objects.get(
                year=2014,
                level=Contest.INTERNATIONAL,
                kind=Contest.QUARTET,
            )
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                try:
                    quartet = Quartet.objects.get(
                        name=self.c(row[0]),
                    )
                except Quartet.DoesNotExist:
                    print "Could not find Quartet {0}".format(row[0])
                    break
                performance = QuartetPerformance(
                    quartet=quartet,
                    contest=contest,
                    round=self.c(row[9]),
                    song1=self.c(row[1]),
                    mus1=self.c(row[2]),
                    prs1=self.c(row[3]),
                    sng1=self.c(row[4]),
                    song2=self.c(row[5]),
                    mus2=self.c(row[6]),
                    prs2=self.c(row[7]),
                    sng2=self.c(row[8]),
                )
                performance.save()
                print "Performance created"

        return "Done"
