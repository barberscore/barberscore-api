# Standard Libary
import datetime
import logging
import time

# Third-Party
import pydf
from auth0.v3.authentication import GetToken
from auth0.v3.exceptions import Auth0Error
from auth0.v3.management import Auth0
from cloudinary.uploader import upload_resource
from django_rq import job
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

# Django
from django.apps import apps as api_apps
from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.text import slugify

log = logging.getLogger(__name__)
api = api_apps.get_app_config('api')
bhs = api_apps.get_app_config('bhs')


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


def get_auth0_accounts():
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
                'auth0_id': user['user_id'],
                'email': user['email'],
                'name': user['user_metadata']['name'],
                'barberscore_id': user['app_metadata']['barberscore_id'],
            }
            output.append(payload)
        more = bool(results['users'])
        i += 1
        t = 0
    return output


# Person Updaters
@job
def update_or_create_person_from_human(human):
    Person = api.get_model('Person')
    return Person.objects.update_or_create_from_human(human)


@job
def update_bhs_subscription_from_person(person):
    return person.update_bhs_subscription()


# Quartet Updaters
@job
def update_or_create_quartet_from_structure(structure):
    Group = api.get_model('Group')
    return Group.objects.update_or_create_from_structure(structure)


@job
def update_quartet_memberships(quartet):
    return quartet.update_memberships()


@job
def update_or_create_quartet_membership_from_join(join):
    Member = api.get_model('Member')
    return Member.objects.update_or_create_from_join(join)


# Chapter/Chorus Updaters
@job
def update_or_create_chapter_from_structure(structure):
    Organization = api.get_model('Organization')
    return Organization.objects.update_or_create_from_structure(structure)


@job
def update_chapter_enrollments(chapter):
    return chapter.update_enrollments()


@job
def update_or_create_chapter_enrollment_from_join(join):
    Enrollment = api.get_model('Enrollment')
    return Enrollment.objects.update_or_create_from_join(join)


@job
def update_chorus_from_chapter(chorus):
    return chorus.update_from_chapter()


@job
def update_members_from_enrollments(enrollment):
    Member = api.get_model('Member')
    return Member.objects.update_or_create_from_enrollment(enrollment)

###


@job
def delete_auth0_account_orphan(auth0_id):
    auth0 = get_auth0()
    # Delete Auth0
    auth0.users.delete(auth0_id)
    return auth0_id


@job
def create_auth0_account_from_user(user):
    auth0 = get_auth0()
    # Build payload
    payload = {
        "connection": "email",
        "email": user.email,
        "email_verified": True,
        "user_metadata": {
            "name": user.name
        },
        "app_metadata": {
            "barberscore_id": str(user.id),
        }
    }
    # Create Auth0 Account
    try:
        response = auth0.users.create(payload)
    except Auth0Error as e:
        log.error(e)
        user.delete()
        return
    user.auth0_id = response['user_id']
    user.save()
    return user


@job
def update_auth0_account_from_user(user):
    auth0 = get_auth0()
    # Build payload
    payload = {
        "connection": "email",
        "email": user.email,
        "email_verified": True,
        "user_metadata": {
            "name": user.name
        },
        "app_metadata": {
            "barberscore_id": str(user.id),
        }
    }
    # Update Auth0 Account
    response = auth0.users.update(user.auth0_id, payload)
    user.auth0_id = response['user_id']
    user.save()
    return user


@job
def delete_auth0_account_from_user(user):
    auth0 = get_auth0()
    # Delete Auth0
    if user.auth0_id:
        auth0.users.delete(user.auth0_id)
    return


@job
def update_user_from_person(person):
    User = api.get_model('User')
    user = getattr(person, 'user', None)
    if not user:
        user = User.objects.create(
            email=person.email,
            name=person.full_name,
        )
        person.user = user
        person.save()
        return
    user.name = person.full_name
    user.email = person.email
    user.save()
    return


