import os
import csv

from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    District,
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
            for row in reader:

                try:
                    district, created = District.objects.get_or_create(
                        name=unicode(row[0].strip()),
                        abbreviation=unicode(row[1].strip()),
                        kind=unicode(row[2].strip()),
                    )

                except Exception as e:
                    print "District `%s` could not be created." % row[0]
                    print "Exception: {0} ".format(e)
                    break
