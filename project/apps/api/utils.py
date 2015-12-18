import csv

from django.db.models import Q
from unidecode import unidecode

import logging
log = logging.getLogger(__name__)

from nameparser import HumanName

from .models import (
    Organization,
    Convention,
    Session,
    Round,
    Award,
    Judge,
    Person,
    Chapter,
    Group,
    Performer,
)


def import_convention(path, kind, division=False):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        row_one = rows[0]
        row_two = rows[1]
        stix_name = row_one[2]
        if division:
            try:
                district = row_two[0].partition("District")[0].strip()
                division = row_two[1].strip()
                location = ", ".join([row_two[2], row_two[3]])
                dates = ", ".join([row_two[4], row_two[5]])
                year = int(row_two[5])
            except IndexError:
                log.error("Could not build: {0}".format(row_two))
        else:
            try:
                district = row_two[0].partition("District")[0].strip()
                location = ", ".join([row_two[1], row_two[2]])
                dates = ", ".join([row_two[3], row_two[4]])
                year = int(row_two[4])
            except IndexError:
                log.error("Could not build: {0}".format(row_two))
        try:
            organization = Organization.objects.get(
                long_name=district,
            )
        except Organization.DoesNotExist:
            raise RuntimeError("No Match for: {0}".format(district))
        convention = Convention(
            stix_name=stix_name,
            location=location,
            dates=dates,
            year=year,
            organization=organization,
            kind=getattr(Convention.KIND, kind),
        )
        if division:
            convention.stix_div = division
            convention.division = getattr(Convention.DIVISION, division)
    return convention


def get_session_kind(name):
    if 'Novice' in name:
        kind = 'novice'
    elif 'Seniors' in name:
        kind = 'seniors'
    elif 'Collegiate' in name:
        kind = 'collegiate'
    elif 'Chorus' in name:
        kind = 'chorus'
    elif 'Quartet' in name:
        kind = 'quartet'
    elif "Dealer's Choice" in name:
        kind = 'quartet'
    elif "Srs Qt - Oldest Qt Cumulative Yrs" in name:
        kind = 'seniors'
    else:
        log.error("Could not determine Session.KIND: {0}".format(name))
        return None
    return kind


def get_round_kind(name):
    if ' Quarter-Finals' in name:
        kind = 'quarters'
    elif ' Semi-Finals' in name:
        kind = 'semis'
    elif ' Finals' in name:
        kind = 'finals'
    else:
        log.error("Could not determine Round.KIND: {0}".format(name))
        return None
    return kind


