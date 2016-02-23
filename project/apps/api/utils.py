import csv

from django.db.models import Q

from django.db import IntegrityError

from unidecode import unidecode

from psycopg2.extras import DateRange
import arrow

import logging
log = logging.getLogger(__name__)

from fuzzywuzzy import process

from nameparser import HumanName

from .models import (
    Organization,
    Convention,
    Contest,
    Session,
    Round,
    Award,
    Judge,
    Person,
    Chapter,
    Group,
    Performer,
    Contestant,
    Performance,
    Song,
    Score,
)


def import_members(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        for row in rows:
            try:
                p = Person.objects.get(
                    member=row[0],
                )
                p.member = int(row[0])
                p.bhs_name = row[1]
                p.bhs_city = row[2]
                p.bhs_state = row[3]
                p.bhs_phone = row[4]
                p.bhs_email = row[5]
                p.save()
            except Person.DoesNotExist:
                try:
                    p = Person.objects.get(
                        name__iexact=row[1],
                    )
                    p.member = int(row[0])
                    p.bhs_name = row[1]
                    p.bhs_city = row[2]
                    p.bhs_state = row[3]
                    p.bhs_phone = row[4]
                    p.bhs_email = row[5]
                    p.save()
                except Person.MultipleObjectsReturned:
                    print 'DUPLICATE: {0}'.format(row[0])
                except Person.DoesNotExist:
                    try:
                        p = Person.objects.get(
                            common_name__iexact=row[1],
                        )
                        p.member = int(row[0])
                        p.bhs_name = row[1]
                        p.bhs_city = row[2]
                        p.bhs_state = row[3]
                        p.bhs_phone = row[4]
                        p.bhs_email = row[5]
                        p.save()
                    except Person.MultipleObjectsReturned:
                        print 'DUPLICATE: {0}'.format(row[0])
                    except Person.DoesNotExist:
                        try:
                            p = Person.objects.get(
                                full_name__iexact=row[1],
                            )
                            p.member = int(row[0])
                            p.bhs_name = row[1]
                            p.bhs_city = row[2]
                            p.bhs_state = row[3]
                            p.bhs_phone = row[4]
                            p.bhs_email = row[5]
                            p.save()
                        except Person.MultipleObjectsReturned:
                            print 'DUPLICATE: {0}'.format(row[0])
                        except Person.DoesNotExist:
                            try:
                                p = Person.objects.get(
                                    formal_name__iexact=row[1],
                                )
                                p.member = int(row[0])
                                p.bhs_name = row[1]
                                p.bhs_city = row[2]
                                p.bhs_state = row[3]
                                p.bhs_phone = row[4]
                                p.bhs_email = row[5]
                                p.save()
                            except Person.DoesNotExist:
                                Person.objects.create(
                                    name=unidecode(row[1]),
                                    member=row[0],
                                    bhs_name=row[1],
                                    bhs_city=row[2],
                                    bhs_state=row[3],
                                    bhs_phone=row[4],
                                    bhs_email=row[5],
                                )


def import_quartets(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        for row in rows:
            if row[1].endswith(', The'):
                row[1] = "The " + row[1].partition(',')[0]
        for row in rows:
            try:
                g = Group.objects.get(
                    name__iexact=row[1],
                )
                g.kind = Group.KIND.quartet
                g.group_id = int(row[0])
                g.bhs_name = row[1]
                g.bhs_district = row[2]
                g.bhs_location = row[3]
                g.bhs_contact = row[4]
                g.bhs_expiration = row[5]
                g.save()
            except Group.DoesNotExist:
                Group.objects.create(
                    name=row[1],
                    group_id=int(row[0]),
                    bhs_name=row[1],
                    bhs_district=row[2],
                    bhs_location=row[3],
                    bhs_contact=row[4],
                    bhs_expiration=row[5],
                )


def import_choruses(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        for row in rows:
            try:
                g = Group.objects.get(
                    name__iexact=row[3],
                )
                g.kind = Group.KIND.chorus
                g.group_id = int(row[0])
                g.bhs_chapter_code = row[1]
                g.bhs_chapter_name = row[2]
                g.bhs_name = row[3]
                g.bhs_website = row[4]
                g.bhs_location = ", ".join(filter(None, [
                    row[7],
                    row[8],
                ]))
                g.bhs_phone = row[10]
                g.bhs_contact = row[11]
                g.save()
            except Group.DoesNotExist:
                Group.objects.create(
                    name=row[3],
                    kind=Group.KIND.chorus,
                    group_id=int(row[0]),
                    bhs_chapter_code=row[1],
                    bhs_chapter_name=row[2],
                    bhs_name=row[3],
                    bhs_website=row[4],
                    bhs_location=", ".join(filter(None, [
                        row[7],
                        row[8],
                    ])),
                    bhs_phone=row[10],
                    bhs_contact=row[11],
                )


def import_chapters(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        for row in rows:
            try:
                c = Chapter.objects.get(
                    code=row[1],
                )
                c.bhs_group_id = int(row[0])
                c.bhs_chapter_code = row[1]
                c.bhs_chapter_name = row[2]
                c.bhs_group_name = row[3]
                c.bhs_website = row[4]
                c.bhs_venue = row[5]
                c.bhs_address = row[6]
                c.bhs_city = row[7]
                c.bhs_state = row[8]
                c.bhs_zip = row[9]
                c.bhs_phone = row[10]
                c.bhs_contact = row[11]
                c.save()
                print "Updated {0}".format(c)
            except Chapter.DoesNotExist:
                Chapter.objects.create(
                    name=row[2],
                    code=row[1],
                    bhs_group_id=int(row[0]),
                    bhs_chapter_code=row[1],
                    bhs_chapter_name=row[2],
                    bhs_group_name=row[3],
                    bhs_website=row[4],
                    bhs_venue=row[5],
                    bhs_address=row[6],
                    bhs_city=row[7],
                    bhs_state=row[8],
                    bhs_zip=row[9],
                    bhs_phone=row[10],
                    bhs_contact=row[11],
                )
                print "Created {0}".format(row[2])


def import_awards(convention):
    """One time."""
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

                # Instantiate year
                year = convention.year

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
                    'year': year,
                })

    for award in awards:
        Award.objects.get_or_create(**award)
    return


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
                print "Could not build: {0}".format(row_two)
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
        date = DateRange(
            arrow.get(dates, "MMMM D, YYYY").date(),
            arrow.get(dates, "MMMM D, YYYY").replace(days=+1).date(),
            "[)",
        )
        convention = Convention(
            stix_name=stix_name,
            location=location,
            date=date,
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
    elif 'Youth' in name:
        kind = 'youth'
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
        if row[0].startswith('Judge Count:'):
            count = int(row[0].partition(":")[2])
            size = int(count / 3)
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith('Subsessions:'):
            kind = get_session_kind(row[0])
            convention.sessions.get_or_create(
                kind=getattr(Session.KIND, kind),
                size=size,
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
                num=0,
            )
    for session in convention.sessions.all():
        i = 1
        for round in session.rounds.order_by('-kind'):
            round.num = i
            round.save()
            i += 1
    return


def extract_panel(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    judges = []
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
            for panelist in panelists:
                parts = panelist.partition("=")
                panel_id = int(parts[0].partition(" ")[0].strip())
                category_raw = parts[0].partition(" ")[2][1:4]
                if category_raw == 'MUS':
                    category = Judge.CATEGORY.music
                elif category_raw == 'PRS':
                    category = Judge.CATEGORY.presentation
                elif category_raw == 'SNG':
                    category = Judge.CATEGORY.singing
                else:
                    raise RuntimeError("Can't determine category")
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
                judges.append({
                    'kind': kind,
                    'person': person,
                    'session': round.session,
                    'organization': organization,
                    'panel_id': panel_id,
                    'category': category,
                    'slot': panel_id,
                })
    for judge in judges:
        try:
            Judge.objects.get_or_create(**judge)
        except IntegrityError:
            continue
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
                stix_num = parts[0].strip()
                stix_name = parts[2].strip()
                # Identify the organization
                if convention.organization.long_name in stix_name:
                    organization = convention.organization
                else:
                    try:
                        organization = convention.organization.children.get(
                            long_name=stix_name.partition(" Division")[0],
                        )
                    except Organization.DoesNotExist:
                        log.info("Can't find Org: {0}".format(stix_name.partition(" Division")[0]))
                        continue
                try:
                    award = Award.objects.get(
                        organization=organization,
                        stix_name=stix_name,
                    )
                    goal = Contest.GOAL.championship
                except Award.DoesNotExist:
                    goal = Contest.GOAL.qualifier
                    if "International Preliminary" in stix_name:
                        if "Chorus" in stix_name:
                            award = Award.objects.get(
                                organization__name='BHS',
                                kind=Award.KIND.chorus,
                                long_name='',
                            )
                        elif "Quartet" in stix_name:
                            award = Award.objects.get(
                                organization__name='BHS',
                                kind=Award.KIND.quartet,
                                long_name='',
                            )
                        elif "Seniors" in stix_name:
                            award = Award.objects.get(
                                organization__name='BHS',
                                kind=Award.KIND.seniors,
                                long_name='',
                            )
                        elif "Collegiate" in stix_name:
                            award = Award.objects.get(
                                organization__name='BHS',
                                kind=Award.KIND.collegiate,
                                long_name='',
                            )
                        else:
                            log.info("No award for: {0}".format(stix_name))
                            continue
                    elif "District Qualification" in stix_name:
                        if "Chorus" in stix_name:
                            award = Award.objects.get(
                                organization=session.convention.organization,
                                kind=Award.KIND.chorus,
                                long_name='',
                            )
                        elif "Quartet" in stix_name:
                            award = Award.objects.get(
                                organization=session.convention.organization,
                                kind=Award.KIND.quartet,
                                long_name='',
                            )
                        elif "Seniors" in stix_name:
                            award = Award.objects.get(
                                organization=session.convention.organization,
                                kind=Award.KIND.seniors,
                                long_name='',
                            )
                        elif "Collegiate" in stix_name:
                            award = Award.objects.get(
                                organization=session.convention.organization,
                                kind=Award.KIND.collegiate,
                                long_name='',
                            )
                        else:
                            log.info("No award for: {0}".format(stix_name))
                            continue
                    else:
                        log.info("No award for: {0}".format(stix_name))
                        continue
                except Award.MultipleObjectsReturned:
                    log.info("Multi awards for: {0}".format(stix_name))
                    continue
                contest = {
                    'session': session,
                    'award': award,
                    'goal': goal,
                    'subsession_id': stix_num,
                    'subsession_text': stix_name,
                }
                contests.append(contest)
    for contest in contests:
        try:
            Contest.objects.get_or_create(**contest)
        except IntegrityError:
            pass
    return contests


def extract_contestants(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    contestants = []
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Session: "):
            # first retrieve the performer
            kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=getattr(Session.KIND, kind),
            )
            performer_text = unidecode(row[1].partition(":")[2].strip())

            if performer_text == '(Not Found)':
                continue

            if session.kind == Session.KIND.chorus:
                performer = session.performers.get(
                    group__chapter__name__iexact=performer_text,
                )
            else:
                performer = session.performers.get(
                    group__name__iexact=performer_text,
                )

            # Now get contest
            contest_list = row[2].partition(":")[2].strip().split(",")
            for contest in contest_list:
                stix_num = int(contest)
                try:
                    contest = session.contests.get(
                        subsession_id=stix_num,
                    )
                except Contest.DoesNotExist:
                    log.error("Can't find contest: {0}".format(contest))
                    continue
                contestants.append({
                    'contest': contest,
                    'performer': performer,
                })
    for contestant in contestants:
        try:
            Contestant.objects.get_or_create(**contestant)
        except IntegrityError:
            log.error("Already exists: {0}".format(contestant))
            continue
        except ValueError:
            log.error("Can't create: {0}".format(contestant))
            continue
    return


def extract_performances(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    performances = []
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Session: "):
            # first retrieve the performer
            kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=getattr(Session.KIND, kind),
            )
            performer_text = unidecode(row[1].partition(":")[2].strip())

            if performer_text == '(Not Found)':
                continue

            if session.kind == Session.KIND.chorus:
                performer = session.performers.get(
                    group__chapter__name__iexact=performer_text,
                )
            else:
                performer = session.performers.get(
                    group__name__iexact=performer_text,
                )
            # now get the order appearance
            order = int(row[3].partition(":")[2].strip()) - 1

            # And the Round.
            kind = get_round_kind(row[0])
            round = session.rounds.get(
                kind=getattr(Round.KIND, kind),
            )
            # And put together.
            performances.append({
                'round': round,
                'position': order,
                'performer': performer,
            })
    for performance in performances:
        Performance.objects.get_or_create(**performance)
    return


def extract_songs(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    songs = []
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Session: "):
            # first retrieve the performance
            kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=getattr(Session.KIND, kind),
            )
            performer_text = unidecode(row[1].partition(":")[2].strip())

            if performer_text == '(Not Found)':
                continue

            if session.kind == Session.KIND.chorus:
                performer = session.performers.get(
                    group__chapter__name__iexact=performer_text,
                )
            else:
                performer = session.performers.get(
                    group__name__iexact=performer_text,
                )
            order = int(row[3].partition(":")[2].strip()) - 1
            kind = get_round_kind(row[0])
            round = session.rounds.get(
                kind=getattr(Round.KIND, kind),
            )
            performance = Performance.objects.get(
                round=round,
                performer=performer,
                position=order,
            )

            # Next, get the song number
            number = int(row[4].partition(":")[2].strip())

            # Next, get the song title
            title = unidecode(row[5].partition(":")[2].strip())

            songs.append({
                'performance': performance,
                'order': number,
                'title': title,
            })
    for song in songs:
        Song.objects.get_or_create(**song)
    return


def extract_scores(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    scores = []
    for row in rows:
        if len(row) == 0:
            continue
        # if row[0].startswith("Judge Count: "):
        #     judge_count = int(row[0].partition(":")[2].strip())
        if row[0].startswith("Session: "):
            # first retrieve the songs
            kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=getattr(Session.KIND, kind),
            )
            performer_text = unidecode(row[1].partition(":")[2].strip())

            if performer_text == '(Not Found)':
                continue

            if session.kind == Session.KIND.chorus:
                performer = session.performers.get(
                    group__chapter__name__iexact=performer_text,
                )
            else:
                performer = session.performers.get(
                    group__name__iexact=performer_text,
                )
            order = int(row[3].partition(":")[2].strip()) - 1
            kind = get_round_kind(row[0])
            round = session.rounds.get(
                kind=getattr(Round.KIND, kind),
            )
            performance = Performance.objects.get(
                round=round,
                performer=performer,
                position=order,
            )
            number = int(row[4].partition(":")[2].strip())
            song = performance.songs.get(
                order=number,
            )

            judges = session.judges.order_by('panel_id')
            scores_raw = row[-judges.count():]
            i = 0
            for judge in judges:
                try:
                    points = int(scores_raw[i])
                except:
                    log.error("No points: {0} - {1}".format(points, performance))
                scores.append({
                    'song': song,
                    'judge': judge,
                    'category': judge.category,
                    'kind': judge.kind,
                    'points': points,
                })
                i += 1
    for score in scores:
        Score.objects.get_or_create(**score)
    return


def fill_parents(convention):
    for session in convention.sessions.all():
        for contest in session.contests.exclude(
            goal=Contest.GOAL.championship,
        ):
            award = contest.award
            if convention.kind == Convention.KIND.fall:
                try:
                    parent = Contest.objects.get(
                        award=award,
                        goal=Contest.GOAL.championship,
                        session__convention__year=convention.year + 1,
                    )
                except Contest.DoesNotExist:
                    log.error("No Parent for {0}".format(contest))
            elif convention.kind == Convention.KIND.spring:
                try:
                    parent = Contest.objects.get(
                        award=award,
                        goal=Contest.GOAL.championship,
                        session__convention__year=convention.year,
                    )
                except Contest.DoesNotExist:
                    log.error("No Parent for {0}".format(contest))
            else:
                log.error("Indeterminent convention kind.  {0}".format(convention))
            contest.parent = parent
            contest.save()
    return


def update_panel_size(convention):
    for session in convention.sessions.all():
        session.size = session.judges.filter(
            kind=Judge.KIND.official,
            category=Judge.CATEGORY.music,
        ).count()
        session.save()
    return


def denormalize(convention):
    for session in convention.sessions.all():
        for performer in session.performers.all():
            for performance in performer.performances.all():
                for song in performance.songs.all():
                    song.calculate()
                    song.save()
                performance.calculate()
                performance.save()
            performer.calculate()
            performer.save()
        for contest in session.contests.all():
            contest.rank()
            contest.save()
    return


def rank(convention):
    for session in convention.sessions.all():
        for contest in session.contests.all():
            contest.rank()
            contest.save()
    return


def chapter_district(chapter):
    if not chapter.code:
        log.error("No Chapter Code for {0}".format(chapter))
        return
    else:
        letter = chapter.code[:1]
        chapter.organization = Organization.objects.get(code=letter)


def list_prelims(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        includes = [
            # "Evaluation",
            "Preliminary",
            "Qualification",
            # "Out Of District",
            # "Out Of Division",
            # "Out of Division",
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
                    stix_num = parts[0]
                    stix_name = parts[2]

                    # Skip qualifications
                    if any([string in stix_name for string in includes]):
                        kind = get_session_kind(contest)
                        if not kind:
                            continue
                        kind = getattr(Session.KIND, kind)

                        # Identify the organization
                        if "Preliminary" in stix_name:
                            org = stix_name.partition("District")[0].strip()
                            try:
                                organization = Organization.objects.get(
                                    long_name=org,
                                    kind=Organization.KIND.district,
                                )
                            except Organization.DoesNotExist:
                                print "Prelim Error: {0}, {1}".format(org, stix_name)
                                continue
                            try:
                                parent = Award.objects.get(
                                    kind=kind,
                                    organization=organization.parent,
                                    is_improved=False,
                                    size=None,
                                    idiom=None,
                                    parent=None,
                                )
                            except Award.DoesNotExist:
                                print kind, organization
                        elif "Qualification" in stix_name:
                            if "Division" in stix_name:
                                org = stix_name.rpartition("Division")[0].strip()
                                try:
                                    organization = Organization.objects.get(
                                        long_name=org,
                                        kind=Organization.KIND.division,
                                    )
                                except Organization.DoesNotExist:
                                    print "Division Does Not Exist: {0}, {1}, {2}".format(org, stix_name, path)
                                    continue
                                except Organization.MultipleObjectsReturned:
                                    if path.endswith("20.txt"):
                                        organization = Organization.objects.get(
                                            long_name=org,
                                            kind=Organization.KIND.division,
                                            parent__name='BHS LOL',
                                        )
                                    else:
                                        organization = Organization.objects.get(
                                            long_name=org,
                                            kind=Organization.KIND.division,
                                            parent__name='BHS FWD',
                                        )
                                parent = Award.objects.get(
                                    kind=kind,
                                    organization=organization.parent,
                                    is_improved=False,
                                    size=None,
                                    idiom=None,
                                    parent=None,
                                )
                            else:
                                org = stix_name.partition("District")[0].strip()
                                try:
                                    organization = Organization.objects.get(
                                        long_name=org,
                                        kind=Organization.KIND.district,
                                    )
                                except Organization.DoesNotExist:
                                    print "District error: {0}, {1}, {2}".format(org, stix_name, path)
                                    continue
                                parent = Award.objects.get(
                                    kind=kind,
                                    organization=organization,
                                    is_improved=False,
                                    size=None,
                                    idiom=None,
                                    parent=None,
                                )

                        # Identify number of rounds
                        if "(2 Rounds)" in stix_name:
                            rounds = 2
                        elif "(3 Rounds)" in stix_name:
                            rounds = 3
                        else:
                            rounds = 1

                        if 'fall' in path:
                            season = 1
                        elif 'spring' in path:
                            season = 2
                        else:
                            season = None

                        # Build the dictionary
                        awards.append({
                            'organization': organization,
                            'kind': kind,
                            'is_improved': False,
                            'size': None,
                            'idiom': None,
                            'season': season,
                            'rounds': rounds,
                            # 'stix_num': stix_num,
                            'stix_name': stix_name,
                            'parent': parent,
                        })

    for award in awards:
        try:
            Award.objects.get_or_create(**award)
        except IntegrityError:
            print award
