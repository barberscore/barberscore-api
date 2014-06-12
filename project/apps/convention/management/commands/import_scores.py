import os
import csv

from optparse import make_option

from django.utils.text import slugify

from django.core.management.base import BaseCommand, CommandError

from apps.convention.models import Score, Contestant, Contest


class Command(BaseCommand):
    help = "Command to import a list of stuff"
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
            reader = csv.reader(csv_file, delimiter='\t')
            for row in reader:

                try:
                    contestant, created = Contestant.objects.get_or_create(
                        name=unicode(row[0].strip()),
                        defaults={
                            'slug': slugify(
                                unicode(
                                    row[0].strip()
                                )
                            ),
                            'contestant_type': 2
                        }
                    )

                except Exception, e:
                    print "Contestant `%s` could not be created." % row[0]
                    print "Exception: {0} created {1}".format(e, created)
                    break