def extract_sessions(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith('Subsessions:'):
            kind = get_session_kind(row[0])
            convention.sessions.get_or_create(
                kind=getattr(Session.KIND, kind),
            )
    return


def extract_rounds(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Subsessions:"):
            session_kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=getattr(Session.KIND, session_kind),
            )
            round_kind = get_round_kind(row[0])
            session.rounds.create(
                kind=getattr(Round.KIND, round_kind),
                stix_name=row[0],
            )
    return


def create_awards(convention):
    """One time"""
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    excludes = [
        "Evaluation",
        "Preliminary",
        "Qualification",
        "Out Of District",
        "Out Of Division",
        "Out of Division",
    ]
    awards = []
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith('Subsessions:'):
            contest_list = row[1:]
            for contest in contest_list:

                # Parse each list item for id, name
                parts = contest.partition('=')
                # stix_num = parts[0]
                stix_name = parts[2]

                # Skip qualifications
                if any([string in stix_name for string in excludes]):
                    continue

                # Identify the organization
                parent = convention.organization
                if parent.long_name in stix_name:
                    organization = parent
                else:
                    organization = parent.children.get(
                        long_name=stix_name.partition(" Division")[0],
                    )

                # Identify number of rounds
                if "(2 Rounds)" in stix_name:
                    rounds = 2
                elif "(3 Rounds)" in stix_name:
                    rounds = 3
                else:
                    rounds = 1

                kind = get_session_kind(contest)
                if not kind:
                    continue
                kind = getattr(Session.KIND, kind)

                # Instantiate long_name
                long_name = stix_name

                # Exceptions for International
                if "Dealer's Choice" in long_name:
                    long_name = "Dealer's Choice"
                elif "Srs Qt - Oldest Qt Cumulative Yrs" in stix_name:
                    long_name = "Oldest Quartet"
                else:
                    # Remove paranthetical data.  Assumed to tail.
                    long_name = long_name.partition("(")[0].strip()
                    # Remove redundant Organization
                    long_name = long_name.partition("{0} {1}".format(
                        organization.long_name,
                        organization.get_kind_display(),
                    ))[2].strip()
                    # Remove the redundant kind from the string
                    long_name = long_name.partition("{0}".format(
                        Award.KIND[kind]
                    ))[0].strip()

                # Build the dictionary
                awards.append({
                    'organization': organization,
                    'kind': kind,
                    'long_name': long_name,
                    'rounds': rounds,
                    'stix_name': stix_name,
                })

    for award in awards:
        Award.objects.get_or_create(**award)
    return


def extract_panel(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith('Panel'):
            session_kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=getattr(Session.KIND, session_kind),
            )
            round_kind = get_round_kind(row[0])
            try:
                round = session.rounds.get(
                    kind=getattr(Round.KIND, round_kind),
                )
            except TypeError:
                log.error("Can't find Panel: {0}".format(row[0]))
                continue
            panelists = row[1:]
            mus_slot = 1
            prs_slot = 1
            sng_slot = 1
            for panelist in panelists:
                parts = panelist.partition("=")
                panel_id = int(parts[0].partition(" ")[0].strip())
                category = parts[0].partition(" ")[2][1:4]
                nm = unidecode(parts[2])
                name = str(HumanName(nm))
                if panel_id < 50:
                    kind = Judge.KIND.official
                else:
                    kind = Judge.KIND.practice
                try:
                    person = Person.objects.get(
                        Q(formal_name=name) | Q(common_name=name) | Q(full_name=name) | Q(name=name)
                    )
                except Person.DoesNotExist:
                    person = Person.objects.create(
                        name=name,
                    )
                except Person.MultipleObjectsReturned:
                    persons = Person.objects.filter(
                        Q(formal_name=name) | Q(common_name=name) | Q(full_name=name) | Q(name=name)
                    )
                    for person in persons:
                        person.status = Person.STATUS.dup
                        person.save()
                    person = persons.order_by('-is_judge').first()
                    person.save()
                if not person.is_judge:
                    person.status = Person.STATUS.stix
                    person.save()
                if person.organization:
                    organization = person.organization
                else:
                    organization = Organization.objects.get(name='BHS FHT')
                judge_dict = {
                    'kind': kind,
                    'person': person,
                    'round': round,
                    'organization': organization,
                    'session': session,
                    'panel_id': panel_id,
                }
                if category == 'MUS':
                    judge_dict['category'] = Judge.CATEGORY.music
                    judge_dict['slot'] = mus_slot
                    mus_slot += 1
                elif category == 'PRS':
                    judge_dict['category'] = Judge.CATEGORY.presentation
                    judge_dict['slot'] = prs_slot
                    prs_slot += 1
                elif category == 'SNG':
                    judge_dict['category'] = Judge.CATEGORY.singing
                    judge_dict['slot'] = sng_slot
                    sng_slot += 1
                else:
                    raise RuntimeError("Unknown category! {0}".format(category))
                Judge.objects.create(**judge_dict)
    return


def extract_performers(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    performers = []
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Session: "):
            kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=getattr(Session.KIND, kind),
            )
            contestant_text = unidecode(row[1].partition(":")[2].strip())
            if contestant_text == '(Not Found)':
                continue
            if session.kind == Session.KIND.chorus:
                try:
                    chapter = Chapter.objects.get(
                        name__iexact=contestant_text,
                    )
                except Chapter.DoesNotExist:
                    log.info("Potential Duplicate: {0}".format(contestant_text))
                    chapter = Chapter.objects.create(
                        name=contestant_text,
                        status=Chapter.STATUS.dup,
                    )
                try:
                    group = chapter.groups.exclude(
                        status=Group.STATUS.inactive,
                    ).get(
                        chapter=chapter,
                    )
                except Group.MultipleObjectsReturned:
                    group = chapter.groups.exclude(
                        status=Group.STATUS.inactive,
                    ).filter(
                        chapter=chapter,
                    ).first()
                    group.status = Group.STATUS.dup
                    group.save()
                    log.info("Check chapter groups for: {0}".format(group.chapter))
                except Group.DoesNotExist:
                    group = Group.objects.create(
                        name=contestant_text,
                        status=Group.STATUS.dup,
                        chapter=chapter,
                    )
            else:
                try:
                    group = Group.objects.get(
                        name__iexact=contestant_text,
                    )
                except Group.DoesNotExist:
                    log.info("Potential Duplicate: {0}".format(contestant_text))
                    group = Group.objects.create(
                        name=contestant_text,
                        status=Group.STATUS.dup,
                    )
            performers.append({
                'session': session,
                'group': group,
                'status': Performer.STATUS.final,
            })
    for performer in performers:
        Performer.objects.get_or_create(**performer)
    return


def extract_contests(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    contests = []
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Subsessions:"):
            session_kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=getattr(Session.KIND, session_kind),
            )
            contest_list = row[1:]
            for item in contest_list:
                parts = item.partition("=")
                award = Award.objects.get(
                    stix_name=parts[2],
                )
                contest = {
                    'session': session,
                    'award': award,
                }
        contests.append(contest)
    return contests
