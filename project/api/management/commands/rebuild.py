# Django
from django.core.files import File
from django.core.management.base import BaseCommand

# First-Party
from api.models import Convention
from api.utils import (
    extract_contestants,
    extract_contests,
    extract_panel,
    extract_appearances,
    extract_entries,
    extract_rounds,
    extract_scores,
    extract_sessions,
    extract_songs,
    import_convention,
    rank,
)


class Command(BaseCommand):
    help = "Command to rebuild from stix files."

    def handle(self, *args, **options):

        vs = Convention.objects.filter(year=2015)
        vs.delete()

        self.stdout.write("Database Flushed")

        i = 11
        while i <= 27:
            path = "stix/fall000{0}.txt".format(i)
            convention = import_convention(path, season='fall')
            convention.save()
            filename = convention.id.hex + '.txt'
            convention.stix_file.save(
                filename,
                File(open(path, 'r')),
                save=True,
            )
            i += 1
            self.stdout.write("{0}".format(convention))

        i = 11
        while i <= 21:
            path = "stix/spring000{0}.txt".format(i)
            convention = import_convention(path, season='spring')
            convention.save()
            filename = convention.id.hex + '.txt'
            convention.stix_file.save(
                filename,
                File(open(path, 'r')),
                save=True,
            )
            i += 1
            self.stdout.write("{0}".format(convention))

        i = 11
        while i <= 25:
            path = "stix/combo000{0}.txt".format(i)
            convention = import_convention(path, season='spring', division=True)
            convention.save()
            filename = convention.id.hex + '.txt'
            convention.stix_file.save(
                filename,
                File(open(path, 'r')),
                save=True,
            )
            i += 1
            self.stdout.write("{0}".format(convention))

        international = [
            'international.txt',
        ]

        for f in international:
            path = "stix/{0}".format(f)
            convention = import_convention(path, season='summer')
            convention.save()
            filename = convention.id.hex + '.txt'
            convention.stix_file.save(
                filename,
                File(open(path, 'r')),
                save=True,
            )
            self.stdout.write("{0}".format(convention))

        midwinter = [
            'midwinter.txt',
        ]

        for f in midwinter:
            path = "stix/{0}".format(f)
            convention = import_convention(path, season='midwinter')
            convention.save()
            filename = convention.id.hex + '.txt'
            convention.stix_file.save(
                filename,
                File(open(path, 'r')),
                save=True,
            )
            self.stdout.write("{0}".format(convention))

        self.stdout.write("Conventions Loaded")

        vs = Convention.objects.filter(year=2015)

        for v in vs:
            extract_sessions(v)
        self.stdout.write("Sessions Extracted")

        for v in vs:
            extract_rounds(v)
        self.stdout.write("Rounds Extracted")

        for v in vs:
            extract_panel(v)
        self.stdout.write("Panel Extracted")

        for v in vs:
            extract_entries(v)
        self.stdout.write("Entries Extracted")

        for v in vs:
            extract_contests(v)
        self.stdout.write("Contests Extracted")

        for v in vs:
            extract_contestants(v)
        self.stdout.write("Contestants Extracted")

        for v in vs:
            extract_appearances(v)
        self.stdout.write("Appearances Extracted")

        for v in vs:
            extract_songs(v)
        self.stdout.write("Songs Extracted")

        for v in vs:
            extract_scores(v)
        self.stdout.write("Scores Extracted")

        # for v in vs:
        #     fill_parents(v)
        # self.stdout.write("Parents Added")

        # for v in vs:
        #     denormalize(v)
        # self.stdout.write("Convention Denormalized")

        for v in vs:
            rank(v)
        self.stdout.write("Convention Ranked")

        return "Rebuild Complete"
