import logging
log = logging.getLogger(__name__)

from django.shortcuts import (
    render,
    redirect,
)

from django.db import IntegrityError
from django.contrib import messages

from apps.api.models import (
    Group,
    Song,
    Person,
    Collection,
    Duplicate,
    GroupF,
    SongF,
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


def merge_group(request, parent, child):
    parent = Group.objects.get(id=parent)
    child = Group.objects.get(id=child)
    if parent.kind == 1:
        r = redirect('website:quartets')
    else:
        r = redirect('website:choruses')
    contestants = child.contestants.all()
    if not contestants:
        child.delete()
        messages.warning(
            request,
            "Merged {0} into {1}.".format(child, parent)
        )
        return r
    # move related records
    for contestant in contestants:
        contestant.group = parent
        try:
            contestant.save()
        except IntegrityError:
            raise RuntimeError(
                "Contestant {0} already exists.  Merge manually".format(contestant)
            )
    # remove redundant group
    try:
        child.delete()
    except Exception as e:
        raise RuntimeError("Error deleting old group: {0}".format(e))
    duplicates = GroupF.objects.filter(parent=parent)
    duplicates.delete()
    messages.success(
        request,
        "Merged {0} into {1}.".format(child, parent)
    )
    return r


def remove_group(request, parent):
    duplicates = GroupF.objects.filter(parent__id=parent)
    p = Group.objects.get(id=parent)
    if p.kind == 1:
        r = redirect('website:quartets')
    else:
        r = redirect('website:choruses')
    duplicates.delete()
    messages.error(
        request,
        "Removed {0} from duplicates.".format(parent.name)
    )
    return r


def merge_song(request, parent, child):
    parent = Song.objects.get(id=parent)
    child = Song.objects.get(id=child)
    charts = child.charts.all()
    if not charts:
        child.delete()
        messages.warning(
            request,
            "Merged {0} into {1}.".format(child, parent)
        )
        return redirect('website:songs')
    # move related records
    for chart in charts:
        chart.song = parent
        try:
            chart.save()
        except IntegrityError:
            raise RuntimeError(
                "Chart {0} already exists.  Merge manually".format(chart)
            )
    # remove redundant group
    try:
        child.delete()
    except Exception as e:
        raise RuntimeError("Error deleting old song: {0}".format(e))
    duplicates = SongF.objects.filter(parent=parent)
    duplicates.delete()
    messages.success(
        request,
        "Merged {0} into {1}.".format(child, parent)
    )
    return redirect('website:songs')


def remove_song(request, parent):
    duplicates = SongF.objects.filter(parent__id=parent)
    duplicates.delete()
    messages.error(
        request,
        "Removed {0} from duplicates.".format(parent.song)
    )
    return redirect('website:songs')


def choruses(request):
    groups = Group.objects.filter(
        group_duplicates__isnull=False,
    ).filter(kind=2).distinct().order_by('name')
    return render(
        request,
        'groups.html',
        {'groups': groups},
    )


def quartets(request):
    groups = Group.objects.filter(
        group_duplicates__isnull=False,
    ).filter(kind=1).distinct().order_by('name')
    return render(
        request,
        'groups.html',
        {'groups': groups},
    )


def songs(request):
    songs = Song.objects.filter(
        song_duplicates__isnull=False,
    ).distinct().order_by('name')
    return render(
        request,
        'songs.html',
        {'songs': songs},
    )


def persons(request):
    persons = Person.objects.filter(
        person_duplicates__isnull=False,
    ).distinct().order_by('name')
    return render(
        request,
        'persons.html',
        {'persons': persons},
    )
