# Standard Libary
import logging
import time
import requests
from django.core.files.base import ContentFile
# Third-Party
import pydf
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0
from django_rq import job
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

log = logging.getLogger(__name__)
api = api_apps.get_app_config('api')
bhs = api_apps.get_app_config('bhs')


@job
def copy_image(obj):
    if not obj.img:
        raise RuntimeError("no img")
    resp = requests.get(obj.img.url)
    if resp.status_code != requests.codes.ok:
        raise RuntimeError("No bueno")
        #  Error handling here
    obj.image.save('overwritten', ContentFile(resp.content))


def get_auth0():
    auth0_api_access_token = cache.get('auth0_api_access_token')
    if not auth0_api_access_token:
        client = GetToken(settings.AUTH0_DOMAIN)
        response = client.client_credentials(
            settings.AUTH0_API_ID,
            settings.AUTH0_API_SECRET,
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


def get_accounts():
    auth0 = get_auth0()
    output = []
    more = True
    i = 0
    t = 0
    while more:
        results = auth0.users.list(
            fields=[
                'user_id',
                'email',
                'app_metadata',
                'user_metadata',
            ],
            per_page=100,
            page=i,
        )
        try:
            users = results['users']
        except KeyError:
            t += 1
            if t < 4:
                time.sleep(t ** 2)
                continue
            else:
                raise RuntimeError(results)
        for user in users:
            payload = {
                'account_id': user['user_id'],
                'email': user['email'],
                'name': user['user_metadata']['name'],
                'barberscore_id': user['app_metadata']['barberscore_id'],
            }
            output.append(payload)
        more = bool(results['users'])
        i += 1
        t = 0
    return output


@job
def delete_account(account_id):
    auth0 = get_auth0()
    # Delete Auth0
    auth0.users.delete(account_id)
    return account_id


@job
def update_or_create_account_from_user(user, blocked):
    # Get the auth0 client
    auth0 = get_auth0()
    # Instantiate the created variable
    created = True
    # Try to get existing
    if user.account_id:
        try:
            # Flip the bit if you can find an account
            account = auth0.users.get(user.account_id)
            created = False
        except Auth0Error as e:
            # If you can't find the account legit then proceed
            if not e.status_code == 404:
                # If there's a standard error, raise it.
                raise(e)
    # Build payload
    payload = {
        "connection": "email",
        "email": user.email,
        "email_verified": True,
        # "blocked": blocked,
        "user_metadata": {
            "name": user.name
        },
        "app_metadata": {
            "barberscore_id": str(user.id),
        }
    }
    if created:
        # Create with payload if new
        account = auth0.users.create(payload)
        user.account_id = account['user_id']
        user.save()
    else:
        # Only update if there are diffs
        try:
            dirty = any([
                account['email'] != user.email,
                account['user_metadata']['name'] != user.name,
                account['app_metadata']['barberscore_id'] != str(user.id),
                # account['blocked'] != blocked,
            ])
        except KeyError:
            dirty = True
        if dirty:
            account = auth0.users.update(user.account_id, payload)
    return account, created


@job
def delete_account_from_user(user):
    if not user.account_id:
        raise ValueError("No account attached.")
    auth0 = get_auth0()
    # Delete Auth0
    response = auth0.users.delete(user.account_id)
    return response


@job
def create_bbscores_report(session):
    Entry = api.get_model('Entry')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'oa',
        'contestant_id',
        'group_name',
        'group_type',
        'song_number',
        'song_title',
    ]
    ws.append(fieldnames)
    entries = session.entries.filter(
        status__in=[
            Entry.STATUS.approved,
        ]
    ).order_by('draw')
    for entry in entries:
        oa = entry.draw
        group_name = entry.group.name.encode('utf-8').strip()
        group_type = entry.group.get_kind_display()
        if group_type == 'Quartet':
            contestant_id = entry.group.bhs_id
        elif group_type == 'Chorus':
            contestant_id = entry.group.code
        else:
            raise RuntimeError("Improper Entity Type")
        i = 1
        for repertory in entry.group.repertories.order_by('chart__title'):
            song_number = i
            song_title = repertory.chart.title.encode('utf-8').strip()
            i += 1
            row = [
                oa,
                contestant_id,
                group_name,
                group_type,
                song_number,
                song_title,
            ]
            ws.append(row)
    file = save_virtual_workbook(wb)
    content = ContentFile(file)
    session.bbscores_report.save('overwritten', content)
    session.save
    return session.bbscores_report.url


