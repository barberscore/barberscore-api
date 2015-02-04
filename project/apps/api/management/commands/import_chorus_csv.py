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
                    chorus = Chorus.objects.get_or_create(
                        id=self.c(row[0]),
                        name=self.c(row[1]),
                        location=self.c(row[3]),
                        website=self.c(row[4]),
                        facebook=self.c(row[5]),
                        twitter=self.c(row[6]),
                        email=self.c(row[7]),
                        phone=self.c(row[8]),
                        director=self.c(row[9]),
                        description=self.c(row[12]),
                        chapter_code=self.c(row[13]),
                        chapter_name=self.c(row[14]),
                        district_id=self.c(row[15]),
                    )
                    print chorus
                except Exception as e:
                    print "Chorus {0} could not be created.".format(
                        row[0],
                    )
                    print "Exception: {0} ".format(e)
        return "Done"
