# Django
from django.core.management.base import BaseCommand
from django.apps import apps as api_apps


# First-Party
from app.models import (
    Assignment,
    Award,
    Catalog,
    Chapter,
    Contest,
    Contestant,
    Convention,
    Group,
    Host,
    Judge,
    Member,
    Organization,
    Performance,
    Performer,
    Person,
    Role,
    Round,
    Score,
    Session,
    Slot,
    Song,
    Submission,
    Venue,
)


class Command(BaseCommand):
    help = "Command to build nomens."

    def handle(self, *args, **options):
        config = api_apps.get_app_config('app')
        primitives = [
            'Award',
            'Catalog',
            'Chapter',
            'Group',
            'Organization',
            'Person',
            'Venue',
        ]

        for primitive in primitives:
            model = config.get_model(primitive)
            for i in model.objects.all():
                i.calculate_nomen()
                i.save()

        # [i.calculate_nomen() for i in Award.objects.all()]
        # [i.calculate_nomen() for i in Catalog.objects.all()]
        # [i.calculate_nomen() for i in Chapter.objects.all()]
        # [i.calculate_nomen() for i in Group.objects.all()]
        # [i.calculate_nomen() for i in Organization.objects.all()]
        # [i.calculate_nomen() for i in Person.objects.all()]
        # [i.calculate_nomen() for i in Venue.objects.all()]
        # # Branches
        # [i.calculate_nomen() for i in Convention.objects.all()]
        # [i.calculate_nomen() for i in Host.objects.all()]
        # [i.calculate_nomen() for i in Session.objects.all()]
        # [i.calculate_nomen() for i in Judge.objects.all()]
        # [i.calculate_nomen() for i in Assignment.objects.all()]
        # [i.calculate_nomen() for i in Member.objects.all()]
        # [i.calculate_nomen() for i in Role.objects.all()]
        # [i.calculate_nomen() for i in Round.objects.all()]
        # [i.calculate_nomen() for i in Contest.objects.all()]
        # [i.calculate_nomen() for i in Performer.objects.all()]
        # [i.calculate_nomen() for i in Slot.objects.all()]
        # [i.calculate_nomen() for i in Submission.objects.all()]
        # [i.calculate_nomen() for i in Contestant.objects.all()]
        # [i.calculate_nomen() for i in Performance.objects.all()]
        # [i.calculate_nomen() for i in Song.objects.all()]
        # [i.calculate_nomen() for i in Score.objects.all()]
        return "Rebuilt nomens."