@job
def create_drcj_report(session):
    Entry = api.get_model('Entry')
    Group = api.get_model('Group')
    Member = api.get_model('Member')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'OA',
        'Group Name',
        'Representing',
        'Evaluation?',
        'Score/Eval-Only?',
        'BHS ID',
        'Group Status',
        'Repertory Count',
        'Estimated MOS',
        'Members Expiring',
        'Tenor',
        'Lead',
        'Baritone',
        'Bass',
        'Director(s)',
        'Award(s)',
        'Chapter(s)',
    ]
    ws.append(fieldnames)
    entries = session.entries.filter(
        status__in=[
            Entry.STATUS.approved,
        ]
    ).order_by('draw')
    for entry in entries:
        oa = entry.draw
        group_name = entry.group.name
        representing = entry.representing
        evaluation = entry.is_evaluation
        private = entry.is_private
        bhs_id = entry.group.bhs_id
        repertory_count = entry.group.repertories.filter(
            status__gt=0,
        ).count()
        group_status = entry.group.get_status_display()
        repertory_count = entry.group.repertories.filter(
            status__gt=0,
        ).count()
        participant_count = entry.mos
        members = entry.group.members.filter(
            status__gt=0,
        )
        expiring_count = members.filter(
            person__current_through__lte=session.convention.close_date,
        ).count()
        directors = entry.directors
        awards_list = []
        contestants = entry.contestants.filter(
            status__gt=0,
        ).order_by('contest__award__name')
        for contestant in contestants:
            awards_list.append(contestant.contest.award.name)
        awards = "\n".join(filter(None, awards_list))
        parts = {}
        part = 1
        while part <= 4:
            try:
                member = members.get(
                    part=part,
                )
            except Member.DoesNotExist:
                parts[part] = None
                part += 1
                continue
            except Member.MultipleObjectsReturned:
                parts[part] = None
                part += 1
                continue
            member_list = []
            member_list.append(
                member.person.nomen,
            )
            member_list.append(
                member.person.email,
            )
            member_list.append(
                member.person.phone,
            )
            member_detail = "\n".join(filter(None, member_list))
            parts[part] = member_detail
            part += 1
        if entry.group.kind == entry.group.KIND.quartet:
            persons = members.values_list('person', flat=True)
            cs = Group.objects.filter(
                members__person__in=persons,
                members__status__gt=0,
                kind=Group.KIND.chorus,
            ).distinct(
            ).order_by(
                'parent__name',
            ).values_list(
                'parent__name',
                flat=True
            )
            chapters = "\n".join(cs)
        elif entry.group.kind == entry.group.KIND.chorus:
            try:
                chapters = entry.group.parent.name
            except AttributeError:
                chapters = None
        row = [
            oa,
            group_name,
            representing,
            evaluation,
            private,
            bhs_id,
            group_status,
            repertory_count,
            participant_count,
            expiring_count,
            parts[1],
            parts[2],
            parts[3],
            parts[4],
            directors,
            awards,
            chapters,
        ]
        ws.append(row)
    file = save_virtual_workbook(wb)
    content = ContentFile(file)
    session.drcj_report.save('overwritten', content)
    session.save()
    return session.drcj_report.url


@job
def create_admins_report(session):
    Entry = api.get_model('Entry')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'group',
        'admin',
        'email',
        'cell',
    ]
    ws.append(fieldnames)
    entries = session.entries.filter(
        status__in=[
            Entry.STATUS.approved,
        ]
    ).order_by('group__nomen')
    for entry in entries:
        admins = entry.group.officers.filter(
            status__gt=0,
        )
        for admin in admins:
            group = entry.group.nomen
            person = admin.person.nomen
            email = admin.person.email
            cell = admin.person.cell_phone
            row = [
                group,
                person,
                email,
                cell,
            ]
            ws.append(row)
    file = save_virtual_workbook(wb)
    content = ContentFile(file)
    session.admins_report.save('overwritten', content)
    session.save()
    return session.admins_report.url


