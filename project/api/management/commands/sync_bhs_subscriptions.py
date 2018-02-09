import django_rq

# Django
from django.core.management.base import BaseCommand

# First-Party
from api.models import Person
from bhs.models import Subscription


class Command(BaseCommand):
    help = "Command to sync persons and humans."

    def handle(self, *args, **options):
        self.stdout.write("Updating persons and subscriptions...")

        subscriptions = Subscription.objects.filter(
            items_editable=True,
        )
        i = 0
        t = subscriptions.count()
        for subscription in subscriptions:
            i += 1
            django_rq.enqueue(
                Person.objects.update_status_from_subscription,
                subscription,
            )
            self.stdout.flush()
            self.stdout.write("Queuing {0}/{1} subscriptions...".format(i, t), ending='\r')
        self.stdout.write("Queued {0} subscriptions.".format(t))
