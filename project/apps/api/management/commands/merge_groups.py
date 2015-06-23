from optparse import make_option

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    Group,
)


class Command(BaseCommand):
    help = "Merge selected gorups"
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

        # make sure both groups exist
        try:
            new_group = Group.objects.get(pk=options['new'])
        except Group.DoesNotExist:
            raise CommandError("Target group does not exist.")
        try:
            old_group = Group.objects.get(pk=options['old'])
        except Group.DoesNotExist:
            raise CommandError("Subject group does not exist.")

        # perform de-dup
        try:
            contestants = old_group.contestants.all()
            for contestant in contestants:
                contestant.group = new_group
                contestant.save()
        except Exception as e:
            raise CommandError("Error moving contestants: {0}".format(e))

        # remove redundant group
        try:
            old_group.delete()
        except Exception as e:
            raise CommandError("Error deleted old group: {0}".format(e))

        return "Merged {0} into {1}".format(old_group, new_group)
