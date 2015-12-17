import os
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


def extract_sessions(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    sessions = {}
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith('Subsessions:'):
            parts = row[0].partition(":")
            contest_name = parts[2].strip()
            if 'Collegiate' in contest_name:
                kind = 'collegiate'
            elif 'Senior' in contest_name:
                kind = 'senior'
            else:
                kind = contest_name.partition(" ")[0].lower()
            sessions[kind] = True
    for key, value in sessions.viewitems():
        Session.objects.create(
            convention=convention,
            year=convention.year,
            kind=getattr(Session.KIND, key),
        )
    return


def extract_rounds(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Subsessions:"):
            subsession_text = row[0].partition(":")[2].strip()
            # Strip parantheticals
            subsession_text = subsession_text.partition("(")[0].strip()
            # Catch Collegiate
            if 'Collegiate' in subsession_text:
                subsession_text = "Collegiate Finals"
            if 'Seniors' in subsession_text:
                subsession_text = "Senior Finals"
            # Split the subsession
            parts = subsession_text.partition(" ")
            session_kind = parts[0].strip().lower()
            round_kind = parts[2].strip()
            # print session_kind
            # print round_kind
            # continue
            session = convention.sessions.get(
                kind=getattr(Session.KIND, session_kind),
            )
            if round_kind == 'Finals':
                kind = 'finals'
            elif round_kind == 'Semi-Finals':
                kind = 'semis'
            elif round_kind == 'Quarter-Finals':
                kind = 'quarters'
            session.rounds.create(
                kind=getattr(Round.KIND, kind),
                stix_name=subsession_text,
            )
    return
    # Determine meta-data
    # counts = {}
    # counts['collegiate'] = 0
    # counts['chorus'] = 0
    # counts['quartet'] = 0
    # for row in rows:
    #     if len(row) == 0:
    #         continue
    #     if row[0].startswith('Subsessions:'):
    #         # Parse session into components
    #         parts = row[0].partition(':')
    #         # Parse session meta-data
    #         session_text = parts[2].strip()
    #         if 'Collegiate' in session_text:
    #             counts['collegiate'] += 1
    #         elif session_text.startswith('Chorus'):
    #             counts['chorus'] += 1
    #         elif session_text.startswith('Quartet'):
    #             counts['quartet'] += 1
    #         else:
    #             raise RuntimeError("Can't determine session kind")
    # for key, value in counts.viewitems():
    #     if value:
    #         i = 1
    #         j = value
    #         while i <= value:
    #             try:
    #                 session = convention.sessions.get(
    #                     kind=getattr(Session.KIND, key),
    #                 )
    #             except Session.DoesNotExist:
    #                 print "No session: {0} {1}".format(key, value)
    #             rnd, created = session.rounds.get_or_create(
    #                 num=i,
    #                 kind=j,
    #                 stix_name=session_text.partition("(")[0].strip(),
    #             )
    #             i += 1
    #             j -= 1


def extract_awards(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    sessions = convention.sessions.all()
    excludes = [
        "Evaluation",
        "Preliminary",
        "Qualification",
        "Out Of District",
        "Out Of Division",
        "Out of Division",
    ]
    for session in sessions:
        contest = {}
        for row in rows:
            if len(row) == 0:
                continue
            if row[0].startswith('Subsessions:'):
                if 'Collegiate' in row[0]:
                    kind = 'collegiate'
                else:
                    kind = row[0].partition(":")[2].strip().partition(" ")[0].strip().lower()
                if session.kind == getattr(Session.KIND, kind):
                    contest_list = row[1:]
                    for c in contest_list:
                        # Parse each list item for id, name
                        parts = c.partition('=')
                        contest_num = parts[0]
                        contest_name = parts[2]
                        # Skip qualifications
                        if any([string in contest_name for string in excludes]):
                            continue
                        contest[contest_num] = contest_name
        parent = convention.organization
        for key, value in contest.viewitems():
            # Set values for legacy data
            stix_num = key
            stix_name = value
            # Match organization
            if parent.long_name in value:
                organization = parent
            else:
                organization = parent.children.get(
                    long_name=value.partition(" Division")[0],
                )
            # Create name variable for parsing
            name = stix_name
            # Identify number of rounds (if applicable)
            if "(2 Rounds)" in name:
                rounds = 2
                name = name.partition("(2 Rounds)")[0].strip()
            elif "(3 Rounds)" in name:
                rounds = 3
                name = name.partition("(3 Rounds)")[0].strip()
            else:
                rounds = 1
            # Remove paranthetical data for District/Division
            name = name.partition("(")[0].strip()
            # Remove the redundant organization from the string
            name = value.partition("{0} {1}".format(
                organization.long_name,
                organization.get_kind_display(),
            ))[2].strip()
            # Identify the kind by name and remove.  Order is important (for quartets)
            if 'Srs Qt -' in name:
                name = name.partition('Srs Qt -')[0].strip()
                kind = Award.KIND.senior
            if 'Novice' in name:
                name = name.partition('Novice')[0].strip()
                kind = Award.KIND.novice
            elif 'Seniors' in name:
                name = name.partition('Seniors')[0].strip()
                kind = Award.KIND.senior
            elif 'Collegiate' in name:
                name = name.partition('Collegiate')[0].strip()
                kind = Award.KIND.collegiate
            elif 'Chorus' in name:
                name = name.partition('Chorus')[0].strip()
                kind = Award.KIND.chorus
            elif 'Quartet' in name:
                name = name.partition('Quartet')[0].strip()
                kind = Award.KIND.quartet
            elif "Dealer's Choice" in name:
                kind = Award.KIND.quartet
            else:
                kind = None
            award, created = Award.objects.get_or_create(
                long_name=name,
                organization=organization,
                kind=kind,
            )
            if created:
                award.rounds = rounds
                award.stix_num = stix_num
                award.stix_name = stix_name
                award.save()
    return


def extract_panel(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith('Panel'):
            subsession = row[0].partition("-")[2].partition(":")[0].strip()
            if 'Collegiate' in subsession:
                subsession = "Collegiate Finals"
            if 'Seniors' in subsession:
                subsession = "Senior Finals"
            round = Round.objects.get(
                session__convention=convention,
                stix_name=subsession,
            )
            panelists = row[1:]
            mus_slot = 1
            prs_slot = 1
            sng_slot = 1
            for panelist in panelists:
                parts = panelist.partition("=")
                panel_id = int(parts[0].partition(" ")[0].strip())
                category = parts[0].partition(" ")[2][1:4]
                nm = parts[2]
                try:
                    nm = u'{0}'.format(nm)
                except UnicodeDecodeError:
                    nm = unidecode(nm)
                name = str(HumanName(nm))
                if panel_id < 50:
                    kind = Judge.KIND.official
                else:
                    kind = Judge.KIND.practice
                try:
                    person = Person.objects.get(
                        Q(formal_name=name) | Q(common_name=name) | Q(full_name=name)
                    )
                except Person.DoesNotExist:
                    person = Person.objects.create(
                        name=name,
                    )
                except Person.MultipleObjectsReturned:
                    persons = Person.objects.filter(
                        Q(formal_name=name) | Q(common_name=name) | Q(full_name=name)
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
                    'session': round.session,
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


def deinterlace(path):
    with open(path) as csvfile:
        raw = [row for row in csv.reader(
            csvfile,
        )]
        l = len(raw)
        data = []
        i = 0
        #  Deinterlace and build list of dictionaries.
        while i < l:
            if (i % 2 == 0):  # zero-indexed rows
                row = raw[i]
                row.extend(raw[i + 1])
                data.append(row)
            else:  # Skip interlaced row; added supra
                pass
            i += 1
        return data


def strip_penalties(output):
    for row in output:
        scores = [6, 7, 8, 10, 11, 12]
        for score in scores:
            try:
                int(row[score])
            except ValueError:
                row[score] = row[score][:3]
    return output


def write_file(path, output):
    basepath = os.path.split(path)[0]
    namepath = os.path.split(path)[1]
    with open(os.path.join(basepath, namepath,), 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in output:
            writer.writerow(row)
    return


def parse_chorus(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[9].split('[', 1)[1].split(']', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[9] = row[9].split('[', 1)[0]
        # Add round
        row.extend(['1'])
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    # new_list = [[row[ci] for ci in (
    #     18, 16, 8, 0, 17, 1, 2, 3, 4, 9, 10, 11, 12, 6, 7
    # )] for row in output]

    # new_list = strip_penalties(new_list)

    output = write_file(path, output)

    return


def parse_chorus_nd(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        # row.extend([row[8].split('(', 1)[1].split(')', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        # row[8] = row[8].split('(', 1)[0]
        # Add round
        row.extend(['1'])
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    new_list = [[row[ci] for ci in (
        17, 16, 8, 0, 15, 1, 2, 3, 4, 9, 10, 11, 12, 6, 7
    )] for row in output]

    new_list = strip_penalties(new_list)

    output = write_file(path, new_list)

    return


def parse_district_chorus(path, district):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[9].split('(', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[9] = row[9].split('(', 1)[0]
        # Add round
        row.extend(['1'])
        # Overwrite district
        row[19] = district
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    # Reorder in list -- SUPER Kludge!
    for row in output:
        row.insert(0, row.pop(-1))
        row.insert(1, row.pop(-2))
        row.insert(2, row.pop(11))
        row.insert(4, row.pop(-1))
        row.insert(-1, row.pop(12))
        row.pop(5)
        row.pop(9)
        row.pop(9)
        row.pop(9)
        row.pop(13)
        row.pop(13)
        row.pop(14)

    output = strip_penalties(output)

    output = write_file(path, output)

    return


def parse_quarters(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[7].split('[', 1)[1].split(']', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[7] = row[7].split('[', 1)[0]
        # Add round
        row.extend(['3'])
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    new_list = [[row[ci] for ci in (
        16, 14, 0, 15, 12, 1, 2, 3, 4, 8, 9, 10, 11, 6,
    )] for row in output]

    new_list = strip_penalties(new_list)

    output = write_file(path, new_list)

    return


def parse_semis(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[9].split('[', 1)[1].split(']', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[9] = row[9].split('[', 1)[0]
        # Add round
        row.extend(['2'])
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    new_list = [[row[ci] for ci in (
        20, 18, 0, 19, 14, 1, 2, 3, 4, 10, 11, 12, 13, 8,
    )] for row in output]

    new_list = strip_penalties(new_list)

    output = write_file(path, new_list)

    return


def parse_finals(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[9].split('[', 1)[1].split(']', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[9] = row[9].split('[', 1)[0]
        # Add round
        row.extend(['1'])
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    # Reorder in list -- SUPER Kludge!
    for row in output:
        row.insert(0, row.pop(-1))
        row.insert(1, row.pop(-2))
        row.insert(3, row.pop(-2))
        row.insert(4, row.pop(-1))
        row.pop(9)
        row.pop(9)
        row.pop(9)
        row.pop(9)
        row.pop(9)
        row.pop(-1)
        row.pop(-1)

    output = strip_penalties(output)

    output = write_file(path, output)

    return


def place_round(performers):
    draw = []
    i = 1
    for performer in performers:
        try:
            match = performer.points == draw[0].points
        except IndexError:
            performer.place = i
            performer.save()
            draw.append(performer)
            continue
        if match:
            performer.place = i
            i += len(draw)
            performer.save()
            draw.append(performer)
            continue
        else:
            i += 1
            performer.place = i
            performer.save()
            draw = [performer]
    return


def merge_groups(from_group, to_group):
    cs = from_group.performers.all()
    for c in cs:
        c.group = to_group
        c.save()
    from_group.delete()


def score_performer(performer):
    session = performer.contest.session
    if performer.contest.kind == 1:
        if performer.quarters_points and not performer.semis_points:
            performer.score = round(performer.points / (session * 6 * 1), 1)
        elif performer.semis_points and not performer.finals_points:
            performer.score = round(performer.points / (session * 6 * 2), 1)
        elif performer.finals_points:
            performer.score = round(performer.points / (session * 6 * 3), 1)
        else:
            performer.score = None
    else:
        performer.score = round(performer.points / (session * 6 * 1), 1)
    performer.save()
    return


def parse_arrangers(data):
    names = [
        ['quarters_song1', 'quarters_song1_arranger'],
        ['quarters_song2', 'quarters_song2_arranger'],
        ['semis_song1', 'semis_song1_arranger'],
        ['semis_song2', 'semis_song2_arranger'],
        ['finals_song1', 'finals_song1_arranger'],
        ['finals_song2', 'finals_song2_arranger'],
    ]

    for row in data:
        try:
            c = Performer.objects.get(
                contest__name='International Quartet 2015',
                group__name__iexact=row[0],
            )
        except c.DoesNotExist:
            print row
        for n in names:
            song = getattr(c, n[0])
            try:
                match = (song.name == row[1])
            except AttributeError:
                continue
            if match:
                try:
                    arranger = Person.objects.get(name__iexact=row[2])
                except Person.DoesNotExist:
                    continue
                setattr(c, n[1], arranger)
                c.save()
