import os
import csv

from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    ChorusPerformance,
    Chorus,
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
                    chorus = Chorus.objects.get(
                        name=unicode(row[0].strip()),
                    )
                except ChorusPerformance.DoesNotExist:
                    print 'Chorus does not exist'
                    break

                try:
                    contest = Contest.objects.get(
                        year=2014,
                    )
                except Exception as e:
                    print "{0}".format(e)

                performance = ChorusPerformance(
                    chorus=chorus,
                    contest=contest,
                    song1=unicode(row[3].strip()),
                    mus1=unicode(row[4].strip()),
                    prs1=unicode(row[5].strip()),
                    sng1=unicode(row[6].strip()),
                    song2=unicode(row[7].strip()),
                    mus2=unicode(row[8].strip()),
                    prs2=unicode(row[9].strip()),
                    sng2=unicode(row[10].strip()),
                )
                performance.save()
                print performance
        return "Complete"
