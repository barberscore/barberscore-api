# Django
# Third-Party
# Third-Party
from openpyxl import Workbook

from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand

# First-Party
from api.models import Chart


class Command(BaseCommand):
    help = "Command to sync database with BHS ."

    def handle(self, *args, **options):
        self.stdout.write("Sending song title report...")
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'title',
        ]
        ws.append(fieldnames)
        charts = Chart.objects.all().distinct(
            'title'
        ).order_by(
            'title'
        )
        for chart in charts:
            title = chart.title.strip()
            row = [
                title,
            ]
            ws.append(row)
        wb.save('song_title_report.xlsx')

        message = EmailMessage(
            subject='Song Title Report',
            body='Song Title Report Attached',
            from_email='admin@barberscore.com',
            to=['chris.buechler@verizon.net', ]
        )
        message.attach_file('song_title_report.xlsx')
        result = message.send()
        if result == 1:
            self.stdout.write("Sent.")
        else:
            self.stdout.write("Error.  Not sent.")
