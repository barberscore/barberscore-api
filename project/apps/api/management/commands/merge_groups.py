from optparse import make_option

from django.db import IntegrityError

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    Group,
)


class Command(BaseCommand):
    help = "Merge selected groups by name"
    option_list = option_list + (
        make_option(
            "-n",
            "--new",
            dest="new",
            help="specify new name",
        ),
    )

    def handle(self, *args, **options):
        # make sure file option is present
        if options['old'] is None:
            raise CommandError("Option `--old=...` must be specified.")

        if options['new'] is None:
            raise CommandError("Option `--new=...` must be specified.")

        # make sure both groups exist
        try:
            new_group = Group.objects.get(
                name__iexact=options['new'],
            )
        except Group.DoesNotExist:
            raise CommandError("Target group does not exist.")
        try:
            old_group = Group.objects.get(
                name__iexact=options['old'],
            )
        except Group.DoesNotExist:
            raise CommandError("Subject group does not exist.")

        # perform de-dup
        performers = old_group.performers.all()
        if not performers:
            old_group.delete()
            return 'No contesants to move.'

        for performer in performers:
            performer.group = new_group
            try:
                performer.save()
            except IntegrityError:
                raise CommandError(
                    "Performer {0} already exists.  Merge manually".format(performer)
                )

        # remove redundant group
        try:
            old_group.delete()
        except Exception as e:
            raise CommandError("Error deleted old group: {0}".format(e))

        return "Merged {0} into {1}".format(old_group, new_group)
