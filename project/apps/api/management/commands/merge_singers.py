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

        # Move performers
        performers_tenor = old_singer.performers_tenor.all()
        performers_lead = old_singer.performers_lead.all()
        performers_baritone = old_singer.performers_baritone.all()
        performers_bass = old_singer.performers_bass.all()
        if not bool(performers_tenor or performers_lead or performers_baritone or performers_bass):
            return 'No contesants to move.'

        if performers_tenor:
            for performer in performers_tenor:
                performer.singer = new_singer
                try:
                    performer.save()
                except IntegrityError:
                    raise CommandError(
                        "Performer {0} already exists.  Merge manually".format(performer)
                    )

        if performers_lead:
            for performer in performers_lead:
                performer.singer = new_singer
                try:
                    performer.save()
                except IntegrityError:
                    raise CommandError(
                        "Performer {0} already exists.  Merge manually".format(performer)
                    )

        if performers_baritone:
            for performer in performers_baritone:
                performer.singer = new_singer
                try:
                    performer.save()
                except IntegrityError:
                    raise CommandError(
                        "Performer {0} already exists.  Merge manually".format(performer)
                    )

        if performers_bass:
            for performer in performers_bass:
                performer.singer = new_singer
                try:
                    performer.save()
                except IntegrityError:
                    raise CommandError(
                        "Performer {0} already exists.  Merge manually".format(performer)
                    )

        # remove redundant singer
        try:
            old_singer.delete()
        except Exception as e:
            raise CommandError("Error deleted old singer: {0}".format(e))

        return "Merged {0} into {1}".format(old_singer, new_singer)
