# Django
from django.core.management.base import BaseCommand
from auth0.v3.management.rest import Auth0Error

# First-Party
from api.models import User

from api.services import (
    get_auth0,
    get_auth0_users,
    generate_payload,
)


class Command(BaseCommand):
    help = "Command to sync database with Auth0."

    def handle(self, *args, **options):
        # Get the Auth0 instance
        auth0 = get_auth0()
        # Get the accounts
        accounts = get_auth0_users(auth0)
        # Delete orphaned Auth0 accounts
        self.stdout.write("Deleting orphaned accounts...")
        for account in accounts:
            try:
                user = User.objects.get(
                    auth0_id=account['user_id'],
                )
            except User.DoesNotExist:
                auth0.users.delete(account['user_id'])
                self.stdout.write("DELETED: {0}".format(account['user_id']))
        # Get User Accounts
        users = User.objects.exclude(auth0_id=None)
        # Update each User account
        self.stdout.write("Checking auth0 for User accounts...")
        for user in users:
            # First, check to see if the User account is in the Auth0 Account list
            match = next(
                (a for a in accounts if a['user_id'] == str(user.auth0_id)),
                None,
            )
            if match:
                # If you find the account, check to see if it needs updating.
                payload = {
                    'email': user.email,
                    'user_metadata': {
                        'name': user.name,
                    },
                    'user_id': user.auth0_id,
                    'app_metadata': {
                        'barberscore_id': str(user.id),
                    },
                }
                if payload != match:
                    # Details need updating
                    del payload['user_id']
                    account = auth0.users.update(user.auth0_id, payload)
                    self.stdout.write("UPDATED: {0}".format(account['user_id']))
            else:
                # The User account thinks it has an Auth0, but doesn't.  Create (reset)
                payload = generate_payload(user)
                account = auth0.users.create(payload)
                user.auth0_id = account['user_id']
                user.save()
                self.stdout.write("RESET: {0}".format(account['user_id']))
        # Create new accounts
        users = User.objects.filter(
            auth0_id=None,
        )
        self.stdout.write("Creating auth0 accounts...")
        for user in users:
            payload = generate_payload(user)
            # Create
            try:
                account = auth0.users.create(payload)
            except Auth0Error as e:
                self.stdout.write(e)
                continue
            user.auth0_id = account['user_id']
            user.save()
            self.stdout.write("CREATED: {0}".format(account['user_id']))
