# Standard Libary
import csv
import logging
from datetime import datetime

# Third-Party
import requests

# Django
from django.db import IntegrityError
from django.utils import dateparse
from django.utils import encoding

# Local
from .models import Chart
from .models import Contestant
from .models import Entry
from .models import Group
from .models import Member
from .models import Office
from .models import Officer
from .models import Person
from .models import Repertory
from .models import Session
from .models import User

log = logging.getLogger('importer')


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)


def print_headers(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        for key, value in enumerate(rows[0]):
            print(key, value)


def import_persons(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            bhs_id = int(row[0])
            prefix_name = row[1].strip()
            first_name = row[2].strip()
            middle_name = row[3].strip()
            if len(middle_name) == 1:
                middle_name = "{0}.".format(middle_name)
            last_name = row[4].strip()
            suffix_name = row[5].strip()
            nick_name = row[23].strip()
            if nick_name and (nick_name != first_name):
                nick_name = "({0})".format(nick_name)
            else:
                nick_name = None
            name = " ".join(
                map(
                    (lambda x: encoding.smart_text(x)),
                    filter(
                        None, [
                            prefix_name,
                            first_name,
                            middle_name,
                            last_name,
                            suffix_name,
                            nick_name,
                        ]
                    )
                )
            )

            spouse = row[25].strip()

            email = row[6].strip()
            if not email:
                email = None

            address1 = row[10].strip()
            city = row[14].strip()
            state = row[16].strip()
            postal_code = row[17].strip()
            country = row[15].strip()
            address = "{0}; {1}, {2}  {3}".format(
                address1,
                city,
                state,
                postal_code,
            )
            if "NULL" in address:
                address = ""

            if country == 'United States' and str(row[8]) != 'NULL':
                cell_phone = "+1{0}{1}".format(
                    str(row[8]).strip(),
                    str(row[9]).replace("-", "").strip(),
                )
            else:
                cell_phone = ""
            if country == 'United States' and str(row[19]) != 'NULL':
                home_phone = "+1{0}{1}".format(
                    str(row[19]).strip(),
                    str(row[20]).replace("-", "").strip(),
                )
            else:
                home_phone = ""

            birth_date = dateparse.parse_datetime(row[22]).date()

            try:
                part = int(row[26])
            except ValueError:
                part = None

            defaults = {
                'name': name,
                'spouse': spouse,
                'email': email,
                'birth_date': birth_date,
                'address': address,
                'cell_phone': cell_phone,
                'home_phone': home_phone,
                'part': part,
            }
            try:
                person, created = Person.objects.update_or_create(
                    bhs_id=bhs_id,
                    defaults=defaults,
                )
            except IntegrityError as e:
                log.error(e)
            log.info((person, created))


def import_chapter_membership(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            entity_id = int(row[1])
            person_id = int(row[0])
            start_date = dateparse.parse_datetime(row[3]).date()
            end_date = dateparse.parse_datetime(row[4]).date()
            if entity_id == 503858:
                # Skip Placeholder Chapter
                continue
            try:
                chapter = Entity.objects.get(bhs_id=entity_id)
            except Entity.DoesNotExist as e:
                log.error((e, row))
                continue
            try:
                person = Person.objects.get(bhs_id=person_id)
            except Person.DoesNotExist as e:
                log.error((e, row))
                continue
            defaults = {
                'start_date': start_date,
                'end_date': end_date,
                'status': Member.STATUS.active,
            }
            member, created = Member.objects.update_or_create(
                person=person,
                entity=chapter,
                defaults=defaults,
            )
            log.info((member, created))


def import_quartet_membership(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            try:
                quartet = Entity.objects.get(bhs_id=int(row[1]))
            except Entity.DoesNotExist as e:
                log.error((e, row))
                continue
            try:
                person = Person.objects.get(bhs_id=int(row[3]))
            except Person.DoesNotExist as e:
                log.error((e, row))
                continue
            try:
                start_date = dateparse.parse_datetime(row[10]).date()
            except AttributeError:
                start_date = None
            # end_date = dateparse.parse_datetime(row[11]).date()
            part = int(row[7])
            defaults = {
                'start_date': start_date,
                'end_date': None,
                'part': part,
                'status': Member.STATUS.active,
            }
            member, created = Member.objects.update_or_create(
                person=person,
                entity=quartet,
                defaults=defaults,
            )
            log.info((member, created))


def import_youth_person(
    bhs_id=None,
    first_name=None,
    last_name=None,
    birth_date=None,
    street=None,
    city=None,
    state=None,
    postal_code=None,
    country=None,
    phone=None,
    email=None,
    part=None,
):
    name = " ".join(
        map(
            (lambda x: encoding.smart_text(x)),
            filter(
                None, [
                    first_name,
                    last_name,
                ]
            )
        )
    )
    address = "{0}; {1}, {2}  {3}".format(
        street,
        city,
        state,
        postal_code,
    )

    defaults = {
        'name': name,
        'email': email,
        'birth_date': birth_date,
        'address': address,
        'cell_phone': phone,
        'part': part,
    }
    try:
        person, created = Person.objects.update_or_create(
            bhs_id=bhs_id,
            defaults=defaults,
        )
    except IntegrityError as e:
        log.error(e)
        return
    log.info((person, created))
    return person


def import_youth(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            try:
                bhs_id=int(row[13])
            except ValueError:
                bhs_id = None
            first_name=row[9].strip()
            last_name=row[10].strip()
            try:
                birth_date=dateparse.parse_datetime(row[12]).date()
            except AttributeError:
                birth_date=None
            street=row[14].strip()
            city=row[15].strip()
            state=row[16].strip()
            postal_code=row[17].strip()
            country=row[18].strip()
            phone=row[19].strip()
            email=row[20].strip()
            part=1

            name = " ".join(
                map(
                    (lambda x: encoding.smart_text(x)),
                    filter(
                        None, [
                            first_name,
                            last_name,
                        ]
                    )
                )
            )
            address = "{0}; {1}, {2}  {3}".format(
                street,
                city,
                state,
                postal_code,
            )

            defaults = {
                'name': name,
                'email': email,
                'birth_date': birth_date,
                'address': address,
                'cell_phone': phone,
                'part': part,
            }

            if bhs_id:
                tenor, created = Person.objects.update_or_create(
                    bhs_id=bhs_id,
                    defaults=defaults,
                )
            else:
                try:
                    tenor = Person.objects.get(email=email)
                except Person.DoesNotExist:
                    tenor = Person.objects.create(**defaults)

            try:
                bhs_id=int(row[25])
            except ValueError:
                bhs_id = None
            first_name=row[21].strip()
            last_name=row[22].strip()
            try:
                birth_date=dateparse.parse_datetime(row[24]).date()
            except AttributeError:
                birth_date=None
            street=row[26].strip()
            city=row[27].strip()
            state=row[28].strip()
            postal_code=row[29].strip()
            country=row[30].strip()
            phone=row[31].strip()
            email=row[32].strip()
            part=2
            name = " ".join(
                map(
                    (lambda x: encoding.smart_text(x)),
                    filter(
                        None, [
                            first_name,
                            last_name,
                        ]
                    )
                )
            )
            address = "{0}; {1}, {2}  {3}".format(
                street,
                city,
                state,
                postal_code,
            )

            defaults = {
                'name': name,
                'email': email,
                'birth_date': birth_date,
                'address': address,
                'cell_phone': phone,
                'part': part,
            }

            if bhs_id:
                lead, created = Person.objects.update_or_create(
                    bhs_id=bhs_id,
                    defaults=defaults,
                )
            else:
                try:
                    lead = Person.objects.get(email=email)
                except Person.DoesNotExist:
                    lead = Person.objects.create(**defaults)

            try:
                bhs_id=int(row[37])
            except ValueError:
                bhs_id = None
            first_name=row[33].strip()
            last_name=row[34].strip()
            try:
                birth_date=dateparse.parse_datetime(row[36]).date()
            except AttributeError:
                birth_date=None
            street=row[38].strip()
            city=row[39].strip()
            state=row[40].strip()
            postal_code=row[41].strip()
            country=row[42].strip()
            phone=row[43].strip()
            email=row[44].strip()
            part=3
            name = " ".join(
                map(
                    (lambda x: encoding.smart_text(x)),
                    filter(
                        None, [
                            first_name,
                            last_name,
                        ]
                    )
                )
            )
            address = "{0}; {1}, {2}  {3}".format(
                street,
                city,
                state,
                postal_code,
            )

            defaults = {
                'name': name,
                'email': email,
                'birth_date': birth_date,
                'address': address,
                'cell_phone': phone,
                'part': part,
            }

            if bhs_id:
                baritone, created = Person.objects.update_or_create(
                    bhs_id=bhs_id,
                    defaults=defaults,
                )
            else:
                try:
                    baritone = Person.objects.get(email=email)
                except Person.DoesNotExist:
                    baritone = Person.objects.create(**defaults)


            try:
                bhs_id=int(row[49])
            except ValueError:
                bhs_id = None
            first_name=row[45].strip()
            last_name=row[46].strip()
            try:
                birth_date=dateparse.parse_datetime(row[48]).date()
            except AttributeError:
                birth_date=None
            street=row[50].strip()
            city=row[51].strip()
            state=row[52].strip()
            postal_code=row[53].strip()
            country=row[54].strip()
            phone=row[55].strip()
            email=row[56].strip()
            part=4
            name = " ".join(
                map(
                    (lambda x: encoding.smart_text(x)),
                    filter(
                        None, [
                            first_name,
                            last_name,
                        ]
                    )
                )
            )
            address = "{0}; {1}, {2}  {3}".format(
                street,
                city,
                state,
                postal_code,
            )

            defaults = {
                'name': name,
                'email': email,
                'birth_date': birth_date,
                'address': address,
                'cell_phone': phone,
                'part': part,
            }

            if bhs_id:
                bass, created = Person.objects.update_or_create(
                    bhs_id=bhs_id,
                    defaults=defaults,
                )
            else:
                try:
                    bass = Person.objects.get(email=email)
                except Person.DoesNotExist:
                    bass = Person.objects.create(**defaults)
            try:
                quartet_id = int(row[5])
            except ValueError:
                quartet_id = None
            quartet_name = row[0].strip()
            defaults = {
                'name': quartet_name,
                'status': 10,
                'kind': 31,
                'long_name': quartet_name,
            }
            if quartet_id:
                quartet, created = Entity.objects.update_or_create(
                    bhs_id=quartet_id,
                    defaults=defaults,
                )
            else:
                quartet = Entity.objects.create(**defaults)
            office = Office.objects.get(code='QREP')
            defaults = {
                'status': 10,
            }
            Officer.objects.update_or_create(
                office=office,
                person=tenor,
                entity=quartet,
                defaults=defaults
            )
            Officer.objects.update_or_create(
                office=office,
                person=lead,
                entity=quartet,
                defaults=defaults
            )
            Officer.objects.update_or_create(
                office=office,
                person=baritone,
                entity=quartet,
                defaults=defaults
            )
            Officer.objects.update_or_create(
                office=office,
                person=bass,
                entity=quartet,
                defaults=defaults
            )
            session = Session.objects.get(
                convention__id='0887d95f-1836-455d-921a-1f3b8e966b02'
            )
            try:
                prelim = float(row[2])
            except ValueError:
                prelim = None
            entry = Entry.objects.create(
                session=session,
                entity=quartet,
                prelim=prelim,
            )

            defaults = {
                'status': 10,
                'part': 1,
            }
            tenor_m, created = Member.objects.update_or_create(
                entity=quartet,
                person=tenor,
                defaults = defaults,
            )
            defaults = {
                'status': 10,
                'part': 2,
            }
            lead_m, created = Member.objects.update_or_create(
                entity=quartet,
                person=lead,
                defaults = defaults,
            )
            defaults = {
                'status': 10,
                'part': 3,
            }
            baritone_m, created = Member.objects.update_or_create(
                entity=quartet,
                person=baritone,
                defaults = defaults,
            )
            defaults = {
                'status': 10,
                'part': 4,
            }
            bass_m, created = Member.objects.update_or_create(
                entity=quartet,
                person=bass,
                defaults = defaults,
            )
            defaults = {
                'part': 1,
            }
            Participant.objects.update_or_create(
                entry=entry,
                member=tenor_m,
            )
            defaults = {
                'part': 2,
            }
            Participant.objects.update_or_create(
                entry=entry,
                member=lead_m,
            )
            defaults = {
                'part': 3,
            }
            Participant.objects.update_or_create(
                entry=entry,
                member=baritone_m,
            )
            defaults = {
                'part': 4,
            }
            Participant.objects.update_or_create(
                entry=entry,
                member=bass_m,
            )

            try:
                chart1_id = int(row[60])
            except ValueError:
                chart1_id = None
            if chart1_id:
                chart1 = Chart.objects.get(
                    bhs_id=chart1_id,
                )
            else:
                title = row[57].strip()
                arrangers = row[58].strip()
                composers = row[59].strip()
                lyricists = row[59].strip()
                holders = row[61].strip()
                chart1 = Chart.objects.create(
                    title=title,
                    arrangers=arrangers,
                    composers=composers,
                    lyricists=lyricists,
                    holders=holders,
                    entity=quartet,
                )
            Repertory.objects.create(
                entity=quartet,
                chart=chart1,
            )
            try:
                chart2_id = int(row[65])
            except ValueError:
                chart2_id = None
            if chart2_id:
                chart2 = Chart.objects.get(
                    bhs_id=chart2_id,
                )
            else:
                title = row[62].strip()
                arrangers = row[63].strip()
                composers = row[64].strip()
                lyricists = row[64].strip()
                holders = row[66].strip()
                chart2 = Chart.objects.create(
                    title=title,
                    arrangers=arrangers,
                    composers=composers,
                    lyricists=lyricists,
                    holders=holders,
                    entity=quartet,
                )
            Repertory.objects.create(
                entity=quartet,
                chart=chart2,
            )
            #
            # try:
            #     User.objects.get(
            #         email=tenor.email,
            #     )
            # except User.DoesNotExist:
            #     User.objects.create_user(
            #         email=tenor.email,
            #         person=tenor,
            #     )
            # try:
            #     User.objects.get(
            #         email=lead.email,
            #     )
            # except User.DoesNotExist:
            #     User.objects.create_user(
            #         email=lead.email,
            #         person=lead,
            #     )
            # try:
            #     User.objects.get(
            #         email=baritone.email,
            #     )
            # except User.DoesNotExist:
            #     User.objects.create_user(
            #         email=baritone.email,
            #         person=baritone,
            #     )
            # try:
            #     User.objects.create_user(
            #         email=bass.email,
            #     )
            # except User.DoesNotExist:
            #     User.objects.create_user(
            #         email=bass.email,
            #         person=bass,
            #     )


def import_charts(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            defaults = {
                'title': row[0],
                'arrangers': row[1],
                'composers': row[2],
                'lyricists': row[3],
                'holders': row[4],
                'status': 10,
            }
            try:
                Chart.objects.create(**defaults)
            except Exception as e:
                print(e, row)
                continue


def import_aff_membership(path, entity):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            email = row[1].strip()
            # dob = dateparse.parse_date(row[2])
            cell_phone = row[2]
            name = row[0].strip()
            person, created = Person.objects.get_or_create(
                email=email,
            )
            person.full_name = name
            person.email = email
            person.cell_phone = cell_phone
            person.location = 'AUS'
            person.save()
            defaults = {'status': 10}
            Member.objects.update_or_create(
                entity=entity,
                person=person,
                defaults=defaults,
            )


def import_chorus_competitors(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        session = Session.objects.get(
            kind=Session.KIND.chorus,
            convention__entity__code='BHS',
            convention__year=2017,
        )
        contest = session.contests.first()
        rows = [row for row in reader]
        for row in rows:
            try:
                chorus_id = int(row[6])
            except ValueError as e:
                continue
            try:
                chorus = Entity.objects.get(bhs_id=chorus_id)
            except Entity.DoesNotExist as e:
                print((e, chorus_id))
                continue
            director_email = row[4].strip()
            codirector_email = row[5].strip()
            if director_email:
                try:
                    director = Person.objects.get(email=director_email)
                except Person.DoesNotExist:
                    director = None
                except Person.MultipleObjectsReturned:
                    director = None
            else:
                director = None
            if codirector_email:
                try:
                    codirector = Person.objects.get(email=codirector_email)
                except Person.DoesNotExist:
                    codirector = None
                except Person.MultipleObjectsReturned:
                    codirector = None
            else:
                codirector = None
            defaults = {
                'director': director,
                'codirector': codirector,
                'is_evaluation': False,
                'is_private': False,
            }
            entry, meta = Entry.objects.update_or_create(
                session=session,
                entity=chorus,
                defaults=defaults,
            )
            contestant, meta = Contestant.objects.update_or_create(
                contest=contest,
                entry=entry,
            )
    return


def import_quartet_competitors(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        session = Session.objects.get(
            kind=Session.KIND.quartet,
            convention__entity__code='BHS',
            convention__year=2017,
            num_rounds=3,
        )
        contest = session.contests.get(
            award__name='International Quartet Championship',
        )
        rows = [row for row in reader]
        for row in rows:
            try:
                quartet_id = int(row[0])
            except ValueError as e:
                continue
            try:
                quartet = Entity.objects.get(bhs_id=quartet_id)
            except Entity.DoesNotExist as e:
                print((e, quartet_id))
                continue
            prelim = float(row[1])
            rep_id = row[2].strip()
            rep = Entity.objects.get(
                kind=Entity.KIND.district,
                code=rep_id,
            )
            try:
                tenor = Person.objects.get(bhs_id=int(row[3]))
            except Person.DoesNotExist:
                tenor = None
                print('missing')
            try:
                lead = Person.objects.get(bhs_id=int(row[4]))
            except Person.DoesNotExist:
                lead = None
                print('missing')
            try:
                baritone = Person.objects.get(bhs_id=int(row[5]))
            except Person.DoesNotExist:
                baritone = None
                print('missing')
            try:
                bass = Person.objects.get(bhs_id=int(row[6]))
            except Person.DoesNotExist:
                bass = None
                print('missing')
            defaults = {
                'prelim': prelim,
                'representing': rep,
                'tenor': tenor,
                'lead': lead,
                'baritone': baritone,
                'bass': bass,
                'is_evaluation': False,
                'is_private': False,
            }
            entry, meta = Entry.objects.update_or_create(
                session=session,
                entity=quartet,
                defaults=defaults,
            )
            contestant, meta = Contestant.objects.update_or_create(
                contest=contest,
                entry=entry,
            )
    return


def import_aff_competitors(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        session = Session.objects.get(
            kind=Session.KIND.quartet,
            convention__entity__code='BHS',
            convention__year=2017,
            num_rounds=3,
        )
        contest = session.contests.get(
            award__name='International Quartet Championship',
        )
        rows = [row for row in reader]
        for row in rows:
            try:
                quartet_id = int(row[0])
            except ValueError as e:
                continue
            try:
                quartet = Entity.objects.get(bhs_id=quartet_id)
            except Entity.DoesNotExist as e:
                print((e, quartet_id))
                continue
            rep_id = row[2].strip()
            try:
                rep = Entity.objects.get(
                    kind=Entity.KIND.affiliate,
                    code=rep_id,
                )
            except Entity.DoesNotExist as e:
                print((e, rep_id))
            try:
                tenor = quartet.members.filter(part=1).first().person
            except Person.DoesNotExist:
                tenor = None
                print('missing')
            try:
                lead = quartet.members.filter(part=2).first().person
            except Person.DoesNotExist:
                lead = None
                print('missing')
            try:
                baritone = quartet.members.filter(part=3).first().person
            except Person.DoesNotExist:
                baritone = None
                print('missing')
            try:
                bass = quartet.members.filter(part=4).first().person
            except Person.DoesNotExist:
                bass = None
                print('missing')
            defaults = {
                'representing': rep,
                'tenor': tenor,
                'lead': lead,
                'baritone': baritone,
                'bass': bass,
                'is_evaluation': False,
                'is_private': False,
            }
            entry, meta = Entry.objects.update_or_create(
                session=session,
                entity=quartet,
                defaults=defaults,
            )
            contestant, meta = Contestant.objects.update_or_create(
                contest=contest,
                entry=entry,
            )
    return


# def import_membership(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             try:
#                 person = Person.objects.get(bhs_id=int(row[0]))
#             except Person.DoesNotExist as e:
#                 log.error(e)
#                 continue
#             bhs = Entity.objects.get(code='BHS')
#             try:
#                 start_date = dateparse.parse_datetime(row[57]).date()
#             except AttributeError:
#                 start_date = None
#             try:
#                 end_date = dateparse.parse_datetime(row[58]).date()
#             except AttributeError:
#                 end_date = None
#             defaults = {
#                 'start_date': start_date,
#                 'end_date': end_date,
#                 'status': Member.STATUS.active,
#             }
#             member, created = Member.objects.update_or_create(
#                 person=person,
#                 entity=bhs,
#                 defaults=defaults,
#             )
#             log.info((member, created))
#

def import_chapter_officers(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            office_name = row[11]
            chapter_id = int(row[9])
            person_id = int(row[3])
            try:
                office = Office.objects.get(name=office_name)
            except Office.DoesNotExist as e:
                log.error((e, office_name))
                continue
            try:
                chapter = Entity.objects.get(bhs_id=chapter_id)
            except Entity.DoesNotExist as e:
                log.error((e, chapter_id))
                continue
            try:
                person = Person.objects.get(bhs_id=person_id)
            except Person.DoesNotExist as e:
                log.error((e, person_id))
                continue
            start_date = dateparse.parse_datetime(row[6]).date()
            end_date = dateparse.parse_datetime(row[7]).date()
            defaults = {
                'start_date': start_date,
                'end_date': end_date,
                'status': Officer.STATUS.active,
            }
            officer, created = Officer.objects.update_or_create(
                person=person,
                entity=chapter,
                office=office,
                defaults=defaults,
            )
            log.info((officer, created))


def import_quartet_reps(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            office = Office.objects.get(code='QREP')
            try:
                quartet = Entity.objects.get(bhs_id=int(row[1]))
            except Entity.DoesNotExist as e:
                continue
            try:
                person = Person.objects.get(bhs_id=int(row[3]))
            except Person.DoesNotExist as e:
                continue
            if int(row[9]) != 1:
                continue
            defaults = {
                'status': Officer.STATUS.active,
            }
            officer, created = Officer.objects.update_or_create(
                person=person,
                entity=quartet,
                office=office,
                defaults=defaults,
            )
            log.info((officer, created))


def import_db_quartets(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        parent = Entity.objects.get(code='FHT')
        for row in rows:
            bhs_id = int(row[1])
            name = row[2].strip()
            defaults = {
                'name': name,
                'parent': parent,
                'kind': Entity.KIND.quartet,
            }
            quartet, created = Entity.objects.update_or_create(
                bhs_id=bhs_id,
                defaults=defaults,
            )
            log.info((quartet, created))


def import_db_chapters(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            bhs_id = int(row[1])
            try:
                chapter = Entity.objects.get(bhs_id=bhs_id)
                continue
            except Entity.DoesNotExist:
                pass
            raw = row[2].strip()
            if raw == 'Z000 Placeholder Chapter':
                continue
            code = raw.partition(" ")[0]
            long_name = raw.partition(" ")[2]
            try:
                parent = Entity.objects.get(code=raw[:1])
            except Entity.DoesNotExist:
                log.error(raw)
            name = "{0} Chorus".format(long_name)
            defaults = {
                'name': name,
                'long_name': long_name,
                'parent': parent,
                'kind': Entity.KIND.chorus,
            }
            chapter, created = Entity.objects.update_or_create(
                bhs_id=bhs_id,
                defaults=defaults,
            )
            log.info((chapter, created))


def import_db_member_persons(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            bhs_id = int(row[0])
            first_name = row[2].strip()
            nick_name = row[48].strip()
            if nick_name:
                if nick_name != first_name:
                    nick_name = "({0})".format(nick_name)
            else:
                nick_name = None
            middle_name = row[3].strip()
            last_name = row[4].strip()
            suffix_name = row[5].strip()
            prefix_name = row[1].strip()
            name = " ".join(
                map(
                    (lambda x: encoding.smart_text(x)),
                    filter(
                        None, [
                            prefix_name,
                            first_name,
                            middle_name,
                            last_name,
                            suffix_name,
                            nick_name,
                        ]
                    )
                )
            )
            email = row[16].strip()
            spouse = row[50].strip()
            address1 = row[69].strip()
            address2 = row[70].strip()
            city = row[72].strip()
            state = row[73].strip()
            postal_code = row[74].strip()
            country = row[75].strip()
            if country == 'United States' and str(row[39]) != 'NULL':
                phone = "+1{0}{1}".format(
                    str(row[39]).strip(),
                    str(row[40]).replace("-", "").strip(),
                )
            else:
                phone = ""
            birth_date = dateparse.parse_datetime(row[47]).date()
            address = "{0}; {2}, {3}  {4}".format(
                address1,
                address2,
                city,
                state,
                postal_code,
            )
            if "NULL" in address:
                address = ""
            defaults = {
                'name': name,
                'email': email,
                'spouse': spouse,
                'address': address,
                'phone': phone,
                'birth_date': birth_date,
            }
            person, created = Person.objects.update_or_create(
                bhs_id=bhs_id,
                defaults=defaults,
            )
            log.info((person, created))


def import_db_quartet_persons(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            if int(row[3]) == 1:
                continue
            bhs_id = int(row[3])
            name = row[4].strip()
            birth_date = dateparse.parse_datetime(row[5]).date()
            email = row[14].strip()
            defaults = {
                'name': name,
                'email': email,
                'birth_date': birth_date,
            }
            person, created = Person.objects.update_or_create(
                bhs_id=bhs_id,
                defaults=defaults,
            )
            log.info((person, created))


def import_music_catalog(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        # Extract
        items = []
        for row in rows:
            extract = {}
            try:
                extract['bhs_id'] = int(row[0])
            except ValueError as e:
                log.error(e)
                continue
            extract['title'] = row[1]
            if row[7] == 'NULL':
                extract['composers'] = ''
            else:
                extract['composers'] = row[7]
            if row[8] == 'NULL':
                extract['lyricists'] = ''
            else:
                extract['lyricists'] = row[8]
            if row[10] == 'NULL':
                extract['holders'] = ''
            else:
                extract['holders'] = row[10]
            if row[20] == 'NULL':
                extract['arrangers'] = ''
            else:
                extract['arrangers'] = row[20]
            items.append(extract)
    bhs = Entity.objects.get(code='BHS')
    for item in items:
        chart, created = Chart.objects.get_or_create(bhs_id=item['bhs_id'], entity=bhs)
    for item in items:
        chart = Chart.objects.get(bhs_id=item['bhs_id'])
        if item['title'] not in chart.title:
            chart.title = item['title']
        if item['composers'] not in chart.composers:
            chart.composers = item['composers']
        if item['lyricists'] not in chart.lyricists:
            chart.lyricists = item['lyricists']
        if item['holders'] not in chart.holders:
            chart.holders = item['holders']
        if item['arrangers'] not in chart.arrangers:
            chart.arrangers = item['arrangers']
        chart.save()


def extract_arrangers(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        # Extract
        original = []
        for row in rows:
            extract = {}
            extract['arr_id'] = row[19]
            extract['arr_name'] = row[20]
            try:
                extract['arr_rata'] = float(row[21])
            except ValueError:
                extract['arr_rata'] = None
            extract['code'] = row[22]
            original.append(extract)
    result = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in original)]
    return result



def create_db_chart(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            chart = {}
            chart['bhs_id'] = int(row[0])
            chart['announced'] = dateparse.parse_date(row[1])
            chart['title'] = row[2].strip()
            chart['arrangers'] = row[3].strip() if row[3].strip() else "(Unknown)"
            try:
                chart['bhs_fee'] = int(row[4])
            except ValueError:
                chart['bhs_fee'] = None
            chart['difficulty'] = int(row[5]) if row[5] else None
            chart['tempo'] = int(row[6]) if row[6] else None
            chart['is_medley'] = True if row[7] == 'True' else False
            chart['gender'] = 1
            chart['voicing'] = 1
            Chart.objects.create(
                **chart
            )



def import_judge_roster(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        rows = [row for row in reader]
        for row in rows:
            try:
                person = Person.objects.get(
                    bhs_id=int(row[1]),
                )
            except Person.DoesNotExist:
                log.error('Can not find person for {0} {1}'.format(row[2], row[1]))
                continue
            spouse = row[2].partition("(")[2].partition(")")[0]
            address = "{0}; {1}".format(row[3], row[4])
            email = row[5]
            home_phone = row[7].partition("h")[2]
            work_phone = row[8].partition("w")[2]
            cell_phone = row[9].partition("c")[2]
            airports = []
            if row[11]:
                airports.append(row[11])
            if row[12]:
                airports.append(row[12])
            if row[13]:
                airports.append(row[13])
            if row[14]:
                airports.append(row[14])
            person.spouse = spouse
            person.address = address
            person.email = email
            person.home_phone = home_phone
            person.work_phone = work_phone
            person.cell_phone = cell_phone
            person.airports = airports
            person.save()
            try:
                district = Entity.objects.get(
                    code=row[10],
                    kind__in=[
                        Entity.KIND.district,
                        Entity.KIND.affiliate,
                    ]
                )
            except Entity.DoesNotExist:
                log.error('Can not find district for {0} {1}'.format(row[2], row[1]))
                continue
            status = row[15]
            if status == 'Certified':
                status = 10
            else:
                status = 0
            category = row[0]
            if category == 'MUS':
                office = Office.objects.get(name='Society C&J Music Judge')
            elif category == 'PER':
                office = Office.objects.get(name='Society C&J Performance Judge')
            elif category == 'SNG':
                office = Office.objects.get(name='Society C&J Singing Judge')
            elif category == 'ADM':
                office = Office.objects.get(name='Society C&J Administrator')
            elif category == 'DRCJ':
                continue
            else:
                log.error("Can't find category for {0}".format(row[0]))
            try:
                yos = int(row[6])
            except ValueError:
                yos = 0
            year = 2017 - yos
            start_date = datetime(year, 7, 1)
            officer = {
                'person': person,
                'office': office,
                'entity': district,
                'start_date': start_date,
                'status': status,
            }
            Officer.objects.create(**officer)


def import_db_offices(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            office = {}
            office['name'] = row[2]
            office['status'] = int(row[3])
            office['kind'] = int(row[4])
            office['code'] = row[5]
            office['long_name'] = row[6]
            Office.objects.create(**office)


def import_db_internationals(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            international = {}
            international['name'] = row[4]
            international['status'] = int(row[5])
            international['kind'] = int(row[7])
            international['code'] = row[10]
            international['long_name'] = row[11]
            international['start_date'] = dateparse.parse_date(row[13])
            international['location'] = row[15]
            international['website'] = row[16]
            international['facebook'] = row[17]
            international['twitter'] = row[18]
            international['email'] = row[19]
            international['phone'] = row[20]
            international['picture'] = row[21]
            international['description'] = row[22]
            international['bhs_id'] = int(row[24])
            international['parent'] = None
            Entity.objects.create(**international)


def import_db_districts(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        parent = Entity.objects.get(code='BHS')
        for row in rows:
            district = {}
            district['name'] = row[4]
            district['status'] = int(row[5])
            district['kind'] = int(row[7])
            district['code'] = row[10]
            district['long_name'] = row[11]
            district['code'] = row[12]
            district['start_date'] = dateparse.parse_date(row[13])
            district['location'] = row[15]
            district['website'] = row[16]
            district['facebook'] = row[17]
            district['twitter'] = row[18]
            district['email'] = row[19]
            district['phone'] = row[20]
            district['picture'] = row[21]
            district['description'] = row[22]
            try:
                district['bhs_id'] = int(row[24])
            except ValueError:
                district['bhs_id'] = None
            district['parent'] = parent
            Entity.objects.create(**district)


def import_db_divisions(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            division = {}
            division['name'] = row[4]
            division['status'] = int(row[5])
            division['kind'] = int(row[7])
            division['code'] = row[10]
            division['long_name'] = row[11]
            division['code'] = row[12]
            division['start_date'] = dateparse.parse_date(row[13])
            division['location'] = row[15]
            division['website'] = row[16]
            division['facebook'] = row[17]
            division['twitter'] = row[18]
            division['email'] = row[19]
            division['phone'] = row[20]
            division['picture'] = row[21]
            division['description'] = row[22]
            try:
                division['bhs_id'] = int(row[24])
            except ValueError:
                division['bhs_id'] = None
            parent = Entity.objects.get(
                kind=11,
                code=row[4].split()[0]
            )
            division['parent'] = parent
            Entity.objects.create(**division)


# def import_db_members(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         rows = [row for row in reader]
#         for row in rows:
#             if int(row[2]) != 2:
#                 continue
#             chapter_id = int(row[0])
#             person_id = int(row[1])
#             try:
#                 p = Person.objects.get(
#                     bhs_id=person_id,
#                 )
#             except Person.DoesNotExist:
#                 print 'No Person'
#                 continue
#             try:
#                 c = Chapter.objects.get(
#                     bhs_id=chapter_id,
#                 )
#             except Chapter.DoesNotExist:
#                 print 'No Chapter {0}'.format(chapter_id)
#                 continue
#             start = dateparse.parse_date(row[3])
#             end = dateparse.parse_date(row[4])
#             try:
#                 mem, create = Member.objects.get_or_create(
#                     person=p,
#                     chapter=c,
#                 )
#             except IntegrityError:
#                 print "Integrity {0} - {1}".format(c, p)
#                 continue
#             mem.start_date = start
#             mem.end_date = end
#             mem.save()
#     return "Finished"


# def import_db_quartets(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             if int(row[4]) == 3:
#                 name = row[2].strip()
#                 if name.endswith(', The'):
#                     name = "The " + name.partition(', The')[0]
#                 try:
#                     created = False
#                     g = Group.objects.get(
#                         bhs_id=int(row[0]),
#                     )
#                 except Group.DoesNotExist:
#                     bhs_id = int(row[0])
#                     try:
#                         g, created = Group.objects.get_or_create(
#                             bhs_id=bhs_id,
#                             name=encoding.smart_text(name),
#                         )
#                     except UnicodeDecodeError:
#                         continue
#             else:
#                 continue
#             print g, created


# def import_db_districts(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             if int(row[4]) == 3:
#                 name = row[2].strip()
#                 if name.endswith(', The'):
#                     name = "The " + name.partition(', The')[0]
#                 try:
#                     created = False
#                     g = Group.objects.get(
#                         bhs_id=int(row[0]),
#                     )
#                 except Group.DoesNotExist:
#                     bhs_id = int(row[0])
#                     try:
#                         g, created = Group.objects.get_or_create(
#                             bhs_id=bhs_id,
#                             name=encoding.smart_text(name),
#                         )
#                     except UnicodeDecodeError:
#                         continue
#             else:
#                 continue
#             print g, created


# def import_db_chapters(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             if int(row[4]) == 4:
#                 code = row[1].strip()
#                 name = row[2].partition(" ")[2].strip()
#                 try:
#                     created = False
#                     c = Chapter.objects.get(
#                         bhs_id=int(row[0]),
#                     )
#                 except Chapter.DoesNotExist:
#                     bhs_id = int(row[0])
#                     try:
#                         c, created = Chapter.objects.get_or_create(
#                             bhs_id=bhs_id,
#                             code=code,
#                             name=encoding.smart_text(name),
#                         )
#                     except UnicodeDecodeError:
#                         continue
#                     except IntegrityError:
#                         exist = Chapter.objects.get(
#                             code=code,
#                         )
#                         exist.bhs_id = bhs_id
#                         exist.save()
#                         created = 'UPDATED'
#             else:
#                 continue
#             print c, created


# def import_db_roles(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             if int(row[12]) not in [1, 2, 3, 4]:
#                 continue
#             try:
#                 group = Group.objects.get(
#                     bhs_id=int(row[1])
#                 )
#             except Group.DoesNotExist:
#                 log.error("Missing Group {0}: {1}".format(row[1], row[2]))
#                 continue
#             if group.KIND == Group.KIND.chorus:
#                 log.error("Chorus, not Quartet {0}: {1}".format(row[1], row[2]))
#                 continue
#             try:
#                 person = Person.objects.get(
#                     bhs_id=int(row[3])
#                 )
#             except Person.DoesNotExist:
#                 person = Person.objects.create(
#                     name=encoding.smart_text(row[4]),
#                     bhs_id=int(row[3]),
#                 )
#             if int(row[12]) == 1:
#                 part = Role.PART.tenor
#             elif int(row[12]) == 2:
#                 part = Role.PART.lead
#             elif int(row[12]) == 3:
#                 part = Role.PART.baritone
#             elif int(row[12]) == 4:
#                 part = Role.PART.bass
#             else:
#                 log.error("No Part: {0}".format(row[12]))
#                 continue
#             lower = dateparse.parse_date(row[7])
#             if not row[8]:
#                 upper = None
#             else:
#                 upper = dateparse.parse_date(row[8])
#             date = DateRange(
#                 lower=lower,
#                 upper=upper,
#                 bounds="[)",
#             )
#             if upper and lower:
#                 if lower > upper:
#                     date = None
#             role = {
#                 'bhs_id': int(row[0]),
#                 'group': group,
#                 'person': person,
#                 'date': date,
#                 'part': part,
#             }
#             try:
#                 role, created = Role.objects.get_or_create(
#                     **role
#                 )
#             except Role.MultipleObjectsReturned:
#                 log.error("Multi Roles: {1}".format(group))
#                 continue
#             print role


# def import_db_participants(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             if int(row[5]) != 38:
#                 continue
#             else:
#                 part = Role.PART.director
#             groups = Group.objects.filter(
#                 chapter__bhs_id=int(row[1]),
#                 status=Group.STATUS.active,
#                 kind=Group.KIND.chorus,
#             )
#             if groups.count() > 1:
#                 log.error("Too many groups {0}: {1}".format(row[1], row[2]))
#                 continue
#             elif groups.count() == 0:
#                 group = Group.objects.filter(
#                     chapter__bhs_id=int(row[1])
#                 ).first()
#                 if not group:
#                     try:
#                         chapter = Chapter.objects.get(bhs_id=int(row[1]))
#                     except Chapter.DoesNotExist:
#                         log.error("No chapter {0}: {1}".format(row[1], row[2]))
#                         continue
#                     group, c = Group.objects.get_or_create(
#                         chapter=chapter,
#                         status=Group.STATUS.inactive,
#                         name=row[2].strip(),
#                         kind=Group.KIND.chorus,
#                     )
#             else:
#                 group = groups.first()
#             if group.kind != Group.KIND.chorus:
#                 log.error("Not a chorus {0}: {1}".format(row[1], row[2]))
#                 continue
#             try:
#                 person = Person.objects.get(
#                     bhs_id=(row[3])
#                 )
#             except Person.DoesNotExist:
#                 log.error("Missing Person {0}: {1} for {2} {3}".format(
#                     row[3],
#                     row[4],
#                     row[1],
#                     row[2],
#                 ))
#                 continue
#             lower = dateparse.parse_date(row[7])
#             if not row[8]:
#                 upper = None
#             else:
#                 upper = dateparse.parse_date(row[8])
#             if lower < upper:
#                 date = DateRange(
#                     lower=lower,
#                     upper=upper,
#                     bounds="[)",
#                 )
#             else:
#                 log.error("Date out of sequence: {0} {1}".format(
#                     row[7],
#                     row[8],
#                 ))
#                 date = None
#             role = {
#                 'bhs_id': int(row[0]),
#                 'group': group,
#                 'person': person,
#                 'date': date,
#                 'part': part,
#             }
#             try:
#                 role, created = Role.objects.get_or_create(
#                     **role
#                 )
#             except Role.MultipleObjectsReturned:
#                 log.error("ERROR: Multi Roles: {1}".format(role))
#                 continue
#             print role
#         return


# def import_db_entries(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             convention_bhs_id = int(row[3])
#             group_bhs_id = int(row[2])
#             soa = int(row[6]) if int(row[6]) else None
#             try:
#                 convention = Convention.objects.get(
#                     bhs_id=convention_bhs_id,
#                 )
#             except Convention.DoesNotExist:
#                 log.error("No Convention: {0}".format(row[3]))
#                 continue
#             try:
#                 group = Group.objects.get(
#                     bhs_id=group_bhs_id,
#                 )
#             except Group.DoesNotExist:
#                 try:
#                     chapter = Chapter.objects.get(code=row[1][:4])
#                     groups = chapter.groups.filter(status=Group.STATUS.active)
#                     if groups.count() == 1:
#                         group = groups.first()
#                         group.bhs_id = group_bhs_id
#                         group.save()
#                     else:
#                         log.error("No Group: {0}, {1}".format(row[2], row[1]))
#                         continue
#                 except Chapter.DoesNotExist:
#                     log.error("No Group: {0}, {1}".format(row[2], row[1]))
#             if row[7].strip() == 'Normal Evaluation and Coaching':
#                 is_evaluation = True
#             else:
#                 is_evaluation = False
#             try:
#                 session = convention.sessions.get(
#                     kind=group.kind,
#                 )
#             except Session.DoesNotExist:
#                 try:
#                     session = convention.sessions.get(
#                         kind=Session.KIND.youth,
#                     )
#                 except Session.DoesNotExist:
#                     log.error("No Session: {0}, {1} - {2}".format(convention, group, group.get_kind_display()))
#                     continue
#             entry, created = Entry.objects.get_or_create(
#                 session=session,
#                 group=group,
#             )
#             entry.soa = soa
#             entry.is_evaluation = is_evaluation
#             entry.bhs_id = int(row[0])
#             entry.save()


# def import_db_representing(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             name = row[11].strip()
#             if name == 'Div I':
#                 name = 'Division I Division'
#             elif name == 'Div II':
#                 name = 'Division II Division'
#             elif name == 'Div III':
#                 name = 'Division III Division'
#             elif name == 'Div IV':
#                 name = 'Division IV Division'
#             elif name == 'Div V':
#                 name = 'Division V Division'
#             elif name == 'Arizona  Division':
#                 name = 'Arizona Division'
#             elif name == 'Division One':
#                 name = 'Division One Division'
#             elif name == 'Granite & Pine Division':
#                 name = 'Granite and Pine Division'
#             if name != 'NULL':
#                 convention = Convention.objects.get(
#                     bhs_id=int(row[3]),
#                 )
#                 district_name = convention.international.code
#                 try:
#                     international = International.objects.get(
#                         name="{0} {1}".format(
#                             district_name,
#                             name,
#                         )
#                     )
#                 except International.DoesNotExist:
#                     log.error("Bad Div: {0} {1}".format(district_name, name))
#                     continue
#                 try:
#                     entry = Entry.objects.get(
#                         bhs_id=int(row[0]),
#                     )
#                 except Entry.DoesNotExist:
#                     log.error("Can't find entry")
#                     continue
#                 entry.representing = international
#                 entry.save()


# def import_db_contests(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             convention_bhs_id = int(row[3])
#             entry_bhs_id = int(row[0])
#             try:
#                 convention = Convention.objects.get(
#                     bhs_id=convention_bhs_id,
#                 )
#             except Convention.DoesNotExist:
#                 log.error("No Convention: {0}".format(row[3]))
#                 continue
#             name = row[8].strip()
#             try:
#                 entry = Entry.objects.get(
#                     bhs_id=entry_bhs_id,
#                 )
#             except Entry.DoesNotExist:
#                 log.error("Can't find entry")
#                 continue
#             try:
#                 session = convention.sessions.get(
#                     kind=entry.group.kind,
#                 )
#             except Session.DoesNotExist:
#                 try:
#                     session = convention.sessions.get(
#                         kind=Session.KIND.youth,
#                     )
#                 except Session.DoesNotExist:
#                     try:
#                         session = convention.sessions.get(
#                             kind=Session.KIND.seniors,
#                         )
#                     except Session.DoesNotExist:
#                         log.error("No Session: {0}, {1} - {2}".format(
#                             convention,
#                             entry.group,
#                             entry.group.get_kind_display(),
#                         ))
#                         continue
#             if not entry.representing:
#                 log.error("No representation for {0}".format(entry))
#                 continue
#             international = entry.representing
#             if international.level == International.LEVEL.district:
#                 district = international
#                 division = None
#             elif international.level == International.LEVEL.division:
#                 district = international.parent
#                 division = international
#             else:
#                 log.error("Bad Rep: {0} {1}".format(
#                     entry,
#                     international,
#                 ))
#                 continue
#             excludes = [
#                 "International Srs Qt - Oldest Singer",
#             ]
#             if any([string in name for string in excludes]):
#                 continue
#             if name == 'Scores for Evaluation Only':
#                 entry.status = Entry.STATUS.evaluation
#                 entry.save()
#                 continue
#             name = name.replace("Most Improved", "Most-Improved")
#             try:
#                 award = Award.objects.get(
#                     international=entry.representing,
#                     stix_name__endswith=name,
#                 )
#             except Award.DoesNotExist:
#                 if 'International Preliminary Quartet' in name:
#                     award = Award.objects.get(
#                         name='International Quartet',
#                     )
#                 elif 'International Preliminary Youth Qt' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.international,
#                         kind=Award.KIND.youth,
#                     )
#                 elif 'International Preliminary Seniors Qt' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.international,
#                         kind=Award.KIND.seniors,
#                     )
#                 elif 'Quartet District Qualification' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.quartet,
#                         international=district,
#                     )
#                 elif 'International Seniors Quartet' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.international,
#                         kind=Award.KIND.seniors,
#                     )
#                 elif 'International Srs Qt - Oldest Qt' in name:
#                     award = Award.objects.get(
#                         name='International Oldest Seniors'
#                     )
#                 elif 'Seniors Qt District Qualification (Overall)' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.seniors,
#                         international=district,
#                     )
#                 elif 'District Super Seniors Quartet' in name:
#                     award = Award.objects.get(
#                         name='Far Western District Super Seniors'
#                     )
#                 elif 'Out Of District Qt Prelims (2 Rounds)' in name:
#                     award = Award.objects.get(
#                         name='International Quartet',
#                     )
#                 elif 'Out of Division Quartet (Score)' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.quartet,
#                         international=district,
#                     )
#                 elif 'Out Of Division Seniors Quartet' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.seniors,
#                         international=district,
#                     )
#                 elif 'Out Of Division Quartet (Overall)' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.quartet,
#                         international=district,
#                     )
#                 elif 'International Chorus' == name:
#                     award = Award.objects.get(
#                         name='International Chorus',
#                     )
#                 elif 'International Preliminary Chorus' == name:
#                     award = Award.objects.get(
#                         name='International Chorus',
#                     )
#                 elif 'Chorus District Qualification' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.chorus,
#                         international=district,
#                     )
#                 elif 'Most-Improved Chorus' in name:
#                     award = Award.objects.get(
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.chorus,
#                         international=district,
#                         is_improved=True,
#                     )
#                 elif 'Out Of Division Chorus' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.chorus,
#                         international=district,
#                     )
#                 elif 'Plateau A (or 1) Chorus' == name:
#                     if row[4] == 'Division Only':
#                         international = division
#                         level = Award.LEVEL.division
#                     else:
#                         international = district
#                         level = Award.LEVEL.district
#                     if "Improved" in name:
#                         is_improved = True
#                     else:
#                         is_improved = False
#                     award = Award.objects.get(
#                         Q(
#                             stix_name__contains='Plateau A ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau 1 ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau I ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ),
#                     )
#                 elif 'Plateau AA (or 2) Chorus' == name:
#                     if row[4] == 'Division Only':
#                         international = division
#                         level = Award.LEVEL.division
#                     else:
#                         international = district
#                         level = Award.LEVEL.district
#                     if "Improved" in name:
#                         is_improved = True
#                     else:
#                         is_improved = False
#                     award = Award.objects.get(
#                         Q(
#                             stix_name__contains='Plateau AA ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau 2 ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau II ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ),
#                     )
#                 elif 'Plateau AAA (or 3) Chorus' == name:
#                     if row[4] == 'Division Only':
#                         international = division
#                         level = Award.LEVEL.division
#                     else:
#                         international = district
#                         level = Award.LEVEL.district
#                     if "Improved" in name:
#                         is_improved = True
#                     else:
#                         is_improved = False
#                     award = Award.objects.get(
#                         Q(
#                             stix_name__contains='Plateau AAA ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau 3 ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau III ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ),
#                     )
#                 elif 'Plateau AAAA (or 4) Chorus' == name:
#                     if row[4] == 'Division Only':
#                         international = division
#                         level = Award.LEVEL.division
#                     else:
#                         international = district
#                         level = Award.LEVEL.district
#                     if "Improved" in name:
#                         is_improved = True
#                     else:
#                         is_improved = False
#                     award = Award.objects.get(
#                         Q(
#                             stix_name__contains='Plateau AAAA ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau 4 ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau IV ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             international=international,
#                             is_improved=is_improved,
#                         ),
#                     )
#                 elif 'Division Quartet' == name:
#                     if not division:
#                         log.error("Div with no Div: {0}".format(entry))
#                         continue
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.division,
#                         kind=Award.KIND.quartet,
#                         international=division,
#                     )
#                 else:
#                     log.error(
#                         "No Award: {0}, {1} {2}".format(
#                             name,
#                             district,
#                             division,
#                         )
#                     )
#                     continue
#             except Award.MultipleObjectsReturned:
#                 log.error("Multiawards")
#                 continue
#             contest, foo = session.contests.get_or_create(
#                 award=award,
#             )
#             contestant, created = Contestant.objects.get_or_create(
#                 contest=contest,
#                 entry=entry,
#             )
#             print contestant, created


# def update_panel_size(convention):
#     for session in convention.sessions.all():
#         session.size = session.assignments.filter(
#             kind=Assignment.KIND.official,
#             category=Assignment.CATEGORY.music,
#         ).count()
#         session.save()
#     return


# def denormalize(convention):
#     for session in convention.sessions.all():
#         for entry in session.entries.all():
#             for appearance in entry.appearances.all():
#                 for song in appearance.songs.all():
#                     song.calculate()
#                     song.save()
#                 appearance.calculate()
#                 appearance.save()
#             entry.calculate()
#             entry.save()
#         for contest in session.contests.all():
#             contest.rank()
#             contest.save()
#     return


# def rank(convention):
#     for session in convention.sessions.all():
#         session.rank()
#         session.save()
#         for contest in session.contests.all():
#             contest.rank()
#             contest.save()
#         for round in session.rounds.all():
#             round.rank()
#             round.save()
#     return


# def calculate(convention):
#     for session in convention.sessions.all():
#         for entry in session.entries.all():
#             for appearance in entry.appearances.all():
#                 for song in appearance.songs.all():
#                     song.calculate()
#                     song.save()
#                 appearance.calculate()
#                 appearance.save()
#             entry.calculate()
#             entry.save()
#             for contestant in entry.contestants.all():
#                 contestant.calculate()
#                 contestant.save()
#     return


# def chapter_district(chapter):
#     if not chapter.code:
#         log.error("No Chapter Code for {0}".format(chapter))
#         return
#     else:
#         letter = chapter.code[:1]
#         chapter.international = International.objects.get(code=letter)


# def generate_cycle(year):
    # conventions = Convention.objects.filter(
    #     year=year - 1,
    # )
    # log.info(conventions)
    # for convention in conventions:
    #     new_v, f = Convention.objects.get_or_create(
    #         season=convention.season,
    #         division=convention.division,
    #         year=convention.year + 1,
    #         international=convention.international
    #     )
    #     log.info("{0}, {1}".format(new_v, f))
    #     sessions = convention.sessions.all()
    #     for session in sessions:
    #         new_s, f = new_v.sessions.get_or_create(
    #             kind=session.kind,
    #         )
    #         log.info("{0}, {1}".format(new_s, f))
    #         rounds = session.rounds.all()
    #         for round in rounds:
    #             new_r, f = new_s.rounds.get_or_create(
    #                 kind=round.kind,
    #                 num=round.num,
    #             )
    #             log.info("{0}, {1}".format(new_r, f))
    #         assignments = session.assignments.filter(kind=Assignment.KIND.official)
    #         for assignment in assignments:
    #             new_j, f = new_s.assignments.get_or_create(
    #                 category=assignment.category,
    #                 kind=assignment.kind,
    #                 slot=assignment.slot,
    #             )
    #             log.info("{0}, {1}".format(new_j, f))
    #         contests = session.contests.all()
    #         for contest in contests:
    #             new_c, f = new_s.contests.get_or_create(
    #                 award=contest.award,
    #                 session=contest.session,
    #                 cycle=contest.cycle + 1,
    #                 is_qualifier=contest.is_qualifier
    #             )
    #             log.info("{0}, {1}".format(new_c, f))
    # return "Built {0}".format(year)
