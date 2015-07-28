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
    GroupF,
    SongF,
    PersonF,
)


def home(request):
    return render(
        request,
        'home.html',
    )


def merge_groups(request, parent, child):
    parent = Group.objects.get(id=parent)
    child = Group.objects.get(id=child)
    if parent.kind == 1:
        r = redirect('website:quartets')
    else:
        r = redirect('website:choruses')
    contestants = child.contestants.all()
    if not contestants.exists():
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
            messages.error(
                request,
                "Target {0} already exists.  Merge manually".format(contestant),
            )
            duplicates = GroupF.objects.filter(parent_id=parent)
            children = [d.child for d in duplicates]
            for c in children:
                records = GroupF.objects.filter(parent=c)
                records.delete()
            duplicates.delete()
    # remove redundant group
    try:
        child.delete()
    except Exception as e:
        raise RuntimeError("Error deleting old group: {0}".format(e))
    duplicates = GroupF.objects.filter(parent=parent)
    children = [d.child for d in duplicates]
    for c in children:
        records = GroupF.objects.filter(parent=c)
        records.delete()
    duplicates.delete()
    messages.success(
        request,
        "Merged {0} into {1}.".format(child, parent)
    )
    return r


def remove_group(request, parent):
    duplicates = GroupF.objects.filter(parent__id=parent)
    group = Group.objects.get(id=parent)
    if group.kind == 1:
        r = redirect('website:quartets')
    else:
        r = redirect('website:choruses')
    children = [d.child for d in duplicates]
    for c in children:
        records = GroupF.objects.filter(parent=c)
        records.delete()
    duplicates.delete()
    messages.error(
        request,
        "Removed {0} from duplicates.".format(group.name)
    )
    return r


def merge_songs(request, parent, child):
    parent = Song.objects.get(id=parent)
    child = Song.objects.get(id=child)
    spots = child.spots.all()
    if not spots.exists():
        child.delete()
        messages.warning(
            request,
            "Merged {0} into {1}.".format(child, parent)
        )
        return redirect('website:songs')
    # move related records
    for spot in spots:
        spot.song = parent
        try:
            spot.save()
        except IntegrityError:
            messages.error(
                request,
                "Target {0} already exists.  Merge manually".format(spot),
            )
            duplicates = SongF.objects.filter(parent_id=parent)
            children = [d.child for d in duplicates]
            for c in children:
                records = SongF.objects.filter(parent=c)
                records.delete()
            duplicates.delete()
    # remove redundant group
    try:
        child.delete()
    except Exception as e:
        raise RuntimeError("Error deleting old song: {0}".format(e))
    duplicates = SongF.objects.filter(parent=parent)
    children = [d.child for d in duplicates]
    for c in children:
        records = SongF.objects.filter(parent=c)
        records.delete()
    duplicates.delete()
    messages.success(
        request,
        "Merged {0} into {1}.".format(child, parent)
    )
    return redirect('website:songs')


def remove_song(request, parent):
    duplicates = SongF.objects.filter(parent__id=parent)
    song = Song.objects.get(id=parent)
    children = [d.child for d in duplicates]
    for c in children:
        records = SongF.objects.filter(parent=c)
        records.delete()
    duplicates.delete()
    messages.error(
        request,
        "Removed {0} from duplicates.".format(song.name)
    )
    return redirect('website:songs')


def merge_persons(request, parent, child):
    parent = Person.objects.get(id=parent)
    child = Person.objects.get(id=child)
    quartets = child.quartets.all()
    choruses = child.choruses.all()
    arrangements = child.arrangements.all()
    if (quartets.exists() and choruses.exists() and arrangements.exists()):
        child.delete()
        messages.warning(
            request,
            "Merged {0} into {1}.".format(child, parent)
        )
        return redirect('website:persons')
    # move related records
    for quartet in quartets:
        quartet.person = parent
        try:
            quartet.save()
        except IntegrityError:
            messages.error(
                request,
                "Quartet {0} already exists.  Merge manually".format(quartet),
            )
            duplicates = PersonF.objects.filter(parent__id=parent)
            children = [d.child for d in duplicates]
            for c in children:
                records = PersonF.objects.filter(parent=c)
                records.delete()
            duplicates.delete()
    for chorus in choruses:
        chorus.person = parent
        try:
            chorus.save()
        except IntegrityError:
            messages.error(
                request,
                "Target {0} already exists.  Merge manually".format(chorus),
            )
            duplicates = PersonF.objects.filter(parent_id=parent)
            children = [d.child for d in duplicates]
            for c in children:
                records = PersonF.objects.filter(parent=c)
                records.delete()
            duplicates.delete()
            return redirect('website:persons')
    for arrangement in arrangements:
        arrangement.person = parent
        try:
            arrangement.save()
        except IntegrityError:
            messages.error(
                request,
                "Target {0} already exists.  Merge manually".format(arrangement),
            )
            duplicates = PersonF.objects.filter(parent_id=parent)
            children = [d.child for d in duplicates]
            for c in children:
                records = PersonF.objects.filter(parent=c)
                records.delete()
            duplicates.delete()
            return redirect('website:persons')
    # remove redundant group
    try:
        child.delete()
    except Exception as e:
        raise RuntimeError("Error deleting old person: {0}".format(e))
    duplicates = PersonF.objects.filter(parent=parent)
    children = [d.child for d in duplicates]
    for c in children:
        records = PersonF.objects.filter(parent=c)
        records.delete()
    duplicates.delete()
    messages.success(
        request,
        "Merged {0} into {1}.".format(child, parent)
    )
    return redirect('website:persons')


def remove_person(request, parent):
    duplicates = PersonF.objects.filter(parent__id=parent)
    person = Person.objects.get(id=parent)
    children = [d.child for d in duplicates]
    for c in children:
        records = PersonF.objects.filter(parent=c)
        records.delete()
    duplicates.delete()
    messages.error(
        request,
        "Removed {0} from duplicates.".format(person.name)
    )
    return redirect('website:persons')


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
