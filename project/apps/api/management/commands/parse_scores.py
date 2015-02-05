import os
from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.utils import (
    parse_quarters,
    parse_semis,
    parse_finals,
)


class Command(BaseCommand):
    help = "De-duplication command"
    option_list = BaseCommand.option_list + (
        make_option(
            "-r",
            "--round",
            dest="round",
            help="specify round",
        ),
    )
    option_list = option_list + (
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
        if options['round'] is None:
            raise CommandError("Option `--round=...` must be specified.")

        if options['filename'] is None:
            raise CommandError("Option `--file=...` must be specified.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']):
            raise CommandError("File does not exist at the specified path.")

        # print file
        print "Path: `%s`" % options['filename']

        # open the file
        if options['round'] == 'q':
            parse_quarters(options['filename'])

        elif options['round'] == 's':
            parse_semis(options['filename'])

        elif options['round'] == 'f':
            parse_finals(options['filename'])

        else:
            raise CommandError("Round mis-specified")

        return "Done"
