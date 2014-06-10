import os
import csv

from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.bbs.models import (
    Contestant,
    Performance,
    Contest,
)


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
            reader = csv.reader(csv_file)
            for row in reader:

                try:
                    contest = Contest.objects.get(contest_type=Contest.CHORUS)
                    contestant = Contestant.objects.get(
                        name=unicode(row[1].strip())
                    )
                    performance, created = Performance.objects.get_or_create(
                        contestant=contestant,
                        contest=contest,
                        contest_round=3,
                        appearance=int(row[0]),
                    )
                    performance.save()
                    print "Contestant {0} saved.".format(contestant.name)
                except Exception, e:
                    print "Contestant `%s` could not be created." % row[1]
                    print "Exception: {0} ".format(e)
                    continue
