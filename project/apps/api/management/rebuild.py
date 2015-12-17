from apps.api.models import *
from apps.api.utils import *
from django.core.files import File

vs = Convention.objects.filter(year=2015)
vs.delete()

ws = Award.objects.all()
ws.delete()

print "Database Flushed"

i = 11
while i <= 27:
    path = "stix/fall000{0}.txt".format(i)
    convention = import_convention(path, kind='fall')
    convention.save()
    filename = convention.id.hex + '.txt'
    convention.stix_file.save(
        filename,
        File(open(path, 'r')),
        save=True,
    )
    i += 1
    print convention


i = 11
while i <= 21:
    path = "stix/spring000{0}.txt".format(i)
    convention = import_convention(path, kind='spring')
    convention.save()
    filename = convention.id.hex + '.txt'
    convention.stix_file.save(
        filename,
        File(open(path, 'r')),
        save=True,
    )
    i += 1
    print convention


i = 11
while i <= 25:
    path = "stix/combo000{0}.txt".format(i)
    convention = import_convention(path, kind='spring', division=True)
    convention.save()
    filename = convention.id.hex + '.txt'
    convention.stix_file.save(
        filename,
        File(open(path, 'r')),
        save=True,
    )
    i += 1
    print convention

international = [
    'international.txt',
]

for f in international:
    path = "stix/{0}".format(f)
    convention = import_convention(path, kind='international')
    convention.save()
    filename = convention.id.hex + '.txt'
    convention.stix_file.save(
        filename,
        File(open(path, 'r')),
        save=True,
    )
    print convention

midwinter = [
    'midwinter.txt',
]

for f in midwinter:
    path = "stix/{0}".format(f)
    convention = import_convention(path, kind='midwinter')
    convention.save()
    filename = convention.id.hex + '.txt'
    convention.stix_file.save(
        filename,
        File(open(path, 'r')),
        save=True,
    )
    print convention


print "Conventions Loaded"
vs = Convention.objects.filter(year=2015)

for v in vs:
    extract_sessions(v)
print "Sessions Extracted"

for v in vs:
    extract_rounds(v)
print "Rounds Extracted"

for v in vs:
    extract_awards(v)
print "Awards Extracted"

for v in vs:
    extract_panel(v)
print "Panel Extracted"