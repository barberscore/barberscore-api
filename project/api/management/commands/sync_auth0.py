# Standard Libary
import logging

# Third-Party
from auth0.v3.management import Auth0
from auth0.v3.management.rest import Auth0Error

# Django
from django.conf import settings
from django.core.management.base import BaseCommand

# First-Party
from api.models import User
from api.utils import get_auth0_token

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Command to sync database with Auth0."

    def get_auth0(self):
        token = get_auth0_token()
        return Auth0(
            settings.AUTH0_DOMAIN,
            token,
        )

    def get_auth0_users(self, auth0):
        lst = []
        more = True
        i = 0
        while more:
            results = auth0.users.list(
                fields=[
                    'user_id',
                ],
                per_page=100,
                page=i,
            )
            payload = [result['user_id'] for result in results['users']]
            lst.extend(payload)
            more = bool(results['users'])
            i += 1
        return lst

    def generate_payload(self, user):
        email = user.email
        try:
            name = user.person.name
        except ValueError:
            name = None
        try:
            bhs_id = user.person.bhs_id
        except ValueError:
            bhs_id = None
        payload = {
            "connection": "email",
            "email": email,
            "email_verified": True,
            "user_metadata": {
                "name": name
            },
            "app_metadata": {
                "bhs_id": bhs_id
            }
        }
        return payload


    def handle(self, *args, **options):
        # Get the Auth0 instance
        auth0 = self.get_auth0()
        # Delete orphaned Auth0
        accounts = self.get_auth0_users(auth0)
        for account in accounts:
            try:
                user = User.objects.get(
                    auth0_id=account,
                )
            except User.DoesNotExist:
                auth0.users.delete(account)
                log.info("DELETED: {0}".format(account))
        account = None
        # Get Auth0, non-admin Barberscore accounts
        users = User.objects.filter(
            is_staff=False,
        ).exclude(
            auth0_id=None,
        )
        for user in users:
            payload = self.generate_payload(user)
            try:
                # Update existing
                account = auth0.users.update(user.auth0_id, payload)
                log.info("UPDATED: {0}".format(account))
            except Auth0Error as e:
                if e.status_code == 404:
                    # Reset orphans
                    account = auth0.users.create(payload)
                    user.auth0_id = account['user_id']
                    user.save()
                    log.info("RESET: {0}".format(account))
                else:
                    # Other errors
                    log.error(e)
        # Get non-Auth0, non-admin
        users = User.objects.filter(
            is_staff=False,
            auth0_id=None,
        )
        for user in users:
            payload = self.generate_payload(user)
            # Create
            try:
                account = auth0.users.create(payload)
            except Auth0Error as e:
                log.error(e)
                continue
            user.auth0_id = account['user_id']
            user.save()
            log.info("CREATED: {0}".format(account))
