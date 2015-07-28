import logging
log = logging.getLogger(__name__)

from django.shortcuts import (
    render,
    redirect,
)

from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q

from apps.api.models import (
    Group,
    Song,
    Person,
    DuplicateGroup,
    DuplicateSong,
    DuplicatePerson,
)


def home(request):
    return render(
        request,
        'home.html',
    )


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


def remove_group(request, parent_id):
    parent = Group.objects.get(id=parent_id)
    if parent.kind == Group.QUARTET:
        r = redirect('website:quartets')
    else:
        r = redirect('website:choruses')
    duplicates = DuplicateGroup.objects.filter(
        Q(parent=parent) | Q(child=parent)
    )
    duplicates.delete()
    messages.error(
        request,
        "Removed {0} from duplicates.".format(parent.name)
    )
    return r


def merge_groups(request, parent_id, child_id):
    parent = Group.objects.get(id=parent_id)
    child = Group.objects.get(id=child_id)
    if parent.kind == 1:
        r = redirect('website:quartets')
    else:
        r = redirect('website:choruses')
    contestants = child.contestants.all()
    # move related records
    for contestant in contestants:
        contestant.group = parent
        try:
            contestant.save()
        except IntegrityError:
            messages.error(
                request,
                "Target {0} already exists.  Merge manually.".format(contestant),
            )
            duplicates = DuplicateGroup.filter(child=child)
            duplicates.delete()
            return r
    # once records are moved, remove redundant group
    try:
        child.delete()
    except Exception as e:
        raise RuntimeError("Error deleting old group: {0}".format(e))
    messages.success(
        request,
        "Merged {0} into {1}.".format(child, parent)
    )
    return r


def remove_song(request, parent_id):
    parent = Song.objects.get(id=parent_id)
    duplicates = DuplicateSong.objects.filter(
        Q(parent=parent) | Q(child=parent)
    )
    duplicates.delete()
    messages.error(
        request,
        "Removed {0} from duplicates.".format(parent.name)
    )
    return redirect('website:songs')


def merge_songs(request, parent_id, child_id):
    parent = Song.objects.get(id=parent_id)
    child = Song.objects.get(id=child_id)
    arrangements = child.arrangements.all()
    # move related records
    for arrangement in arrangements:
        arrangement.song = parent
        try:
            arrangement.save()
        except IntegrityError:
            messages.error(
                request,
                "Target {0} already exists.  Merge manually.".format(arrangement),
            )
            duplicates = DuplicateSong.filter(child=child)
            duplicates.delete()
            return redirect('website:songs')
    # once records are moved, remove redundant object
    try:
        child.delete()
    except Exception as e:
        raise RuntimeError("Error deleting old song: {0}".format(e))
    messages.success(
        request,
        "Merged {0} into {1}.".format(child, parent)
    )
    return redirect('website:songs')


def remove_person(request, parent_id):
    parent = Person.objects.get(id=parent_id)
    duplicates = DuplicatePerson.objects.filter(
        Q(parent=parent) | Q(child=parent)
    )
    duplicates.delete()
    messages.error(
        request,
        "Removed {0} from duplicates.".format(parent.name)
    )
    return redirect('website:persons')


def merge_persons(request, parent_id, child_id):
    parent = Person.objects.get(id=parent_id)
    child = Person.objects.get(id=child_id)
    quartets = child.quartets.all()
    choruses = child.choruses.all()
    arrangements = child.arrangements.all()

    # move related records
    for quartet in quartets:
        quartet.person = parent
        try:
            quartet.save()
        except IntegrityError:
            messages.error(
                request,
                "Target {0} already exists.  Merge manually.".format(quartet),
            )
            duplicates = DuplicatePerson.filter(child=child)
            duplicates.delete()
            return redirect('website:persons')
    for chorus in choruses:
        chorus.person = parent
        try:
            chorus.save()
        except IntegrityError:
            messages.error(
                request,
                "Target {0} already exists.  Merge manually.".format(chorus),
            )
            duplicates = DuplicatePerson.filter(child=child)
            duplicates.delete()
            return redirect('website:persons')
    for arrangement in arrangements:
        arrangement.person = parent
        try:
            arrangement.save()
        except IntegrityError:
            messages.error(
                request,
                "Target {0} already exists.  Merge manually.".format(arrangement),
            )
            duplicates = DuplicatePerson.filter(child=child)
            duplicates.delete()
            return redirect('website:persons')
    # once records are moved, remove redundant group
    try:
        child.delete()
    except Exception as e:
        raise RuntimeError("Error deleting old person: {0}".format(e))
    messages.success(
        request,
        "Merged {0} into {1}.".format(child, parent)
    )
    return redirect('website:persons')
