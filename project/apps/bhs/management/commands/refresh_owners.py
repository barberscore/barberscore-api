# Django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

# Local
from apps.bhs.owners import get_owner_users
from apps.bhs.owners import remove_user_from_owners
from apps.bhs.owners import sync_owners


class Command(BaseCommand):
    help = (
        "Refresh the owners of in-progress Conventions, Sessions, and "
        "Rounds from the dynamic staff owner list "
        "(settings.CONVENTION_OWNERS / settings.SESSION_OWNERS).  "
        "Strictly additive: owners added ad hoc are never touched.  To "
        "strip a specific former owner from in-progress objects, pass "
        "--remove with their email address."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--remove',
            action='append',
            default=[],
            metavar='EMAIL',
            help=(
                "Email address of a user to remove as owner from all "
                "in-progress objects (repeatable).  Only this user is "
                "touched; other owners are left as-is."
            ),
        )

    def handle(self, *args, **options):
        User = get_user_model()
        owners = get_owner_users()
        self.stdout.write("Dynamic owners (active staff):")
        for owner in owners:
            self.stdout.write("  {0}".format(owner.email))
        if not owners:
            self.stdout.write(self.style.WARNING(
                "No active staff users found; nothing to add."
            ))
        else:
            results = sync_owners()
            for label, count, added in results:
                self.stdout.write(
                    "{0}: {1} in-progress; {2} owner(s) added.".format(
                        label,
                        count,
                        added,
                    )
                )
        for email in options['remove']:
            user = User.objects.filter(email=email).first()
            if not user:
                raise CommandError(
                    "No user with email {0}".format(email)
                )
            if user.is_staff and user.is_active:
                self.stdout.write(self.style.WARNING(
                    "{0} is still active staff; skipping removal.".format(
                        email,
                    )
                ))
                continue
            remove_user_from_owners(user)
            self.stdout.write(
                "Removed {0} from all in-progress objects.".format(email)
            )
        self.stdout.write(self.style.SUCCESS("Complete."))
