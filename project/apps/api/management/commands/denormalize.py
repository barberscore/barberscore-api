from django.core.management.base import (
    BaseCommand,
)

from apps.api.models import (
    Award,
    Certification,
    Chapter,
    Chart,
    Contest,
    Contestant,
    Convention,
    Group,
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
    Song,
    Submission,
    Venue,
)


class Command(BaseCommand):
    help = "Command to denormalize names."

    def handle(self, *args, **options):
        # Primitives
        [i.save() for i in Award.objects.all()]
        [i.save() for i in Chapter.objects.all()]
        [i.save() for i in Chart.objects.all()]
        [i.save() for i in Convention.objects.all()]
        [i.save() for i in Group.objects.all()]
        [i.save() for i in Organization.objects.all()]
        [i.save() for i in Person.objects.all()]
        [i.save() for i in Venue.objects.all()]
        # Branches
        [i.save() for i in Session.objects.all()]
        [i.save() for i in Certification.objects.all()]
        [i.save() for i in Judge.objects.all()]
        [i.save() for i in Member.objects.all()]
        [i.save() for i in Role.objects.all()]
        [i.save() for i in Round.objects.all()]
        [i.save() for i in Contest.objects.all()]
        [i.save() for i in Performer.objects.all()]
        [i.save() for i in Contestant.objects.all()]
        [i.save() for i in Performance.objects.all()]
        [i.save() for i in Submission.objects.all()]
        [i.save() for i in Song.objects.all()]
        [i.save() for i in Score.objects.all()]
        return "Done"