@job
def update_person_status_from_subscription(subscription):
    Person = api.get_model('Person')
    try:
        person = Person.objects.get(bhs_pk=subscription.human.id)
    except Person.DoesNotExist:
        return
    person.status = getattr(
        Person.STATUS,
        subscription.status,
        Person.STATUS.inactive
    )
    person.current_through = subscription.current_through
    person.save()
    return


@job
def update_is_senior(group):
    Person = api.get_model('Person')
    midwinter = datetime.date(2019, 1, 26)
    persons = Person.objects.filter(
        members__group=group,
        members__status__gt=0,
    )
    all_over_55 = True
    total_years = 0
    for person in persons:
        years = int((midwinter - person.birth_date).days / 365)
        if years < 55:
            all_over_55 = False
        total_years += years
    if all_over_55 and (total_years >= 240):
        group.is_senior = True
    else:
        group.is_senior = False
    group.save()
    return group.is_senior


@job
def update_group_from_bhs(group):
    Group = api.get_model('Group')
    Member = api.get_model('Member')
    Structure = bhs.get_model('Structure')
    if not group.bhs_pk:
        return
    structure = Structure.objects.get(id=group.bhs_pk)
    group, created = Group.objects.update_or_create_from_structure(structure)

    js = structure.smjoins.all(
    ).values(
        'subscription__human',
        'structure',
    ).distinct()

    for j in js:
        m = structure.smjoins.filter(
            subscription__human__id=j['subscription__human'],
            structure__id=j['structure'],
        ).latest('established_date', 'updated_ts')
        Member.objects.update_or_create_from_join(m)
    return group


@job
def update_person_from_bhs(person):
    Person = api.get_model('Person')
    Human = bhs.get_model('Human')
    if not person.bhs_pk:
        raise RuntimeError("No BHS link")
    try:
        human = Human.objects.get(id=person.bhs_pk)
    except Human.DoesNotExist:
        person.delete()
        return
    person, created = Person.objects.update_or_create_from_human(human)
    subscription = human.subscriptions.filter(
        items_editable=True,
    ).latest('created_ts')
    if subscription:
        status = getattr(
            Person.STATUS,
            subscription.status,
            Person.STATUS.inactive
        )
        current_through = subscription.current_through
    else:
        status = Person.STATUS.new
        current_through = None
    person.status = status
    person.current_through = current_through
    person.save()
    return person


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
    public_id = "session/{0}/{1}-bbscores_report.xlsx".format(
        session.id,
        slugify(session.nomen),
    )
    bbscores_report = upload_resource(
        file,
        resource_type='raw',
        public_id=public_id,
        overwrite=True,
        invalidate=True,
    )
    session.bbscores_report = bbscores_report
    session.save()
    return bbscores_report


