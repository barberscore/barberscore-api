from django.core.management.base import BaseCommand

# Third-Party
import requests


class Command(BaseCommand):
    help = "Command to upload from dropbox."

    def add_arguments(self, parser):
        parser.add_argument(
            'dropbox',
            nargs='?',
        )

    def handle(self, *args, **options):
        # Parse URL input
        dropbox = options['dropbox']
        p1 = dropbox.partition('?')
        p2 = p1[0].rpartition('/')
        filename = p2[2]
        url = dropbox.replace("?dl=0", "?dl=1")
        # open in binary mode
        with open(filename, "wb") as file:
            # get request
            response = requests.get(url)
            # write to file
            file.write(response.content)
        self.stdout.write("Uploaded {0}".format(filename))
        return
