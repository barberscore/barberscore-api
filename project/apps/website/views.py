import logging
log = logging.getLogger(__name__)

from django.shortcuts import (
    render,
    redirect,
)

from fuzzywuzzy import process
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
        duplicates__isnull=False,
    ).filter(kind=Group.CHORUS).distinct().order_by('name')
    return render(
        request,
        'groups.html',
        {'groups': groups},
    )


def quartets(request):
    groups = Group.objects.filter(
        duplicates__isnull=False,
    ).filter(kind=Group.QUARTET).distinct().order_by('name')
    return render(
        request,
        'groups.html',
        {'groups': groups},
    )


def songs(request):
    songs = Song.objects.filter(
        duplicates__isnull=False,
    ).distinct().order_by('name')
    return render(
        request,
        'songs.html',
        {'songs': songs},
    )


def persons(request):
    persons = Person.objects.filter(
        duplicates__isnull=False,
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


def build_chorus(request):
    vs = Group.objects.filter(kind=Group.CHORUS).values('name')
    choices = [v['name'] for v in vs]
    gs = Group.objects.filter(kind=Group.CHORUS)
    for g in gs:
        matches = process.extract(g.name, choices)
        for match, score in matches:
            if score > 85 and score < 100:
                child = Group.objects.get(name=match)
                DuplicateGroup.objects.create(
                    parent=g,
                    child=child,
                    score=score,
                )
    messages.success(
        request,
        "Build complete.",
    )
    return redirect('website:choruses')


def build_quartet(request):
    vs = Group.objects.filter(kind=Group.QUARTET).values('name')
    choices = [v['name'] for v in vs]
    gs = Group.objects.filter(kind=Group.QUARTET)
    for g in gs:
        matches = process.extract(g.name, choices)
        for match, score in matches:
            if score > 85 and score < 100:
                child = Group.objects.get(name=match)
                DuplicateGroup.objects.create(
                    parent=g,
                    child=child,
                    score=score,
                )
    messages.success(
        request,
        "Build complete.",
    )
    return redirect('website:quartets')


def build_song(request):
    vs = Song.objects.values('name')
    choices = [v['name'] for v in vs]
    gs = Song.objects.all()
    for g in gs:
        matches = process.extract(g.name, choices)
        for match, score in matches:
            if score > 85 and score < 100:
                child = Song.objects.get(name=match)
                DuplicateSong.objects.create(
                    parent=g,
                    child=child,
                    score=score,
                )
    messages.success(
        request,
        "Build complete.",
    )
    return redirect('website:songs')


def build_person(request):
    vs = Person.objects.values('name')
    choices = [v['name'] for v in vs]
    gs = Person.objects.all()
    for g in gs:
        matches = process.extract(g.name, choices)
        for match, score in matches:
            if score > 85 and score < 100:
                child = Person.objects.get(name=match)
                DuplicatePerson.objects.create(
                    parent=g,
                    child=child,
                    score=score,
                )
    messages.success(
        request,
        "Build complete.",
    )
    return redirect('website:persons')
