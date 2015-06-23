for row in data:
    contestant = {}
    contestant['contest'] = Contest.objects.get(
        year=int(row[0]),
        kind=2,
        level=1,
    )
    try:
        contestant['group'] = Group.objects.get(
            name__iexact=row[2].strip(),
            kind=2,
        )
    except Group.DoesNotExist:
        try:
            contestant['group'] = Group.objects.get(
                name__iexact="{0} Chorus".format(row[2].strip()),
                kind=2,
            )
        except Group.DoesNotExist:
            contestant['group'] = Group.objects.create(
                name="{0} Chorus".format(row[2].strip()),
                kind=2,
            )
    contestant['director'], created = Director.objects.get_or_create(
        name=row[6].strip(),
    )
    try:
        contestant['district'] = District.objects.get(name=row[4])
    except District.DoesNotExist:
        contestant['district'] = None
    contestant['total_raw'] = int(row[3])
    contestant['place'] = int(row[1])
    new.append(contestant)