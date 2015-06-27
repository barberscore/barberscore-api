from optparse import make_option

from django.db import IntegrityError

from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from apps.api.models import (
    Singer,
)


class Command(BaseCommand):
    help = "Merge selected singers by name"
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

        # make sure both singers exist
        try:
            new_singer = Singer.objects.get(
                name__iexact=options['new'],
            )
        except Singer.DoesNotExist:
            raise CommandError("New singer does not exist.")
        try:
            old_singer = Singer.objects.get(
                name__iexact=options['old'],
            )
        except Singer.DoesNotExist:
            raise CommandError("Old singer does not exist.")

        # Move contestants
        contestants_tenor = old_singer.contestants_tenor.all()
        contestants_lead = old_singer.contestants_lead.all()
        contestants_baritone = old_singer.contestants_baritone.all()
        contestants_bass = old_singer.contestants_bass.all()
        if not bool(contestants_tenor or contestants_lead or contestants_baritone or contestants_bass):
            return 'No contesants to move.'

        if contestants_tenor:
            for contestant in contestants_tenor:
                contestant.singer = new_singer
                try:
                    contestant.save()
                except IntegrityError:
                    raise CommandError(
                        "Contestant {0} already exists.  Merge manually".format(contestant)
                    )

        if contestants_lead:
            for contestant in contestants_lead:
                contestant.singer = new_singer
                try:
                    contestant.save()
                except IntegrityError:
                    raise CommandError(
                        "Contestant {0} already exists.  Merge manually".format(contestant)
                    )

        if contestants_baritone:
            for contestant in contestants_baritone:
                contestant.singer = new_singer
                try:
                    contestant.save()
                except IntegrityError:
                    raise CommandError(
                        "Contestant {0} already exists.  Merge manually".format(contestant)
                    )

        if contestants_bass:
            for contestant in contestants_bass:
                contestant.singer = new_singer
                try:
                    contestant.save()
                except IntegrityError:
                    raise CommandError(
                        "Contestant {0} already exists.  Merge manually".format(contestant)
                    )

        # remove redundant singer
        try:
            old_singer.delete()
        except Exception as e:
            raise CommandError("Error deleted old singer: {0}".format(e))

        return "Merged {0} into {1}".format(old_singer, new_singer)
