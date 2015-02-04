import csv

import logging
log = logging.getLogger(__name__)

from .models import (
    District,
    Chorus,
    Quartet,
    Contest,
    Performance,
    Group,
)


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


def parse_chorus(path, round):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[8].split('[', 1)[1].split(']', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[8] = row[8].split('[', 1)[0]
        # Add round
        row.extend([round])
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
        row.insert(2, row.pop(10))
        row.insert(4, row.pop(-1))
        row.pop(10)
        row.pop(9)
        row.insert(-1, row.pop(9))
        row.pop(13)
        row.pop(13)
        row.pop(-1)

    #  Write output
    with open('output.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in output:
            writer.writerow(row)
    return output


def create_from_scores(self):
    data = [row for row in csv.reader(self.csv_finals.read())]
    if self.kind == self.CHORUS:
        for row in data:
            log.debug(row)
            chorus, created = Chorus.objects.get_or_create(
                name__in=[row[2], 'The {0}'.format(row[2])]
            )
            log.debug(chorus)
            if created:
                # TODO refactor
                district_name = row[3]
                try:
                    district = District.objects.get(
                        name=district_name,
                    )
                except District.DoesNotExist as e:
                    # TODO Kludge
                    if district_name == 'AAMBS':
                        district = District.objects.get(name='BHA')
                    else:
                        raise e

                chorus.district = district
                chorus.chapter_name = row[1]
                chorus.save()
                log.info("Created chorus: {0}".format(chorus))
    else:
        # Create contestant objects first (if needed)
        for row in data:

            quartet, created = Quartet.objects.get_or_create(
                name=row[0].split(' ', 1)[1].strip(),
            )
            if created:
                # TODO refactor
                district_name = row[7].split('[', 1)[1].split(']', 1)[0]
                try:
                    district = District.objects.get(
                        name=district_name,
                    )
                except District.DoesNotExist as e:
                    # TODO Kludge
                    if district_name == 'AAMBS':
                        district = District.objects.get(name='BHA')
                    else:
                        raise e
                quartet.district = district
                quartet.save()
                log.info("Created quartet: {0}".format(quartet))
    return "Finished pre-processing"


def import_scores(self):
    reader = csv.reader(self.csv_finals)
    data = [row for row in reader]

    performance = {}

    for row in data:
        performance['contest'] = self
        performance['place'] = row[0]
        performance['name'] = Group.objects.get(name=row[0])
        performance['song1'] = row[1]
        performance['mus1'] = row[2]
        performance['prs1'] = row[3]
        performance['sng1'] = row[4]
        performance['song2'] = row[5]
        performance['mus2'] = row[6]
        performance['prs2'] = row[7]
        performance['sng2'] = row[8]
        performance['men'] = row[9]
        result = Performance.objects.create(**performance)
        log.info("Created performance: {0}".format(performance))
    return "Done"

def process_csv(self):
    if self.csv_quarters:
        self.import_quarters()
    if self.csv_semis:
        self.import_semis()
    if self.csv_finals:
        self.import_finals()
    return "Done"
