import os, csv

from optparse import make_option

from django.utils.text import slugify

from django.core.management.base import BaseCommand, CommandError

from apps.bbs.models import Score, Contestant, Contest


class Command(BaseCommand):
    help = "Command to import a list of stuff"
    option_list = BaseCommand.option_list + (
        make_option(
            "-f",
            "--file",
            dest = "filename",
            help = "specify import file",
            metavar = "FILE"
        ),
    )

    def handle(self, *args, **options):
        # make sure file option is present
        if options['filename'] == None :
            raise CommandError("Option `--file=...` must be specified.")

        # make sure file path resolves
        if not os.path.isfile(options['filename']) :
            raise CommandError("File does not exist at the specified path.")

        # print file
        print "Path: `%s`" % options['filename']

        # open the file
        with open(options['filename']) as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:

                try :
                    contestant, created = Contestant.objects.get_or_create(
                        name=unicode(row[0].strip()),
                        defaults={'slug': slugify(unicode(row[0].strip())), 'contestant_type': 2}
                    )

                except Exception, e:
                    print "Contestant `%s` could not be created." % row[0]
                    print "Exception: {0} created {1}".format(e,created)
                    break

                row.append(contestant.id)
                contest = Contest.objects.get(pk=row[9])
                try:
                    new_score = Score(
                        contest=contest,
                        contestant=contestant,
                        contest_round='Finals',
                        slug=slugify(unicode(row[0].strip())),
                        song1=row[1],
                        mus1=row[2],
                        prs1=row[3],
                        sng1=row[4],
                        song2=row[5],
                        mus2=row[6],
                        prs2=row[7],
                        sng2=row[8]
                    )
                    new_score.save()
                except Exception, e:
                    print "Score {name} could not be created".format(name=row[0])
                    print "Exception: {0}".format(e)
                    break


