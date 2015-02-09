from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    Group,
    Performance,
)


class Command(BaseCommand):
    help = "De-duplication command"
    option_list = BaseCommand.option_list + (
        make_option(
            "-o",
            "--old",
            dest="old",
            help="specify old pk",
        ),
    )
    option_list = option_list + (
        make_option(
            "-n",
            "--new",
            dest="new",
            help="specify new pk",
        ),
    )

    def handle(self, *args, **options):
        # make sure file option is present
        if options['old'] is None:
            raise CommandError("Option `--old=...` must be specified.")

        if options['new'] is None:
            raise CommandError("Option `--new=...` must be specified.")

        # make sure target (new) exists
        try:
            new_group = Group.objects.get(pk=options['new'])
        except Group.DoesNotExist:
            raise CommandError("Target chorus does not exist.")

        try:
            performances = Performance.objects.filter(
                group__pk=options['old'],
            )
        except Performance.DoesNotExist:
            raise CommandError("No performances to migrate.")

        # perform de-dup
        for performance in performances:
            performance.group = new_group
            performance.save()

        # do same for awards, etc?

        return "Done"
