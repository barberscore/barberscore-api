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
                    chorus = Chorus.objects.get(
                        name=self.c(row[12]),
                    )
                except Chorus.DoesNotExist:
                    print "Chorus {0} could not be updated.".format(
                        row[0],
                    )
                    break
                chorus.facebook = self.c(row[3])
                chorus.phone = self.c(row[5])
                chorus.location = self.c(row[9])
                chorus.email = self.c(row[10])
                chorus.name = self.c(row[12])
                chorus.twitter = self.c(row[20])
                chorus.website = self.c(row[21])
                chorus.blurb = self.c(row[22])
                chorus.save()
                print chorus
        return "Done"
