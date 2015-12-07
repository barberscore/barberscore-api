import os
import csv

import logging
log = logging.getLogger(__name__)


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


def strip_penalties(output):
    for row in output:
        scores = [6, 7, 8, 10, 11, 12]
        for score in scores:
            try:
                int(row[score])
            except ValueError:
                row[score] = row[score][:3]
    return output


def write_file(path, output):
    basepath = os.path.split(path)[0]
    namepath = os.path.split(path)[1]
    with open(os.path.join(basepath, namepath,), 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in output:
            writer.writerow(row)
    return


def parse_chorus(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[9].split('[', 1)[1].split(']', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[9] = row[9].split('[', 1)[0]
        # Add round
        row.extend(['1'])
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    # new_list = [[row[ci] for ci in (
    #     18, 16, 8, 0, 17, 1, 2, 3, 4, 9, 10, 11, 12, 6, 7
    # )] for row in output]

    # new_list = strip_penalties(new_list)

    output = write_file(path, output)

    return


def parse_chorus_nd(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        # row.extend([row[8].split('(', 1)[1].split(')', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        # row[8] = row[8].split('(', 1)[0]
        # Add round
        row.extend(['1'])
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    new_list = [[row[ci] for ci in (
        17, 16, 8, 0, 15, 1, 2, 3, 4, 9, 10, 11, 12, 6, 7
    )] for row in output]

    new_list = strip_penalties(new_list)

    output = write_file(path, new_list)

    return


def parse_district_chorus(path, district):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[9].split('(', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[9] = row[9].split('(', 1)[0]
        # Add round
        row.extend(['1'])
        # Overwrite district
        row[19] = district
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
        row.insert(2, row.pop(11))
        row.insert(4, row.pop(-1))
        row.insert(-1, row.pop(12))
        row.pop(5)
        row.pop(9)
        row.pop(9)
        row.pop(9)
        row.pop(13)
        row.pop(13)
        row.pop(14)

    output = strip_penalties(output)

    output = write_file(path, output)

    return


def parse_quarters(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[7].split('[', 1)[1].split(']', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[7] = row[7].split('[', 1)[0]
        # Add round
        row.extend(['3'])
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    new_list = [[row[ci] for ci in (
        16, 14, 0, 15, 12, 1, 2, 3, 4, 8, 9, 10, 11, 6,
    )] for row in output]

    new_list = strip_penalties(new_list)

    output = write_file(path, new_list)

    return


def parse_semis(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[9].split('[', 1)[1].split(']', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[9] = row[9].split('[', 1)[0]
        # Add round
        row.extend(['2'])
        output.append(row)
    # Strip space
    for row in output:
        i = 0
        l = len(row)
        while i < l:
            row[i] = row[i].strip()
            i += 1
    new_list = [[row[ci] for ci in (
        20, 18, 0, 19, 14, 1, 2, 3, 4, 10, 11, 12, 13, 8,
    )] for row in output]

    new_list = strip_penalties(new_list)

    output = write_file(path, new_list)

    return


def parse_finals(path):
    data = deinterlace(path)
    output = []
    # Split first cell and chapter cell
    for row in data:
        row.extend([row[0].split(' ', 1)[0]])
        row.extend([row[9].split('[', 1)[1].split(']', 1)[0]])
        row[0] = row[0].split(' ', 1)[1]
        row[9] = row[9].split('[', 1)[0]
        # Add round
        row.extend(['1'])
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
        row.insert(3, row.pop(-2))
        row.insert(4, row.pop(-1))
        row.pop(9)
        row.pop(9)
        row.pop(9)
        row.pop(9)
        row.pop(9)
        row.pop(-1)
        row.pop(-1)

    output = strip_penalties(output)

    output = write_file(path, output)

    return


def place_round(performers):
    draw = []
    i = 1
    for performer in performers:
        try:
            match = performer.points == draw[0].points
        except IndexError:
            performer.place = i
            performer.save()
            draw.append(performer)
            continue
        if match:
            performer.place = i
            i += len(draw)
            performer.save()
            draw.append(performer)
            continue
        else:
            i += 1
            performer.place = i
            performer.save()
            draw = [performer]
    return


def merge_groups(from_group, to_group):
    cs = from_group.performers.all()
    for c in cs:
        c.group = to_group
        c.save()
    from_group.delete()


def score_performer(performer):
    session = performer.contest.session
    if performer.contest.kind == 1:
        if performer.quarters_points and not performer.semis_points:
            performer.score = round(performer.points / (session * 6 * 1), 1)
        elif performer.semis_points and not performer.finals_points:
            performer.score = round(performer.points / (session * 6 * 2), 1)
        elif performer.finals_points:
            performer.score = round(performer.points / (session * 6 * 3), 1)
        else:
            performer.score = None
    else:
        performer.score = round(performer.points / (session * 6 * 1), 1)
    performer.save()
    return


def parse_arrangers(data):
    names = [
        ['quarters_song1', 'quarters_song1_arranger'],
        ['quarters_song2', 'quarters_song2_arranger'],
        ['semis_song1', 'semis_song1_arranger'],
        ['semis_song2', 'semis_song2_arranger'],
        ['finals_song1', 'finals_song1_arranger'],
        ['finals_song2', 'finals_song2_arranger'],
    ]

    for row in data:
        try:
            c = Performer.objects.get(
                contest__name='International Quartet 2015',
                group__name__iexact=row[0],
            )
        except c.DoesNotExist:
            print row
        for n in names:
            song = getattr(c, n[0])
            try:
                match = (song.name == row[1])
            except AttributeError:
                continue
            if match:
                try:
                    arranger = Person.objects.get(name__iexact=row[2])
                except Person.DoesNotExist:
                    continue
                setattr(c, n[1], arranger)
                c.save()
