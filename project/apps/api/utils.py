# Standard Libary
import csv
import logging

# Third-Party
import arrow
from nameparser import HumanName
from psycopg2.extras import DateRange
from unidecode import unidecode

# Django
from django.db import IntegrityError
from django.db.models import Q

# Local
from .models import (
    Award,
    Chapter,
    Chart,
    Contest,
    Contestant,
    Convention,
    Group,
    Judge,
    Organization,
    Performance,
    Performer,
    Person,
    Role,
    Round,
    Score,
    Session,
    Song,
    Submission,
)

log = logging.getLogger(__name__)


def import_members(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        for row in rows:
            try:
                p = Person.objects.get(
                    bhs_id=row[0],
                )
                p.bhs_id = int(row[0])
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
                    p.bhs_id = int(row[0])
                    p.bhs_name = row[1]
                    p.bhs_city = row[2]
                    p.bhs_state = row[3]
                    p.bhs_phone = row[4]
                    p.bhs_email = row[5]
                    p.save()
                except Person.MultipleObjectsReturned:
                    log.error('DUPLICATE: {0}'.format(row[0]))
                except Person.DoesNotExist:
                    try:
                        p = Person.objects.get(
                            common_name__iexact=row[1],
                        )
                        p.bhs_id = int(row[0])
                        p.bhs_name = row[1]
                        p.bhs_city = row[2]
                        p.bhs_state = row[3]
                        p.bhs_phone = row[4]
                        p.bhs_email = row[5]
                        p.save()
                    except Person.MultipleObjectsReturned:
                        log.error('DUPLICATE: {0}'.format(row[0]))
                    except Person.DoesNotExist:
                        try:
                            p = Person.objects.get(
                                full_name__iexact=row[1],
                            )
                            p.bhs_id = int(row[0])
                            p.bhs_name = row[1]
                            p.bhs_city = row[2]
                            p.bhs_state = row[3]
                            p.bhs_phone = row[4]
                            p.bhs_email = row[5]
                            p.save()
                        except Person.MultipleObjectsReturned:
                            log.error('DUPLICATE: {0}'.format(row[0]))
                        except Person.DoesNotExist:
                            try:
                                p = Person.objects.get(
                                    formal_name__iexact=row[1],
                                )
                                p.bhs_id = int(row[0])
                                p.bhs_name = row[1]
                                p.bhs_city = row[2]
                                p.bhs_state = row[3]
                                p.bhs_phone = row[4]
                                p.bhs_email = row[5]
                                p.save()
                            except Person.DoesNotExist:
                                Person.objects.create(
                                    name=unidecode(row[1]),
                                    bhs_id=row[0],
                                    bhs_name=row[1],
                                    bhs_city=row[2],
                                    bhs_state=row[3],
                                    bhs_phone=row[4],
                                    bhs_email=row[5],
                                )


def import_db_persons(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            created = False
            try:
                p = Person.objects.get(
                    bhs_id=int(row[0])
                )
            except Person.DoesNotExist:
                first_name = row[4].strip()
                nick_name = row[5].strip()
                if nick_name:
                    if nick_name != first_name:
                        nick_name = "({0})".format(nick_name)
                middle_name = row[6].strip()
                last_name = row[7].strip()
                suffix_name = row[8].strip()
                prefix_name = row[2].strip()
                email = row[9].strip()
                name = " ".join(filter(None, [
                    prefix_name,
                    first_name,
                    middle_name,
                    last_name,
                    suffix_name,
                    nick_name,
                ]))
                try:
                    birth_date = arrow.get(row[31]).date()
                except arrow.parser.ParserError:
                    birth_date = None
                try:
                    p, created = Person.objects.get_or_create(
                        bhs_id=int(row[0]),
                        name=unidecode(name),
                        email=email,
                        birth_date=birth_date,
                    )
                except UnicodeDecodeError:
                    continue
            print p, created


def import_db_quartets(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            if int(row[4]) == 3:
                name = row[2].strip()
                if name.endswith(', The'):
                    name = "The " + name.partition(', The')[0]
                try:
                    created = False
                    g = Group.objects.get(
                        bhs_id=int(row[0]),
                    )
                except Group.DoesNotExist:
                    bhs_id = int(row[0])
                    try:
                        g, created = Group.objects.get_or_create(
                            bhs_id=bhs_id,
                            name=unidecode(name),
                        )
                    except UnicodeDecodeError:
                        continue
            else:
                continue
            print g, created


def import_db_chapters(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            if int(row[4]) == 4:
                code = row[1].strip()
                name = row[2].partition(" ")[2].strip()
                try:
                    created = False
                    c = Chapter.objects.get(
                        bhs_id=int(row[0]),
                    )
                except Chapter.DoesNotExist:
                    bhs_id = int(row[0])
                    try:
                        c, created = Chapter.objects.get_or_create(
                            bhs_id=bhs_id,
                            code=code,
                            name=unidecode(name),
                        )
                    except UnicodeDecodeError:
                        continue
                    except IntegrityError:
                        exist = Chapter.objects.get(
                            code=code,
                        )
                        exist.bhs_id = bhs_id
                        exist.save()
                        created = 'UPDATED'
            else:
                continue
            print c, created


def import_db_roles(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            if int(row[12]) not in [1, 2, 3, 4]:
                continue
            try:
                group = Group.objects.get(
                    bhs_id=int(row[1])
                )
            except Group.DoesNotExist:
                log.error("Missing Group {0}: {1}".format(row[1], row[2]))
                continue
            if group.KIND == Group.KIND.chorus:
                log.error("Chorus, not Quartet {0}: {1}".format(row[1], row[2]))
                continue
            try:
                person = Person.objects.get(
                    bhs_id=int(row[3])
                )
            except Person.DoesNotExist:
                person = Person.objects.create(
                    name=unidecode(row[4]),
                    bhs_id=int(row[3]),
                )
            if int(row[12]) == 1:
                part = Role.PART.tenor
            elif int(row[12]) == 2:
                part = Role.PART.lead
            elif int(row[12]) == 3:
                part = Role.PART.baritone
            elif int(row[12]) == 4:
                part = Role.PART.bass
            else:
                log.error("No Part: {0}".format(row[12]))
                continue
            try:
                lower = arrow.get(row[7]).date()
            except arrow.parser.ParserError:
                log.error("No lower date: {0}".format(row[7]))
                lower = None
            if not row[8]:
                upper = None
            else:
                try:
                    upper = arrow.get(row[8]).date()
                except arrow.parser.ParserError:
                    log.error("No upper date: {0}".format(row[8]))
                    upper = None
            date = DateRange(
                lower=lower,
                upper=upper,
                bounds="[)",
            )
            if upper and lower:
                if lower > upper:
                    date = None
            role = {
                'bhs_id': int(row[0]),
                'group': group,
                'person': person,
                'date': date,
                'part': part,
            }
            try:
                role, created = Role.objects.get_or_create(
                    **role
                )
            except Role.MultipleObjectsReturned:
                log.error("Multi Roles: {1}".format(group))
                continue
            print role


def import_db_directors(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            if int(row[5]) != 38:
                continue
            else:
                part = Role.PART.director
            groups = Group.objects.filter(
                chapter__bhs_id=int(row[1]),
                status=Group.STATUS.active,
                kind=Group.KIND.chorus,
            )
            if groups.count() > 1:
                log.error("Too many groups {0}: {1}".format(row[1], row[2]))
                continue
            elif groups.count() == 0:
                group = Group.objects.filter(
                    chapter__bhs_id=int(row[1])
                ).first()
                if not group:
                    try:
                        chapter = Chapter.objects.get(bhs_id=int(row[1]))
                    except Chapter.DoesNotExist:
                        log.error("No chapter {0}: {1}".format(row[1], row[2]))
                        continue
                    group, c = Group.objects.get_or_create(
                        chapter=chapter,
                        status=Group.STATUS.inactive,
                        name=row[2].strip(),
                        kind=Group.KIND.chorus,
                    )
            else:
                group = groups.first()
            if group.kind != Group.KIND.chorus:
                log.error("Not a chorus {0}: {1}".format(row[1], row[2]))
                continue
            try:
                person = Person.objects.get(
                    bhs_id=(row[3])
                )
            except Person.DoesNotExist:
                log.error("Missing Person {0}: {1} for {2} {3}".format(
                    row[3],
                    row[4],
                    row[1],
                    row[2],
                ))
                continue
            try:
                lower = arrow.get(row[7]).date()
            except arrow.parser.ParserError:
                log.error("No lower date: {0}".format(row[7]))
                lower = None
            if not row[8]:
                upper = None
            else:
                try:
                    upper = arrow.get(row[8]).date()
                except arrow.parser.ParserError:
                    log.error("No upper date: {0}".format(row[8]))
                    upper = None
            if lower < upper:
                date = DateRange(
                    lower=lower,
                    upper=upper,
                    bounds="[)",
                )
            else:
                log.error("Date out of sequence: {0} {1}".format(
                    row[7],
                    row[8],
                ))
                date = None
            role = {
                'bhs_id': int(row[0]),
                'group': group,
                'person': person,
                'date': date,
                'part': part,
            }
            try:
                role, created = Role.objects.get_or_create(
                    **role
                )
            except Role.MultipleObjectsReturned:
                log.error("ERROR: Multi Roles: {1}".format(role))
                continue
            print role
        return


def import_db_charts(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            if not row[0]:
                continue
            try:
                c = Chart.objects.get(
                    bhs_marketplace=int(row[0]),
                )
            except Chart.DoesNotExist:
                bhs_marketplace = int(row[0])
                try:
                    bhs_published = arrow.get(row[1]).date()
                except arrow.parser.ParserError:
                    bhs_published = None
                title = row[2]
                arranger = row[3]
                try:
                    bhs_fee = float(row[4])
                except ValueError:
                    bhs_fee = None
                is_parody = bool(row[8])
                is_medley = bool(row[9])
                c, created = Chart.objects.get_or_create(
                    bhs_marketplace=bhs_marketplace,
                    title=title,
                    bhs_published=bhs_published,
                    arranger=arranger,
                    bhs_fee=bhs_fee,
                    is_parody=is_parody,
                    is_medley=is_medley,
                )


def import_db_performers(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            convention_bhs_id = int(row[3])
            group_bhs_id = int(row[2])
            soa = int(row[6]) if int(row[6]) else None
            try:
                convention = Convention.objects.get(
                    bhs_id=convention_bhs_id,
                )
            except Convention.DoesNotExist:
                log.error("No Convention: {0}".format(row[3]))
                continue
            try:
                group = Group.objects.get(
                    bhs_id=group_bhs_id,
                )
            except Group.DoesNotExist:
                try:
                    chapter = Chapter.objects.get(code=row[1][:4])
                    groups = chapter.groups.filter(status=Group.STATUS.active)
                    if groups.count() == 1:
                        group = groups.first()
                        group.bhs_id = group_bhs_id
                        group.save()
                    else:
                        log.error("No Group: {0}, {1}".format(row[2], row[1]))
                        continue
                except Chapter.DoesNotExist:
                    log.error("No Group: {0}, {1}".format(row[2], row[1]))
            if row[7].strip() == 'Normal Evaluation and Coaching':
                is_evaluation = True
            else:
                is_evaluation = False
            try:
                session = convention.sessions.get(
                    kind=group.kind,
                )
            except Session.DoesNotExist:
                try:
                    session = convention.sessions.get(
                        kind=Session.KIND.youth,
                    )
                except Session.DoesNotExist:
                    log.error("No Session: {0}, {1} - {2}".format(convention, group, group.get_kind_display()))
                    continue
            performer, created = Performer.objects.get_or_create(
                session=session,
                group=group,
            )
            performer.soa = soa
            performer.is_evaluation = is_evaluation
            performer.bhs_id = int(row[0])
            performer.save()


def import_db_submissions(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            if row[2]:
                try:
                    chart = Chart.objects.get(
                        bhs_marketplace=int(row[2])
                    )
                except Chart.DoesNotExist:
                    chart = None
            else:
                chart = None
            if not chart:
                try:
                    chart = Chart.objects.get(
                        title=row[1],
                        bhs_marketplace=None,
                    )
                except Chart.DoesNotExist:
                    if row[2]:
                        chart = Chart.objects.create(
                            title=row[1],
                            bhs_marketplace=int(row[2])
                        )
                    else:
                        chart = Chart.objects.create(
                            title=row[1],
                        )
                except Chart.MultipleObjectsReturned:
                    chart = Chart.objects.filter(
                        title=row[1],
                        bhs_marketplace=None,
                    ).first()
            performers = Performer.objects.filter(
                group__bhs_id=int(row[0]),
                session__convention__year=2016,
            )
            for performer in performers:
                submission, created = Submission.objects.get_or_create(
                    performer=performer,
                    chart=chart,
                )
                print submission, created


def import_db_representing(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            name = row[11].strip()
            if name == 'Div I':
                name = 'Division I Division'
            elif name == 'Div II':
                name = 'Division II Division'
            elif name == 'Div III':
                name = 'Division III Division'
            elif name == 'Div IV':
                name = 'Division IV Division'
            elif name == 'Div V':
                name = 'Division V Division'
            elif name == 'Arizona  Division':
                name = 'Arizona Division'
            elif name == 'Division One':
                name = 'Division One Division'
            elif name == 'Granite & Pine Division':
                name = 'Granite and Pine Division'
            if name != 'NULL':
                convention = Convention.objects.get(
                    bhs_id=int(row[3]),
                )
                district_name = convention.organization.short_name
                try:
                    organization = Organization.objects.get(
                        name="{0} {1}".format(
                            district_name,
                            name,
                        )
                    )
                except Organization.DoesNotExist:
                    log.error("Bad Div: {0} {1}".format(district_name, name))
                    continue
                try:
                    performer = Performer.objects.get(
                        bhs_id=int(row[0]),
                    )
                except Performer.DoesNotExist:
                    log.error("Can't find performer")
                    continue
                performer.representing = organization
                performer.save()


def import_db_contests(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            convention_bhs_id = int(row[3])
            performer_bhs_id = int(row[0])
            try:
                convention = Convention.objects.get(
                    bhs_id=convention_bhs_id,
                )
            except Convention.DoesNotExist:
                log.error("No Convention: {0}".format(row[3]))
                continue
            name = row[8].strip()
            try:
                performer = Performer.objects.get(
                    bhs_id=performer_bhs_id,
                )
            except Performer.DoesNotExist:
                log.error("Can't find performer")
                continue
            try:
                session = convention.sessions.get(
                    kind=performer.group.kind,
                )
            except Session.DoesNotExist:
                try:
                    session = convention.sessions.get(
                        kind=Session.KIND.youth,
                    )
                except Session.DoesNotExist:
                    try:
                        session = convention.sessions.get(
                            kind=Session.KIND.seniors,
                        )
                    except Session.DoesNotExist:
                        log.error("No Session: {0}, {1} - {2}".format(
                            convention,
                            performer.group,
                            performer.group.get_kind_display(),
                        ))
                        continue
            if not performer.representing:
                log.error("No representation for {0}".format(performer))
                continue
            organization = performer.representing
            if organization.level == Organization.LEVEL.district:
                district = organization
                division = None
            elif organization.level == Organization.LEVEL.division:
                district = organization.parent
                division = organization
            else:
                log.error("Bad Rep: {0} {1}".format(
                    performer,
                    organization,
                ))
                continue
            excludes = [
                "International Srs Qt - Oldest Singer",
            ]
            if any([string in name for string in excludes]):
                continue
            if name == 'Scores for Evaluation Only':
                performer.status = Performer.STATUS.evaluation
                performer.save()
                continue
            name = name.replace("Most Improved", "Most-Improved")
            try:
                award = Award.objects.get(
                    organization=performer.representing,
                    stix_name__endswith=name,
                )
            except Award.DoesNotExist:
                if 'International Preliminary Quartet' in name:
                    award = Award.objects.get(
                        name='International Quartet',
                    )
                elif 'International Preliminary Youth Qt' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.international,
                        kind=Award.KIND.youth,
                    )
                elif 'International Preliminary Seniors Qt' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.international,
                        kind=Award.KIND.seniors,
                    )
                elif 'Quartet District Qualification' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.district,
                        kind=Award.KIND.quartet,
                        organization=district,
                    )
                elif 'International Seniors Quartet' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.international,
                        kind=Award.KIND.seniors,
                    )
                elif 'International Srs Qt - Oldest Qt' in name:
                    award = Award.objects.get(
                        name='International Oldest Seniors'
                    )
                elif 'Seniors Qt District Qualification (Overall)' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.district,
                        kind=Award.KIND.seniors,
                        organization=district,
                    )
                elif 'District Super Seniors Quartet' in name:
                    award = Award.objects.get(
                        name='Far Western District Super Seniors'
                    )
                elif 'Out Of District Qt Prelims (2 Rounds)' in name:
                    award = Award.objects.get(
                        name='International Quartet',
                    )
                elif 'Out of Division Quartet (Score)' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.district,
                        kind=Award.KIND.quartet,
                        organization=district,
                    )
                elif 'Out Of Division Seniors Quartet' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.district,
                        kind=Award.KIND.seniors,
                        organization=district,
                    )
                elif 'Out Of Division Quartet (Overall)' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.district,
                        kind=Award.KIND.quartet,
                        organization=district,
                    )
                elif 'International Chorus' == name:
                    award = Award.objects.get(
                        name='International Chorus',
                    )
                elif 'International Preliminary Chorus' == name:
                    award = Award.objects.get(
                        name='International Chorus',
                    )
                elif 'Chorus District Qualification' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.district,
                        kind=Award.KIND.chorus,
                        organization=district,
                    )
                elif 'Most-Improved Chorus' in name:
                    award = Award.objects.get(
                        level=Award.LEVEL.district,
                        kind=Award.KIND.chorus,
                        organization=district,
                        is_improved=True,
                    )
                elif 'Out Of Division Chorus' in name:
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.district,
                        kind=Award.KIND.chorus,
                        organization=district,
                    )
                elif 'Plateau A (or 1) Chorus' == name:
                    if row[4] == 'Division Only':
                        organization = division
                        level = Award.LEVEL.division
                    else:
                        organization = district
                        level = Award.LEVEL.district
                    if "Improved" in name:
                        is_improved = True
                    else:
                        is_improved = False
                    award = Award.objects.get(
                        Q(
                            stix_name__contains='Plateau A ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ) | Q(
                            stix_name__contains='Plateau 1 ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ) | Q(
                            stix_name__contains='Plateau I ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ),
                    )
                elif 'Plateau AA (or 2) Chorus' == name:
                    if row[4] == 'Division Only':
                        organization = division
                        level = Award.LEVEL.division
                    else:
                        organization = district
                        level = Award.LEVEL.district
                    if "Improved" in name:
                        is_improved = True
                    else:
                        is_improved = False
                    award = Award.objects.get(
                        Q(
                            stix_name__contains='Plateau AA ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ) | Q(
                            stix_name__contains='Plateau 2 ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ) | Q(
                            stix_name__contains='Plateau II ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ),
                    )
                elif 'Plateau AAA (or 3) Chorus' == name:
                    if row[4] == 'Division Only':
                        organization = division
                        level = Award.LEVEL.division
                    else:
                        organization = district
                        level = Award.LEVEL.district
                    if "Improved" in name:
                        is_improved = True
                    else:
                        is_improved = False
                    award = Award.objects.get(
                        Q(
                            stix_name__contains='Plateau AAA ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ) | Q(
                            stix_name__contains='Plateau 3 ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ) | Q(
                            stix_name__contains='Plateau III ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ),
                    )
                elif 'Plateau AAAA (or 4) Chorus' == name:
                    if row[4] == 'Division Only':
                        organization = division
                        level = Award.LEVEL.division
                    else:
                        organization = district
                        level = Award.LEVEL.district
                    if "Improved" in name:
                        is_improved = True
                    else:
                        is_improved = False
                    award = Award.objects.get(
                        Q(
                            stix_name__contains='Plateau AAAA ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ) | Q(
                            stix_name__contains='Plateau 4 ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ) | Q(
                            stix_name__contains='Plateau IV ',
                            level=level,
                            kind=Award.KIND.chorus,
                            organization=organization,
                            is_improved=is_improved,
                        ),
                    )
                elif 'Division Quartet' == name:
                    if not division:
                        log.error("Div with no Div: {0}".format(performer))
                        continue
                    award = Award.objects.get(
                        is_primary=True,
                        level=Award.LEVEL.division,
                        kind=Award.KIND.quartet,
                        organization=division,
                    )
                else:
                    log.error(
                        "No Award: {0}, {1} {2}".format(
                            name,
                            district,
                            division,
                        )
                    )
                    continue
            except Award.MultipleObjectsReturned:
                log.error("Multiawards")
                continue
            contest, foo = session.contests.get_or_create(
                award=award,
            )
            contestant, created = Contestant.objects.get_or_create(
                contest=contest,
                performer=performer,
            )
            print contestant, created


def import_home_districts(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            try:
                group = Group.objects.get(
                    bhs_id=int(row[0]),
                )
            except Group.DoesNotExist:
                log.error('NO GROUP: {0}'.format(row[0]))
                continue
            org = Organization.objects.get(
                short_name=row[2].partition(" ")[0],
                level=Organization.LEVEL.district,
            )
            group.location = row[1].strip()
            group.organization = org
            group.save()


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
                g.bhs_id = int(row[0])
                g.bhs_name = row[1]
                g.bhs_district = row[2]
                g.bhs_location = row[3]
                g.bhs_contact = row[4]
                g.bhs_expiration = row[5]
                g.save()
            except Group.DoesNotExist:
                Group.objects.create(
                    name=row[1],
                    bhs_id=int(row[0]),
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
                g.bhs_id = int(row[0])
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
                    bhs_id=int(row[0]),
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
                c.bhs_id = int(row[0])
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
                    bhs_id=int(row[0]),
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


def import_prelims(path):
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
            log.error("Already exists: {0}".format(award))
            continue


def import_convention(path, season, division=False):
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
            season=getattr(Convention.SEASON, season),
        )
        if division:
            convention.stix_div = division
            convention.division = getattr(Convention.DIVISION, division)
    return convention


def get_session_kind(name):
    if 'Chorus' in name:
        kind = Session.KIND.chorus
    elif 'Seniors' in name:
        kind = Session.KIND.seniors
    elif 'Collegiate' in name:
        kind = Session.KIND.collegiate
    elif 'Youth' in name:
        kind = Session.KIND.youth
    else:
        kind = Session.KIND.quartet
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
                kind=kind,
                status=Session.STATUS.final,
            )
    return


def extract_rounds(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Subsessions:"):
            kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=kind,
            )
            round_kind = get_round_kind(row[0])
            session.rounds.create(
                kind=getattr(Round.KIND, round_kind),
                stix_name=row[0],
                num=0,
                status=Round.STATUS.final,
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
            kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=kind,
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
                bhs_panel_id = int(parts[0].partition(" ")[0].strip())
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
                if bhs_panel_id < 50:
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
                    'bhs_panel_id': bhs_panel_id,
                    'category': category,
                    'slot': bhs_panel_id,
                    'status': Judge.STATUS.final,
                })
    for judge in judges:
        try:
            Judge.objects.get_or_create(**judge)
        except IntegrityError:
            log.error("Already exists: {0}".format(judge))
            continue
    return


def extract_performers(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    performers = []
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Session: ") and row[4].endswith("1"):
            kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=kind,
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
                    log.error("Can't find chorus by chapter name: {0}, {1}".format(contestant_text, convention))
                    continue
                try:
                    group = chapter.groups.get(
                        status=Group.STATUS.active,
                        chapter=chapter,
                    )
                except Group.DoesNotExist:
                    log.error("Can't find chorus by chapter: {0}, {1}".format(contestant_text, chapter))
                    continue
                except Group.MultipleObjectsReturned:
                    log.error("Multi choruses found for chapter: {0}, {1}".format(contestant_text, chapter))
                    continue
            else:
                try:
                    group = Group.objects.get(
                        name__iexact=contestant_text,
                    )
                except Group.DoesNotExist:
                    group = Group.objects.create(
                        name=contestant_text,
                        status=Group.STATUS.inactive,
                    )
                    log.info("Created Inactive Group: {0}".format(contestant_text))
            performers.append({
                'session': session,
                'group': group,
                'status': Performer.STATUS.final,
                'organization': group.organization,
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
            kind = get_session_kind(row[0])
            session = convention.sessions.get(
                kind=kind,
            )
            contest_list = row[1:]
            excludes = [
                "Evaluation",
                "Out Of District",
                "Out Of Division",
                "Out of Division",
            ]
            for item in contest_list:
                is_qualifier = False
                if convention.season == convention.SEASON.spring:
                    cycle = convention.year
                else:
                    cycle = convention.year + 1
                parts = item.partition("=")
                stix_num = parts[0].strip()
                stix_name = parts[2].strip()
                # Skip evals
                if any([string in stix_name for string in excludes]):
                    continue
                # Identify the organization
                if convention.organization.long_name in stix_name:
                    organization = convention.organization
                else:
                    try:
                        organization = convention.organization.children.get(
                            Q(long_name=stix_name.partition(" Division")[0]) | Q(short_name=stix_name.partition(" Division")[0])
                        )
                    except Organization.DoesNotExist:
                        log.info("Can't find Org: {0}".format(stix_name.partition(" Division")[0]))
                        continue
                if 'Preliminary' in stix_name:
                    award = Award.objects.get(
                        kind=kind,
                        organization=convention.organization.parent,
                        is_primary=True,
                    )
                    is_qualifier = True
                else:
                    try:
                        award = Award.objects.get(
                            organization=organization,
                            stix_name=stix_name,
                        )
                    except Award.DoesNotExist:
                        log.info("No award for: {0}".format(stix_name))
                        continue
                    except Award.MultipleObjectsReturned:
                        log.info("Multi awards for: {0}".format(stix_name))
                        continue
                contest = {
                    'session': session,
                    'award': award,
                    'stix_num': stix_num,
                    'stix_name': stix_name,
                    'status': Contest.STATUS.active,
                    'is_qualifier': is_qualifier,
                    'cycle': cycle,
                }
                contests.append(contest)
    for contest in contests:
        try:
            Contest.objects.get_or_create(**contest)
        except IntegrityError:
            log.error("Contest name already exists: {0}".format(contest))
            continue
    return


def extract_contestants(convention):
    reader = csv.reader(convention.stix_file, skipinitialspace=True)
    rows = [row for row in reader]
    contestants = []
    no_contest = {}
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Subsessions:"):
            kind = get_session_kind(row[0])
            rnd = get_round_kind(row[0])
            key = "{0}{1}{2}".format(kind, rnd)
            kind_list = []
            contest_list = row[1:]
            excludes = [
                "Evaluation",
                "Out Of District",
                "Out Of Division",
                "Out of Division",
            ]
            for item in contest_list:
                parts = item.partition("=")
                stix_num = parts[0].strip()
                stix_name = parts[2].strip()
                if any([string in stix_name for string in excludes]):
                    kind_list.append(stix_num)
            no_contest[key] = kind_list
    for row in rows:
        if len(row) == 0:
            continue
        if row[0].startswith("Session: "):
            # first retrieve the performer
            kind = get_session_kind(row[0])
            rnd = get_round_kind(row[0])
            key = "{0}{1}{2}".format(kind, rnd)
            session = convention.sessions.get(
                kind=kind,
            )
            performer_text = unidecode(row[1].partition(":")[2].strip())

            if performer_text == '(Not Found)':
                continue

            if session.kind == Session.KIND.chorus:
                try:
                    performer = session.performers.get(
                        group__chapter__name__iexact=performer_text,
                    )
                except Performer.DoesNotExist:
                    log.error("No Performer: {0}".format(performer_text))
                    continue
            else:
                performer = session.performers.get(
                    group__name__iexact=performer_text,
                )

            # Now get contest
            contest_list = row[2].partition(":")[2].strip().split(",")
            for contest in contest_list:
                stix_num = int(contest)
                if str(stix_num) in no_contest[key]:
                    log.info("Out of District: {0}".format(performer))
                    continue
                try:
                    contest = session.contests.get(
                        stix_num=stix_num,
                    )
                except Contest.DoesNotExist:
                    log.error("Can't find contest: {0}, {1}, {2}, {3}".format(contest, convention, kind, performer))
                    continue
                except Contest.MultipleObjectsReturned:
                    log.error("Multiple contests: {0}, {1}, {2}, {3}, {4}".format(contest, convention, kind, performer, stix_num))
                    continue
                contestants.append({
                    'contest': contest,
                    'performer': performer,
                    'status': Contestant.STATUS.final,
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
                kind=kind,
            )
            performer_text = unidecode(row[1].partition(":")[2].strip())

            if performer_text == '(Not Found)':
                continue

            if session.kind == Session.KIND.chorus:
                try:
                    performer = session.performers.get(
                        group__chapter__name__iexact=performer_text,
                    )
                except Performer.DoesNotExist:
                    log.error("Can not find chorus: {0}".format(performer_text))
                    continue
            else:
                try:
                    performer = session.performers.get(
                        group__name__iexact=performer_text,
                    )
                except Performer.DoesNotExist:
                    log.error("Can not find quartet: {0}".format(performer_text))
                    continue
            # now get the order appearance
            order = int(row[3].partition(":")[2].strip())

            # And the Round.
            kind = get_round_kind(row[0])
            round = session.rounds.get(
                kind=getattr(Round.KIND, kind),
            )
            # And put together.
            performances.append({
                'round': round,
                'slot': order,
                'position': (order - 1),
                'performer': performer,
                'status': Performance.STATUS.final,
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
                kind=kind,
            )
            performer_text = unidecode(row[1].partition(":")[2].strip())

            if performer_text == '(Not Found)':
                continue

            if session.kind == Session.KIND.chorus:
                try:
                    performer = session.performers.get(
                        group__chapter__name__iexact=performer_text,
                    )
                except Performer.DoesNotExist:
                    log.error("Can not find chorus: {0}".format(performer_text))
                    continue
            else:
                try:
                    performer = session.performers.get(
                        group__name__iexact=performer_text,
                    )
                except Performer.DoesNotExist:
                    log.error("Can not find quartet: {0}".format(performer_text))
                    continue
            order = int(row[3].partition(":")[2].strip())
            kind = get_round_kind(row[0])
            round = session.rounds.get(
                kind=getattr(Round.KIND, kind),
            )
            performance = Performance.objects.get(
                round=round,
                performer=performer,
                slot=order,
            )

            # Next, get the song number
            number = int(row[4].partition(":")[2].strip())

            # Next, get the song title
            title = unidecode(row[5].partition(":")[2].strip())

            chart, created = Chart.objects.get_or_create(
                title=title,
                is_generic=True,
            )

            songs.append({
                'performance': performance,
                'order': number,
                'chart': chart,
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
                kind=kind,
            )
            performer_text = unidecode(row[1].partition(":")[2].strip())

            if performer_text == '(Not Found)':
                continue

            if session.kind == Session.KIND.chorus:
                try:
                    performer = session.performers.get(
                        group__chapter__name__iexact=performer_text,
                    )
                except Performer.DoesNotExist:
                    log.error("Can not find chorus: {0}".format(performer_text))
                    continue
            else:
                try:
                    performer = session.performers.get(
                        group__name__iexact=performer_text,
                    )
                except Performer.DoesNotExist:
                    log.error("Can not find quartet: {0}".format(performer_text))
                    continue
            order = int(row[3].partition(":")[2].strip())
            kind = get_round_kind(row[0])
            round = session.rounds.get(
                kind=getattr(Round.KIND, kind),
            )
            performance = Performance.objects.get(
                round=round,
                performer=performer,
                slot=order,
            )
            number = int(row[4].partition(":")[2].strip())
            song = performance.songs.get(
                order=number,
            )

            judges = session.judges.order_by('bhs_panel_id')
            scores_raw = row[-judges.count():]
            i = 0
            for judge in judges:
                try:
                    points = int(scores_raw[i])
                except:
                    log.error("Can not parse points from panel: {0} - {1}".format(points, performance))
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
        session.rank()
        session.save()
        for contest in session.contests.all():
            contest.rank()
            contest.save()
        for round in session.rounds.all():
            round.rank()
            round.save()
    return


def calculate(convention):
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
            for contestant in performer.contestants.all():
                contestant.calculate()
                contestant.save()
    return


def chapter_district(chapter):
    if not chapter.code:
        log.error("No Chapter Code for {0}".format(chapter))
        return
    else:
        letter = chapter.code[:1]
        chapter.organization = Organization.objects.get(code=letter)


def generate_cycle(year):
    conventions = Convention.objects.filter(
        year=year - 1,
    )
    log.info(conventions)
    for convention in conventions:
        new_v, f = Convention.objects.get_or_create(
            season=convention.season,
            division=convention.division,
            year=convention.year + 1,
            organization=convention.organization
        )
        log.info("{0}, {1}".format(new_v, f))
        sessions = convention.sessions.all()
        for session in sessions:
            new_s, f = new_v.sessions.get_or_create(
                kind=session.kind,
            )
            log.info("{0}, {1}".format(new_s, f))
            rounds = session.rounds.all()
            for round in rounds:
                new_r, f = new_s.rounds.get_or_create(
                    kind=round.kind,
                    num=round.num,
                )
                log.info("{0}, {1}".format(new_r, f))
            judges = session.judges.filter(kind=Judge.KIND.official)
            for judge in judges:
                new_j, f = new_s.judges.get_or_create(
                    category=judge.category,
                    kind=judge.kind,
                    slot=judge.slot,
                )
                log.info("{0}, {1}".format(new_j, f))
            contests = session.contests.all()
            for contest in contests:
                new_c, f = new_s.contests.get_or_create(
                    award=contest.award,
                    session=contest.session,
                    cycle=contest.cycle + 1,
                    is_qualifier=contest.is_qualifier
                )
                log.info("{0}, {1}".format(new_c, f))
    return "Built {0}".format(year)


# def import_entryform(session):
#     reader = csv.reader(session.entry_form, skipinitialspace=True)
#     next(reader)
#     rows = [row for row in reader]
#     parts = ['Tenor', 'Lead', 'Baritone', 'Bass']
#     output = []
#     quartet = None
#     part = None
#     bhs_id = None
#     person = None
#     chapter = None
#     person = None
#     for row in rows:
#         entry = {}
#         if row[1]:
#             quartet = row[1]
#         if any([string in row[10] for string in parts]):
#             part = row[10].partition("-")[0].strip()
#             person = row[10].partition("-")[2].strip()
#             bhs_id = person.partition("-")[0].strip()
#             person = person.partition("-")[2].strip()
#         if not any([string in row[10] for string in parts]):
#             chapter = row[10].partition(" ")[0].strip()
#         entry['quartet'] = quartet
#         entry['part'] = part.lower()
#         entry['bhs_id'] = int(bhs_id)
#         entry['chapter'] = chapter
#         entry['person'] = person
#         output.append(entry)
#     for row in output:
#         if row['chapter']:
#             try:
#                 person = Person.objects.get(
#                     bhs_id=row['bhs_id'],
#                 )
#             except Person.DoesNotExist:
#                 try:
#                     person = Person.objects.create(
#                         bhs_id=row['bhs_id'],
#                         name=row['person'],
#                     )
#                 except IntegrityError:
#                     person = Person.objects.create(
#                         bhs_id=row['bhs_id'],
#                         name="{0} {1}".format(row['person'], row['bhs_id'])
#                     )
#             try:
#                 chapter = Chapter.objects.get(
#                     code=row['chapter']
#                 )
#             except Chapter.DoesNotExist:
#                 print row['chapter']
#             Member.objects.get_or_create(
#                 chapter=chapter,
#                 person=person,
#                 status=Member.STATUS.active,
#             )
#     for row in output:
#         if row['chapter']:
#             try:
#                 performer = Performer.objects.get(
#                     group__name=row['quartet'],
#                     session=session,
#                 )
#             except Performer.DoesNotExist:
#                 print row['quartet']
#                 continue
#             person = Person.objects.get(
#                 bhs_id=row['bhs_id'],
#             )
#             singer, created = Singer.objects.get_or_create(
#                 performer=performer,
#                 person=person,
#                 part=getattr(Singer.PART, row['part']),
#             )
#     return


def import_submission(session):
    reader = csv.reader(session.song_list, skipinitialspace=True)
    next(reader)
    rows = [row for row in reader]
    for row in rows:
        if session.kind == session.KIND.chorus:
            try:
                group = Group.objects.get(
                    status=Group.STATUS.active,
                    chapter__code=row[1],
                )
            except Group.DoesNotExist:
                raise RuntimeError("No chorus for: {0}, {1}, {2}".format(row[1], row[2], session))
            try:
                men = int(row[10])
            except ValueError:
                log.info("Can not parse men: {0}, {1}".format(row[10], group))
                men = None
        else:
            try:
                group = Group.objects.get(
                    bhs_id=row[1],
                )
            except Group.DoesNotExist:
                try:
                    group = Group.objects.create(
                        bhs_id=int(row[1]),
                        name=row[2].strip(),
                        kind=Group.KIND.quartet,
                    )
                    print "Created {0}, {1}".format(row[1], row[2],)
                except IntegrityError:
                    group = Group.objects.create(
                        bhs_id=int(row[1]),
                        name="{0} {1}".format(
                            row[2].strip(),
                            row[1]
                        ),
                        kind=Group.KIND.quartet,
                    )
                    print "Check {0} with {1}".format(
                        row[2].strip(),
                        int(row[1]),
                    )
            men = 4
        if row[11] == 'MEDLEY':
            is_medley = True
        else:
            is_medley = False
        if row[0] == '0':
            oa = None
        else:
            oa = int(row[0])
        if row[7][:1].isdigit():
            bhs_id = int(row[7].partition(' -')[0])
        else:
            bhs_id = None
        round = session.rounds.get(num=1)
        performer, c = session.performers.get_or_create(
            group=group,
        )
        if group.kind == Group.KIND.chorus:
            try:
                performer.organization = group.chapter.organization
            except AttributeError:
                pass
        performer.men = men
        performer.save()
        contests = session.contests.all()
        for contest in contests:
            Contestant.objects.get_or_create(
                performer=performer,
                contest=contest,
            )
        try:
            chart, c = Chart.objects.get_or_create(
                title=row[6],
                arranger=unidecode(row[8]),
                is_medley=is_medley,
                bhs_copyright_date=row[12],
                bhs_copyright_owner=row[13],
                bhs_id=bhs_id,
                composer=unidecode(row[14]),
                lyricist=unidecode(row[15]),
            )
        except IntegrityError:
            print "Duplicate chart: {0} {1} {2} {3}".format(
                row[6],
                unidecode(row[8]),
                bhs_id,
                performer,
            )
        Submission.objects.get_or_create(
            performer=performer,
            chart=chart,
        )
        if oa:
            performance, c = performer.performances.get_or_create(
                round=round,
                slot=oa,
            )
