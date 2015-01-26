import os
import csv
from unidecode import unidecode

from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    Singer,
    Quartet,
    QuartetMembership,
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
                        old_id=self.c(row[0]),
                    )
                except Quartet.DoesNotExist:
                    print "Could not find quaret {0}".format(row[0])
                    break
                lead, created = Singer.objects.get_or_create(
                    name=self.c(row[4]),
                )
                tenor, created = Singer.objects.get_or_create(
                    name=self.c(row[2]),
                )
                baritone, created = Singer.objects.get_or_create(
                    name=self.c(row[6]),
                )
                bass, created = Singer.objects.get_or_create(
                    name=self.c(row[13]),
                )
                QuartetMembership.objects.create(
                    singer=lead,
                    quartet=quartet,
                    contest=contest,
                    part=QuartetMembership.LEAD,
                )
                print "Added {0} to {1}".format(lead, quartet)
                QuartetMembership.objects.create(
                    singer=tenor,
                    quartet=quartet,
                    contest=contest,
                    part=QuartetMembership.TENOR,
                )
                print "Added {0} to {1}".format(tenor, quartet)
                QuartetMembership.objects.create(
                    singer=baritone,
                    quartet=quartet,
                    contest=contest,
                    part=QuartetMembership.BARITONE,
                )
                print "Added {0} to {1}".format(baritone, quartet)
                QuartetMembership.objects.create(
                    singer=bass,
                    quartet=quartet,
                    contest=contest,
                    part=QuartetMembership.BASS,
                )
                print "Added {0} to {1}".format(bass, quartet)
        return "Done"
