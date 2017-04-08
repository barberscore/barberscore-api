# Standard Libary
import csv
import logging

# Third-Party
from auth0.v2.management import Auth0
from psycopg2.extras import DateRange
import requests

# Django
from django.conf import settings
from django.db import IntegrityError
from django.db.models import Q
from django.utils import (
    dateparse,
    encoding,
)

# Local
from .models import (
    Assignment,
    Award,
    Chart,
    Contestant,
    Convention,
    Entity,
    Office,
    Person,
    Session,
    Submission,
    User,
)

log = logging.getLogger(__name__)


def get_auth0_token():
    url = 'https://barberscore.auth0.com/oauth/token'
    payload = {
        'grant_type': 'client_credentials',
        'client_id': settings.AUTH0_API_ID,
        'client_secret': settings.AUTH0_API_SECRET,
        'audience': settings.AUTH0_AUDIENCE,
    }
    response = requests.post(url, payload)
    json = response.json()
    return json['access_token']


def update_db_chart(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            bhs_id = int(row[0]) if row[0] else None
            if bhs_id and row[2]:
                try:
                    bhs_fee = int(row[4])
                except ValueError:
                    bhs_fee = None
                chart, created = Chart.objects.get_or_create(
                    bhs_id=bhs_id
                )
                chart.title = row[2]
                chart.arrangers = row[3]
                chart.bhs_fee = bhs_fee
                chart.bhs_difficulty = int(row[5]) if row[5] else None
                chart.bhs_tempo = int(row[6]) if row[6] else None
                chart.is_medley = True if row[7] == 'True' else False
                chart.save()


# def create_account(person):
#     if not person.email:
#         raise RuntimeError("No email")
#     user = User.objects.create_user(
#         person.email,
#     )
#     password = User.objects.make_random_password()
#     payload = {
#         "connection": "Default",
#         "email": person.email,
#         "password": password,
#         "user_metadata": {
#             "name": person.name
#         },
#         "app_metadata": {
#             "bhs_id": person.bhs_id,
#             "person_id": str(person.id),
#         }
#     }
#     auth0 = Auth0(
#         settings.AUTH0_DOMAIN,
#         settings.AUTH0_TOKEN,
#     )
#     response = auth0.users.create(payload)
#     sub_id = response['user_id']
#     payload2 = {
#         "result_url": "http://localhost:4200",
#         "user_id": sub_id,
#     }
#     response2 = auth0.tickets.create_pswd_change(payload2)
#     return response2['ticket']


def export_db_chapters():
    with open('chapters.csv', 'wb') as f:
        chapters = Entity.objects.filter(
            kind=Entity.KIND.chorus,
        ).exclude(
            parent=None,
        ).values()
        fieldnames = [
            'id',
            'nomen',
            'name',
            'status',
            'kind',
            'age',
            'is_novice',
            'short_name',
            'long_name',
            'code',
            'start_date',
            'end_date',
            'location',
            'website',
            'facebook',
            'twitter',
            'email',
            'phone',
            'picture',
            'description',
            'notes',
            'bhs_id',
            'parent_id',
            'parent',
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for chapter in chapters:
            parent = Entity.objects.get(
                id=str(chapter['parent_id']),
            )
            chapter['parent'] = parent.name
            try:
                writer.writerow(chapter)
            except UnicodeEncodeError:
                clean = {}
                for k, v in chapter.items():
                    try:
                        clean[k] = v.encode('ascii', 'replace')
                    except AttributeError:
                        clean[k] = v
                writer.writerow(clean)


def export_db_offices():
    with open('offices.csv', 'wb') as f:
        offices = Office.objects.all(
        ).values()
        fieldnames = [
            'id',
            'nomen',
            'name',
            'status',
            'kind',
            'short_name',
            'long_name',
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for office in offices:
            try:
                writer.writerow(office)
            except UnicodeEncodeError:
                clean = {}
                for k, v in office.items():
                    try:
                        clean[k] = v.encode('ascii', 'replace')
                    except AttributeError:
                        clean[k] = v
                writer.writerow(clean)


def export_db_awards():
    with open('awards.csv', 'wb') as f:
        awards = Award.objects.all(
        ).values()
        fieldnames = [
            'id',
            'nomen',
            'name',
            'status',
            'kind',
            'season',
            'size',
            'scope',
            'is_primary',
            'is_improved',
            'is_novice',
            'is_manual',
            'is_multi',
            'is_district_representative',
            'rounds',
            'threshold',
            'minimum',
            'advance',
            'entity',
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for office in offices:
            try:
                writer.writerow(office)
            except UnicodeEncodeError:
                clean = {}
                for k, v in office.items():
                    try:
                        clean[k] = v.encode('ascii', 'replace')
                    except AttributeError:
                        clean[k] = v
                writer.writerow(clean)


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
            office['short_name'] = row[5]
            office['long_name'] = row[6]
            Office.objects.create(**office)


def import_db_organizations(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            organization = {}
            organization['name'] = row[4]
            organization['status'] = int(row[5])
            organization['kind'] = int(row[7])
            organization['short_name'] = row[10]
            organization['long_name'] = row[11]
            organization['start_date'] = dateparse.parse_date(row[13])
            organization['location'] = row[15]
            organization['website'] = row[16]
            organization['facebook'] = row[17]
            organization['twitter'] = row[18]
            organization['email'] = row[19]
            organization['phone'] = row[20]
            organization['picture'] = row[21]
            organization['description'] = row[22]
            organization['bhs_id'] = int(row[24])
            organization['parent'] = None
            Entity.objects.create(**organization)


def import_db_districts(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        parent = Entity.objects.get(short_name='BHS')
        for row in rows:
            district = {}
            district['name'] = row[4]
            district['status'] = int(row[5])
            district['kind'] = int(row[7])
            district['short_name'] = row[10]
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
            division['short_name'] = row[10]
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
                short_name=row[4].split()[0]
            )
            division['parent'] = parent
            Entity.objects.create(**division)


def import_db_chapters(path):
    with open(path) as f:
        reader = csv.reader(f, skipinitialspace=True)
        next(reader)
        rows = [row for row in reader]
        for row in rows:
            chapter = {}
            chapter['name'] = row[2]
            chapter['status'] = int(row[3])
            chapter['kind'] = int(row[4])
            chapter['short_name'] = row[7]
            chapter['long_name'] = row[8]
            chapter['code'] = row[9]
            chapter['start_date'] = dateparse.parse_date(row[10])
            chapter['end_date'] = dateparse.parse_date(row[11])
            chapter['location'] = row[12]
            chapter['website'] = row[13]
            chapter['facebook'] = row[14]
            chapter['twitter'] = row[15]
            chapter['email'] = row[16]
            chapter['phone'] = row[17]
            chapter['picture'] = row[18]
            chapter['description'] = row[19]
            chapter['notes'] = row[20]
            try:
                chapter['bhs_id'] = int(row[21])
            except ValueError:
                chapter['bhs_id'] = None
            try:
                parent = Entity.objects.get(
                    kind__lt=30,
                    name=row[23]
                )
            except Entity.DoesNotExist:
                parent = None
            chapter['parent'] = parent
            Entity.objects.create(**chapter)


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


# def import_db_persons(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         next(reader)
#         rows = [row for row in reader]
#         for row in rows:
#             bhs_id = int(row[0])
#             first_name = row[4].strip()
#             nick_name = row[5].strip()
#             if nick_name:
#                 if nick_name != first_name:
#                     nick_name = "({0})".format(nick_name)
#             else:
#                 nick_name = None
#             middle_name = row[6].strip()
#             last_name = row[7].strip()
#             suffix_name = row[8].strip()
#             prefix_name = row[2].strip()
#             name = " ".join(
#                 map(
#                     (lambda x: encoding.smart_text(x)),
#                     filter(
#                         None, [
#                             prefix_name,
#                             first_name,
#                             middle_name,
#                             last_name,
#                             suffix_name,
#                             nick_name,
#                         ]
#                     )
#                 )
#             )
#             email = row[9].strip()
#             kind = int(row[62])
#             bhs_status = int(row[34])
#             spouse = row[38].strip()
#             try:
#                 mon = int(row[78])
#             except ValueError:
#                 mon = None
#             address1 = row[13].strip()
#             address2 = row[14].strip()
#             city = row[16].strip()
#             state = row[17].strip()
#             postal_code = row[18].strip()
#             country = row[19].strip()
#             if country == 'United States':
#                 phone = "+1{0}{1}".format(
#                     str(row[22]),
#                     str(row[23]),
#                 )
#             else:
#                 phone = None
#             start_date = dateparse.parse_date(row[58])
#             birth_date = dateparse.parse_date(row[31])
#             dues_thru = dateparse.parse_date(row[36])
#             defaults = {
#                 'name': name,
#                 'email': email,
#                 'kind': kind,
#                 'status': bhs_status,
#                 'spouse': spouse,
#                 'mon': mon,
#                 'address1': address1,
#                 'address2': address2,
#                 'city': city,
#                 'state': state,
#                 'postal_code': postal_code,
#                 'country': country,
#                 'phone': phone,
#                 'start_date': start_date,
#                 'birth_date': birth_date,
#                 'dues_thru': dues_thru,
#             }
#             person, created = Person.objects.update_or_create(
#                 bhs_id=bhs_id,
#                 defaults=defaults,
#             )
#             print person, created


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


# def import_db_directors(path):
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


# def import_db_submissions(path):
#     with open(path) as f:
#         reader = csv.reader(f, skipinitialspace=True)
#         rows = [row for row in reader]
#         for row in rows:
#             bhs_id = int(row[0])
#             title = row[1].strip()
#             if row[2]:
#                 bhs_marketplace = int(row[2])
#             else:
#                 bhs_marketplace = None
#             if bhs_marketplace:
#                 try:
#                     chart = Chart.objects.get(
#                         bhs_marketplace=bhs_marketplace,
#                     )
#                     log.info('Found chart by marketplace')
#                 except Chart.DoesNotExist:
#                     log.info('No marketplace: {0} {1}'.format(bhs_id, title))
#                     chart = None
#             else:
#                 chart = None
#             if not chart:
#                 try:
#                     chart = Chart.objects.get(
#                         title=title,
#                         bhs_marketplace=None,
#                     )
#                     log.info('Found chart by title')
#                 except Chart.DoesNotExist:
#                     if bhs_marketplace:
#                         chart = Chart.objects.create(
#                             title=title,
#                             bhs_marketplace=bhs_marketplace,
#                         )
#                         log.info("Create chart with id: {0} {1}".format(title, bhs_marketplace))
#                     else:
#                         chart = Chart.objects.create(
#                             title=title,
#                         )
#                         log.info("Create chart with no id: {0}".format(title))
#                 except Chart.MultipleObjectsReturned:
#                     chart = Chart.objects.filter(
#                         title=title,
#                         bhs_marketplace=None,
#                     ).first()
#                     log.info("Pick first chart: {0}".format(title))
#             entries = Entry.objects.filter(
#                 group__bhs_id=bhs_id,
#                 session__convention__year=2016,
#             )
#             for entry in entries:
#                 submission, created = Submission.objects.get_or_create(
#                     entry=entry,
#                     chart=chart,
#                 )
#                 print submission, created


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
#                 district_name = convention.organization.short_name
#                 try:
#                     organization = Organization.objects.get(
#                         name="{0} {1}".format(
#                             district_name,
#                             name,
#                         )
#                     )
#                 except Organization.DoesNotExist:
#                     log.error("Bad Div: {0} {1}".format(district_name, name))
#                     continue
#                 try:
#                     entry = Entry.objects.get(
#                         bhs_id=int(row[0]),
#                     )
#                 except Entry.DoesNotExist:
#                     log.error("Can't find entry")
#                     continue
#                 entry.representing = organization
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
#             organization = entry.representing
#             if organization.level == Organization.LEVEL.district:
#                 district = organization
#                 division = None
#             elif organization.level == Organization.LEVEL.division:
#                 district = organization.parent
#                 division = organization
#             else:
#                 log.error("Bad Rep: {0} {1}".format(
#                     entry,
#                     organization,
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
#                     organization=entry.representing,
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
#                         organization=district,
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
#                         organization=district,
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
#                         organization=district,
#                     )
#                 elif 'Out Of Division Seniors Quartet' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.seniors,
#                         organization=district,
#                     )
#                 elif 'Out Of Division Quartet (Overall)' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.quartet,
#                         organization=district,
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
#                         organization=district,
#                     )
#                 elif 'Most-Improved Chorus' in name:
#                     award = Award.objects.get(
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.chorus,
#                         organization=district,
#                         is_improved=True,
#                     )
#                 elif 'Out Of Division Chorus' in name:
#                     award = Award.objects.get(
#                         is_primary=True,
#                         level=Award.LEVEL.district,
#                         kind=Award.KIND.chorus,
#                         organization=district,
#                     )
#                 elif 'Plateau A (or 1) Chorus' == name:
#                     if row[4] == 'Division Only':
#                         organization = division
#                         level = Award.LEVEL.division
#                     else:
#                         organization = district
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
#                             organization=organization,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau 1 ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             organization=organization,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau I ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             organization=organization,
#                             is_improved=is_improved,
#                         ),
#                     )
#                 elif 'Plateau AA (or 2) Chorus' == name:
#                     if row[4] == 'Division Only':
#                         organization = division
#                         level = Award.LEVEL.division
#                     else:
#                         organization = district
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
#                             organization=organization,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau 2 ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             organization=organization,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau II ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             organization=organization,
#                             is_improved=is_improved,
#                         ),
#                     )
#                 elif 'Plateau AAA (or 3) Chorus' == name:
#                     if row[4] == 'Division Only':
#                         organization = division
#                         level = Award.LEVEL.division
#                     else:
#                         organization = district
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
#                             organization=organization,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau 3 ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             organization=organization,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau III ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             organization=organization,
#                             is_improved=is_improved,
#                         ),
#                     )
#                 elif 'Plateau AAAA (or 4) Chorus' == name:
#                     if row[4] == 'Division Only':
#                         organization = division
#                         level = Award.LEVEL.division
#                     else:
#                         organization = district
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
#                             organization=organization,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau 4 ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             organization=organization,
#                             is_improved=is_improved,
#                         ) | Q(
#                             stix_name__contains='Plateau IV ',
#                             level=level,
#                             kind=Award.KIND.chorus,
#                             organization=organization,
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
#                         organization=division,
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
#         chapter.organization = Organization.objects.get(code=letter)


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
    #         organization=convention.organization
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
