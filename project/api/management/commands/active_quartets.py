# Django
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage

# First-Party
import csv
import datetime
from bhs.models import Structure

class Command(BaseCommand):
    help = "Command to sync database with BHS ."

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            dest='all',
            default=False,
            help='Update all persons.',
        )

    def handle(self, *args, **options):
        self.stdout.write("Sending active quartets...")
        filename = 'active_quartets_{0}.csv'.format(datetime.date.today())
        with open(filename, 'w') as f:
            output = []
            fieldnames = [
                'id',
                'name',
                'bhs_id',
                'district',
            ]
            quartets = Structure.objects.filter(
                kind='quartet',
                status__name='active'
            )
            for quartet in quartets:
                pk = str(quartet.id)
                try:
                    name = quartet.name.strip()
                except AttributeError:
                    name = '(UNKNOWN)'
                bhs_id = quartet.bhs_id
                district = str(quartet.parent)
                row = {
                    'id': pk,
                    'name': name,
                    'bhs_id': bhs_id,
                    'district': district,
                }
                output.append(row)
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            for row in output:
                writer.writerow(row)
        message = EmailMessage(
            subject='Active Quartets',
            body='Active quartets CSV attached',
            from_email='admin@barberscore.com',
            to=['chris.buechler@verizon.net',]
        )
        message.attach_file(filename)
        result = message.send()
        if result == 1:
            self.stdout.write("Sent.")
        else:
            self.stdout.write("Error.  Not sent.")
