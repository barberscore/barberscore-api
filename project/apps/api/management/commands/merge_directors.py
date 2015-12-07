from optparse import make_option

from django.db import IntegrityError

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    Director,
)


class Command(BaseCommand):
    help = "Merge selected directors by name"
    option_list = BaseCommand.option_list + (
        make_option(
            "-o",
            "--old",
            dest="old",
            help="specify old name",
        ),
    )
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

        # make sure both directors exist
        try:
            new_director = Director.objects.get(
                name__iexact=options['new'],
            )
        except Director.DoesNotExist:
            raise CommandError("Target director does not exist.")
        try:
            old_director = Director.objects.get(
                name__iexact=options['old'],
            )
        except Director.DoesNotExist:
            raise CommandError("Subject director does not exist.")

        # perform de-dup
        performers = old_director.performers.all()
        if not performers:
            old_director.delete()
            return 'No contesants to move.'

        for performer in performers:
            performer.director = new_director
            try:
                performer.save()
            except IntegrityError:
                raise CommandError(
                    "Performer {0} already exists.  Merge manually".format(performer)
                )

        # remove redundant director
        try:
            old_director.delete()
        except Exception as e:
            raise CommandError("Error deleted old director: {0}".format(e))

        return "Merged {0} into {1}".format(old_director, new_director)