@job
def create_variance_report(appearance):
    Score = api.get_model('Score')
    Panelist = api.get_model('Panelist')
    songs = appearance.songs.order_by('num')
    scores = Score.objects.filter(
        kind=Score.KIND.official,
        song__in=songs,
    ).order_by(
        'category',
        'panelist',
        'song__num',
    )
    panelists = Panelist.objects.filter(
        kind=Panelist.KIND.official,
        scores__song__appearance=appearance,
    ).order_by(
        'category',
        'person__last_name',
        'scores__song__num',
    )
    context = {
        'appearance': appearance,
        'songs': songs,
        'scores': scores,
        'panelists': panelists,
    }
    rendered = render_to_string('variance.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    appearance.variance_report.save('overwritten', content)
    appearance.save()
    return appearance.variance_report.url


@job
def create_ors_report(round):
    competitors = round.session.competitors.order_by(
        'rank',
        'tot_points'
    )
    panelists = round.panelists.filter(
        kind=round.panelists.model.KIND.official,
    ).order_by(
        'category',
    )
    contests = round.session.contests.filter(
        status__gt=0,
    ).order_by(
        '-award__is_primary',
        'award__name',
    )
    context = {
        'round': round,
        'competitors': competitors,
        'panelists': panelists,
        'contests': contests,
    }
    rendered = render_to_string('ors.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    round.ors_report.save('overwritten', content)
    round.save()
    return round.ors_report.url


@job
def create_oss_report(session):
    Panelist = api.get_model('Panelist')
    competitors = session.competitors.order_by(
        'rank',
        'tot_points'
    )
    rounds = session.rounds.all()
    panelists = Panelist.objects.filter(
        kind=Panelist.KIND.official,
        round__in=rounds,
    ).order_by(
        'category',
    )
    contests = session.contests.filter(
        status__gt=0,
    ).order_by(
        '-award__is_primary',
        'award__name',
    )
    context = {
        'session': session,
        'competitors': competitors,
        'panelists': panelists,
        'contests': contests,
    }
    rendered = render_to_string('oss.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    session.oss_report.save('overwritten', content)
    session.save()
    return session.oss_report.url


@job
def create_csa_report(competitor):
    Panelist = api.get_model('Panelist')
    panelists = Panelist.objects.filter(
        kind=Panelist.KIND.official,
        scores__song__appearance__competitor=competitor,
    ).distinct(
    ).order_by(
        'category',
        'person__last_name',
    )
    appearances = competitor.appearances.order_by(
        'round__num',
    )
    # contests = session.contests.filter(
    #     status__gt=0,
    # ).order_by(
    #     '-award__is_primary',
    #     'award__name',
    # )
    context = {
        'competitor': competitor,
        'panelists': panelists,
        'appearances': appearances,
    }
    rendered = render_to_string('csa.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    competitor.csa_report.save('overwritten', content)
    competitor.save()
    return competitor.csa_report.url


@job
def create_sa_report(session):
    Person = api.get_model('Person')
    persons = Person.objects.filter(
        panelists__round__session=session,
    ).distinct(
    ).order_by(
        'panelists__category',
        'panelists__kind',
        'last_name',
        'first_name',
    )
    competitors = session.competitors.order_by('rank')
    context = {
        'session': session,
        'persons': persons,
        'competitors': competitors,
    }
    rendered = render_to_string('sa.html', context)
    file = pydf.generate_pdf(rendered)
    content = ContentFile(file)
    session.sa_report.save('overwritten', content)
    session.save()
    return session.sa_report.url


@job
def create_pdf(template, context):
    rendered = render_to_string(template, context)
    pdf = pydf.generate_pdf(rendered)
    return pdf


@job('high')
def send_entry(template, context):
    entry = context['entry']
    officers = entry.group.officers.filter(
        status__gt=0,
        person__email__isnull=False,
    )
    if not officers:
        raise RuntimeError("No officers for {0}".format(entry.group))
    assignments = entry.session.convention.assignments.filter(
        category__lt=10,
    ).exclude(person__email=None)
    tos = ["{0} <{1}>".format(officer.person.common_name, officer.person.email) for officer in officers]
    ccs = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    rendered = render_to_string(template, context)
    subject = "[Barberscore] {0}".format(entry.nomen)
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=tos,
        cc=ccs,
        bcc=[
            'admin@barberscore.com',
            'proclamation56@gmail.com',
        ],
    )
    try:
        result = email.send()
    except Exception as e:
        raise(e)
    if result != 1:
        raise RuntimeError("Email unsuccessful {0}".format(entry))
    return


@job('high')
def send_session(template, context):
    session = context['session']
    Officer = api.get_model('Officer')
    Assignment = api.get_model('Assignment')
    Entry = api.get_model('Entry')
    if session.status > session.STATUS.closed:
        # only send to approved entries
        officers = Officer.objects.filter(
            status__gt=0,
            person__email__isnull=False,
            group__entries__session=session,
            group__entries__status=Entry.STATUS.approved,
        ).distinct()
    elif not session.is_invitational:
        # send to all active groups in the district
        if session.kind == session.KIND.quartet:
            officers = Officer.objects.filter(
                status__gt=0,
                person__email__isnull=False,
                group__status__gt=0,
                group__kind=session.kind,
                group__parent__grantors__convention=session.convention,
            ).distinct()
        else:
            officers = Officer.objects.filter(
                status__gt=0,
                person__email__isnull=False,
                group__status__gt=0,
                group__kind=session.kind,
                group__parent__parent__grantors__convention=session.convention,
            ).distinct()
    assignments = Assignment.objects.filter(
        convention=session.convention,
        category=Assignment.CATEGORY.drcj,
        status=Assignment.STATUS.active,
    ).exclude(person__email=None)
    to = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    bcc = ["{0} <{1}>".format(officer.person.common_name, officer.person.email) for officer in officers]
    bcc.extend([
        'Barberscore Admin <admin@barberscore.com>',
        'David Mills <proclamation56@gmail.com>',
    ])
    rendered = render_to_string(template, context)
    subject = "[Barberscore] {0}".format(session.nomen)
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=to,
        bcc=bcc,
    )
    return email.send()


@job('high')
def send_session_reports(template, context):
    session = context['session']
    Assignment = api.get_model('Assignment')
    assignments = Assignment.objects.filter(
        convention=session.convention,
        category__lte=Assignment.CATEGORY.ca,
        status=Assignment.STATUS.active,
    ).exclude(person__email=None)
    to = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    bcc = [
        'Barberscore Admin <admin@barberscore.com>',
        'David Mills <proclamation56@gmail.com>',
    ]
    rendered = render_to_string(template, context)
    subject = "[Barberscore] {0} Reports".format(session.nomen)
    email = EmailMessage(
        subject=subject,
        body=rendered,
        from_email='Barberscore <admin@barberscore.com>',
        to=to,
        bcc=bcc,
    )
    return email.send()
