import os
import csv
from unidecode import unidecode

from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    GroupMember,
    Contest,
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
                    contest = Contest.objects.get(pk=row[2])
                    quartet = Quartet.objects.get(pk=row[3])
                    singer = Singer.objects.get(pk=row[4])
                    gm = GroupMember.objects.create(
                        part=row[1],
                        contest=contest,
                        group=quartet,
                        singer=singer,
                    )
                    print gm
                except Exception as e:
                    print "GM {0} could not be created.".format(
                        row[0],
                    )
                    print "Exception: {0} ".format(e)
        return "Done"
