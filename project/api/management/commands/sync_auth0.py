from django.core.management.base import BaseCommand
import logging

# Django
from auth0.v3.management import Auth0
from auth0.v3.management.rest import Auth0Error

from django.conf import settings

# Local
from api.models import (
    User,
)

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

    def get_auth0_users(self):
        auth0 = self.get_auth0()
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

    def update_or_create_auth0(self, user):
        auth0 = self.get_auth0()
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
        try:
            account, result = auth0.users.update(user.auth0_id, payload), 'Updated'
        except Auth0Error:
            account, result = auth0.users.create(payload), 'Created'
        return account, result

    def handle(self, *args, **options):
        auth0 = self.get_auth0()
        accounts = self.get_auth0_users()
        for account in accounts:
            try:
                user = User.objects.get(
                    auth0_id=account,
                )
            except User.DoesNotExist:
                auth0.users.delete(account)
                log.info("Deleted: {0}".format(account))

        users = User.objects.filter(
            is_staff=False,
        )
        for user in users:
            account, response = self.update_or_create_auth0(user)
            if response == 'Created':
                user.auth0_id = account['user_id']
                user.save()
            log.info("{1}: {0}".format(account['user_id'], response))