@job
def create_drcj_report(session):
    Entry = api.get_model('Entry')
    Organization = api.get_model('Organization')
    Participant = api.get_model('Participant')
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'oa',
        'group_name',
        'representing',
        'evaluation',
        'private',
        'bhs_id',
        'group_status',
        'repertory_count',
        'particpant_count',
        'expiring_count',
        'tenor',
        'lead',
        'baritone',
        'bass',
        'directors',
        'awards',
        'chapters',
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
        participants = entry.participants.filter(
            status__gt=0,
        )
        participant_count = participants.count()
        expiring_count = participants.filter(
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
                participant = entry.participants.get(
                    part=part,
                )
            except Participant.DoesNotExist:
                parts[part] = None
                part += 1
                continue
            except Participant.MultipleObjectsReturned:
                parts[part] = None
                part += 1
                continue
            participant_list = []
            participant_list.append(
                participant.person.nomen,
            )
            participant_list.append(
                participant.person.email,
            )
            participant_list.append(
                participant.person.phone,
            )
            participant_detail = "\n".join(filter(None, participant_list))
            parts[part] = participant_detail
            part += 1
        if entry.group.kind == entry.group.KIND.quartet:
            persons = entry.participants.filter(
                status__gt=0,
            ).values_list('person', flat=True)
            cs = Organization.objects.filter(
                enrollments__person__in=persons,
                enrollments__status__gt=0,
                kind=Organization.KIND.chapter,
            ).distinct(
            ).order_by(
                'org_sort',
                'nomen',
            ).values_list(
                'nomen',
                flat=True
            )
            chapters = "\n".join(cs)
        else:
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
    public_id = "session/{0}/{1}-drcj_report.xlsx".format(
        session.id,
        slugify(session.nomen),
    )
    drcj_report = upload_resource(
        file,
        resource_type='raw',
        public_id=public_id,
        overwrite=True,
        invalidate=True,
    )
    session.drcj_report = drcj_report
    session.save()
    return drcj_report


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

    public_id = "appearance/{0}/{1}-variance_report.pdf".format(
        appearance.id,
        slugify(appearance.nomen),
    )
    variance_report = upload_resource(
        file,
        resource_type='raw',
        public_id=public_id,
        overwrite=True,
        invalidate=True,
    )
    appearance.variance_report = variance_report
    appearance.save()
    return variance_report


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

    public_id = "round/{0}/{1}-ors_report.pdf".format(
        round.id,
        slugify(round.nomen),
    )
    ors_report = upload_resource(
        file,
        resource_type='raw',
        public_id=public_id,
        overwrite=True,
        invalidate=True,
    )
    round.ors_report = ors_report
    round.save()
    return ors_report


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

    public_id = "session/{0}/{1}-oss_report.pdf".format(
        session.id,
        slugify(session.nomen),
    )
    oss_report = upload_resource(
        file,
        resource_type='raw',
        public_id=public_id,
        overwrite=True,
        invalidate=True,
    )
    session.oss_report = oss_report
    session.save()
    return oss_report


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

    public_id = "competitor/{0}/{1}-csa_report.pdf".format(
        competitor.id,
        slugify(competitor.nomen),
    )
    csa_report = upload_resource(
        file,
        resource_type='raw',
        public_id=public_id,
        overwrite=True,
        invalidate=True,
    )
    competitor.csa_report = csa_report
    competitor.save()
    return csa_report


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

    public_id = "session/{0}/{1}-sa_report.pdf".format(
        session.id,
        slugify(session.nomen),
    )
    sa_report = upload_resource(
        file,
        resource_type='raw',
        public_id=public_id,
        overwrite=True,
        invalidate=True,
    )
    session.sa_report = sa_report
    session.save()
    return sa_report


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
        admins = entry.group.members.filter(
            is_admin=True,
        )
        for admin in admins:
            group = entry.group.nomen.encode('utf-8').strip()
            person = admin.person.nomen.encode('utf-8').strip()
            email = admin.person.email.encode('utf-8').strip()
            cell = admin.person.cell_phone
            row = [
                group,
                person,
                email,
                cell,
            ]
            ws.append(row)
    file = save_virtual_workbook(wb)
    public_id = "session/{0}/{1}-admins_report.xlsx".format(
        session.id,
        slugify(session.nomen),
    )
    admins_report = upload_resource(
        file,
        resource_type='raw',
        public_id=public_id,
        overwrite=True,
        invalidate=True,
    )
    session.admins_report = admins_report
    session.save()
    return admins_report


@job
def create_actives_report(session):
    Member = api.get_model('Member')
    Group = api.get_model('Group')
    Organization = api.get_model('Organization')
    organizations = Organization.objects.filter(
        awards__contests__in=session.contests.filter(
            status__gt=0,
        )
    ).distinct()
    # Get active Groups in those Organizations
    # This is really hacky.  Probably a better way available.
    groups = []
    for organization in organizations:
        if organization.kind == Organization.KIND.district:
            dist_groups = Group.objects.filter(
                district=organization.code,
                status__gt=0,
                kind=session.kind,
            )
            [groups.append(x) for x in dist_groups]
        elif organization.kind == Organization.KIND.division:
            div_groups = Group.objects.filter(
                division=organization.name,
                status__gt=0,
                kind=session.kind,
            )
            [groups.append(x) for x in div_groups]
    members = Member.objects.filter(
        is_admin=True,
        group__in=groups,
    ).exclude(person__email=None).order_by(
        'group__nomen',
        'person__nomen',
    )
    wb = Workbook()
    ws = wb.active
    fieldnames = [
        'group',
        'chapter',
        'district',
        'division',
        'admin',
        'email',
        'cell',
    ]
    ws.append(fieldnames)
    for member in members:
        group = member.group.nomen.encode('utf-8').strip()
        chapter = member.group.chapter
        district = member.group.district
        division = member.group.division
        person = member.person.nomen.encode('utf-8').strip()
        email = member.person.email.encode('utf-8').strip()
        cell = member.person.cell_phone
        row = [
            group,
            chapter,
            district,
            division,
            person,
            email,
            cell,
        ]
        ws.append(row)
    file = save_virtual_workbook(wb)
    public_id = "session/{0}/{1}-actives_report.xlsx".format(
        session.id,
        slugify(session.nomen),
    )
    actives_report = upload_resource(
        file,
        resource_type='raw',
        public_id=public_id,
        overwrite=True,
        invalidate=True,
    )
    session.actives_report = actives_report
    session.save()
    return actives_report


@job
def create_pdf(template, context):
    rendered = render_to_string(template, context)
    pdf = pydf.generate_pdf(rendered)
    return pdf


@job
def send_entry(template, context):
    entry = context['entry']
    contacts = entry.group.members.filter(
        is_admin=True,
    ).exclude(person__email=None)
    if not contacts:
        log.error("No valid contacts for {0}".format(entry))
        return
    assignments = entry.session.convention.assignments.filter(
        category__lt=10,
    ).exclude(person__email=None)
    tos = ["{0} <{1}>".format(contact.person.common_name, contact.person.email) for contact in contacts]
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
        log.error("{0} {1}".format(e, entry))
        raise(e)
    if result != 1:
        log.error("{0}".format(entry))
        raise RuntimeError("Email unsuccessful {0}".format(entry))
    return


@job
def send_session(template, context):
    session = context['session']
    Group = api.get_model('Group')
    Member = api.get_model('Member')
    Assignment = api.get_model('Assignment')
    Organization = api.get_model('Organization')
    Entry = api.get_model('Entry')
    if session.status > session.STATUS.closed:
        # only send to existing entries
        contacts = Member.objects.filter(
            is_admin=True,
            group__entries__session=session,
            group__entries__status=Entry.STATUS.approved,
        ).exclude(person__email=None)
    else:
        # send to all active groups in the district
        # Get relevant Organizations
        organizations = Organization.objects.filter(
            awards__contests__in=session.contests.filter(
                status__gt=0,
            )
        ).distinct()
        # Get active Groups in those Organizations
        # This is really hacky.  Probably a better way available.
        groups = []
        for organization in organizations:
            if organization.kind == Organization.KIND.district:
                dist_groups = Group.objects.filter(
                    district=organization.code,
                    status__gt=0,
                    kind=session.kind,
                )
                [groups.append(x) for x in dist_groups]
            elif organization.kind == Organization.KIND.division:
                div_groups = Group.objects.filter(
                    division=organization.name,
                    status__gt=0,
                    kind=session.kind,
                )
                [groups.append(x) for x in div_groups]
        contacts = Member.objects.filter(
            is_admin=True,
            group__in=groups,
        ).exclude(person__email=None)
    assignments = Assignment.objects.filter(
        convention=session.convention,
        category=Assignment.CATEGORY.drcj,
        status=Assignment.STATUS.confirmed,
    ).exclude(person__email=None)
    to = ["{0} <{1}>".format(assignment.person.common_name, assignment.person.email) for assignment in assignments]
    bcc = ["{0} <{1}>".format(contact.person.common_name, contact.person.email) for contact in contacts]
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


@job
def send_session_reports(template, context):
    session = context['session']
    Assignment = api.get_model('Assignment')
    assignments = Assignment.objects.filter(
        convention=session.convention,
        category__lte=Assignment.CATEGORY.ca,
        status=Assignment.STATUS.confirmed,
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
