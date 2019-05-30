import json

from django.core.cache import cache
from django.conf import settings
from auth0.v3.authentication import GetToken
# from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0
from django.utils.crypto import get_random_string
from django_rq import job
from django.apps import apps

def get_auth0():
    auth0_api_access_token = cache.get('auth0_api_access_token')
    if not auth0_api_access_token:
        client = GetToken(settings.AUTH0_DOMAIN)
        response = client.client_credentials(
            settings.AUTH0_CLIENT_ID,
            settings.AUTH0_CLIENT_SECRET,
            settings.AUTH0_AUDIENCE,
        )
        cache.set(
            'auth0_api_access_token',
            response['access_token'],
            timeout=response['expires_in'],
        )
        auth0_api_access_token = response['access_token']
    auth0 = Auth0(
        settings.AUTH0_DOMAIN,
        auth0_api_access_token,
    )
    return auth0


def get_accounts(path='barberscore.json'):
    with open(path) as file:
        accounts = [json.loads(line) for line in file]
        return accounts


@job('low')
def create_or_update_account_from_human(human):
    if isinstance(human, dict):
        mc_pk = human['id']
        first_name = human['first_name']
        last_name = human['last_name']
        nick_name = human['nick_name']
        email = human['email']
        bhs_id = human['bhs_id']
    else:
        mc_pk = str(human.id)
        first_name = human.first_name
        last_name = human.last_name
        nick_name = human.nick_name
        email = human.email
        bhs_id = human.bhs_id

    # Transform
    if nick_name:
        first = nick_name
    else:
        first = first_name
    common_name = " ".join([first, last_name])

    if not email:
        return "Invalid", False

    auth0 = get_auth0()
    q = "app_metadata.mc_pk={0}".format(mc_pk)
    params = {
        'include_totals': True,
        'include_fields': False,
        'search_engine': 'v3',
        'q': q,
    }
    results = auth0.users.list(**params)

    if results['total']:
        email = email
        name = common_name
        username = results['users'][0]['user_id']
        payload = {
            'name': name,
            'given_name': first_name,
            'family_name': last_name,
            'email': email,
            'email_verified': True,
            'app_metadata': {
                'mc_pk': mc_pk,
                'bhs_id': bhs_id,
                'name': None,
            },
            'user_metadata': {}
        }
        try:
            check = all([
                email == results['users'][0]['email'],
                bhs_id == results['users'][0]['app_metadata']['bhs_id'],
                common_name == results['users'][0]['name'],
                first_name == results['users'][0]['given_name'],
                last_name == results['users'][0]['last_name'],
            ])
        except KeyError:
            check = False
        if not check:
            account = auth0.users.update(username, payload)
            created = False
        else:
            return "Skipped", False
    else:
        password = get_random_string()
        payload = {
            'connection': 'Default',
            'email': email,
            'email_verified': True,
            'password': password,
            'name': name,
            'given_name': first_name,
            'family_name': last_name,
            'app_metadata': {
                'mc_pk': mc_pk,
                'bhs_id': bhs_id,
            },
            'user_metadata': {},
        }
        account = auth0.users.create(payload)
        created = True
    return account, created

@job('low')
def delete_account_from_human(human):
    if isinstance(human, dict):
        mc_pk = human['id']
    else:
        mc_pk = str(human.id)
    auth0 = get_auth0()
    q = "app_metadata.mc_pk={0}".format(mc_pk)
    params = {
        'include_totals': True,
        'include_fields': False,
        'search_engine': 'v3',
        'q': q,
    }
    results = auth0.users.list(**params)
    if results['total'] == 1:
        auth0.users.delete(results['users'][0]['user_id'])
        return "Deleted: {0}".format(human)
    return "Not Found: {0}".format(human)


def get_account_orphans():
    Person = apps.get_model('bhs.person')
    accounts = get_accounts()
    one = [a['app_metadata']['mc_pk'] for a in accounts]
    two = list(Person.objects.values_list('mc_pk', flat=True))
    orphans = [{'id':a} for a in one if a not in two]
    return orphans
