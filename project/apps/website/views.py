import logging
log = logging.getLogger(__name__)

from django.shortcuts import (
    render,
    redirect,
)

from apps.api.models import (
    Group,
    Song,
    Person,
    Collection,
    Duplicate,
)


def home(request):
    return render(
        request,
        'home.html',
    )


def collections(request):
    collections = Collection.objects.exclude(is_flag=True).order_by('id')
    return render(
        request,
        'collections.html',
        {'collections': collections},
    )


def collection(request, id):
    collection = Collection.objects.get(id=id)
    dups = []
    if collection.primitive.name == 'Group':
        for d in collection.duplicates.all():
            g = Group.objects.get(id=d.source_id)
            dups.append(g)
    elif collection.primitive.name == 'Song':
        for d in collection.duplicates.all():
            s = Song.objects.get(id=d.source_id)
            dups.append(s)
    elif collection.primitive.name == 'Person':
        for d in collection.duplicates.all():
            p = Person.objects.get(id=d.source_id)
            dups.append(p)
    return render(
        request,
        'collection.html',
        {'collection': collection, 'dups': dups},
    )


def merge(request, id):
    keep = Duplicate.objects.get(source_id=id)
    collection = keep.collection
    if collection.primitive.name == 'Group':
        parent = Group.objects.get(id=keep.source_id)
    elif collection.primitive.name == 'Song':
        parent = Song.objects.get(id=keep.source_id)
    elif collection.primitive.name == 'Person':
        parent = Person.objects.get(id=keep.source_id)
    else:
        raise RuntimeError("No primitive selected.")
    orphans = collection.duplicates.exclude(source_id=id)
    for orphan in orphans:
        if collection.primitive.name == 'Group':
            drop = Group.objects.get(id=orphan.source_id)
            for contestant in drop.contestants.all():
                contestant.group = parent
                contestant.save()
            drop.delete()
        elif collection.primitive.name == 'Song':
            drop = Song.objects.get(id=orphan.source_id)
            for chart in drop.charts.all():
                chart.songs.add(parent)
                chart.songs.remove(drop)
            drop.delete()
        elif collection.primitive.name == 'Person':
            drop = Person.objects.get(id=orphan.source_id)
            for director in drop.choruses.all():
                director.person = parent
                director.save()
            for singer in drop.quartets.all():
                singer.person = parent
                singer.save()
            for arrangement in drop.arrangements.all():
                arrangement.person = parent
                arrangement.save()
            drop.delete()
        else:
            raise RuntimeError("How did i get here?")
    try:
        r = redirect('website:collection', collection.get_next().id)
    except AttributeError:
        r = redirect('website:collections')
    collection.delete()
    return r


def skip(request, id):
    collection = Collection.objects.get(id=id)
    try:
        r = redirect('website:collection', collection.get_next().id)
    except AttributeError:
        r = redirect('website:collections')
    collection.delete()
    return r


def flag(request, id):
    collection = Collection.objects.get(id=id)
    try:
        r = redirect('website:collection', collection.get_next().id)
    except AttributeError:
        r = redirect('website:collections')
    collection.is_flag = True
    collection.save()
    return r


def choruses(request):
    groups = Group.objects.filter(
        group_duplicates__isnull=False,
    ).filter(kind=2).order_by('name')
    return render(
        request,
        'groups.html',
        {'groups': groups},
    )


def quartets(request):
    groups = Group.objects.filter(
        group_duplicates__isnull=False,
    ).filter(kind=1).order_by('name')
    return render(
        request,
        'groups.html',
        {'groups': groups},
    )


def songs(request):
    songs = Song.objects.filter(
        song_duplicates__isnull=False,
    ).order_by('name')
    return render(
        request,
        'songs.html',
        {'songs': songs},
    )


def persons(request):
    persons = Person.objects.filter(
        person_duplicates__isnull=False,
    ).order_by('name')
    return render(
        request,
        'persons.html',
        {'persons': persons},
    )
