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
            next(reader)
            for row in reader:
                try:
                    quartet = Quartet.objects.get(
                        name=self.c(row[0]),
                    )
                except Quartet.DoesNotExist:
                    print "Could not find quaret {0}".format(row[0])
                    break

                lead, created = Singer.objects.get_or_create(
                    name=self.c(row[1]),
                )
                quartet.lead = lead
                print "Added {0} to {1}, created: {2}".format(
                    lead,
                    quartet,
                    created,
                )

                tenor, created = Singer.objects.get_or_create(
                    name=self.c(row[2]),
                )
                quartet.tenor = tenor
                print "Added {0} to {1}, created: {2}".format(
                    tenor,
                    quartet,
                    created,
                )

                baritone, created = Singer.objects.get_or_create(
                    name=self.c(row[3]),
                )
                quartet.baritone = baritone
                print "Added {0} to {1}, created: {2}".format(
                    baritone,
                    quartet,
                    created,
                )

                bass, created = Singer.objects.get_or_create(
                    name=self.c(row[4]),
                )
                quartet.bass = bass
                print "Added {0} to {1}, created: {2}".format(
                    bass,
                    quartet,
                    created,
                )

                quartet.save()

        return "Done"
