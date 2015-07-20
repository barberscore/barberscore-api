from django.shortcuts import (
    render,
    redirect,
)

from .models import (
    Collection,
    Duplicate,
)

from apps.api.models import (
    Group,
)


def home(request):
    return render(
        request,
        'home.html',
    )


def collections(request):
    collections = Collection.objects.all()
    return render(
        request,
        'collections.html',
        {'collections': collections},
    )


def collection(request, id):
    collection = Collection.objects.get(id=id)
    dups = []
    for d in collection.duplicates.all():
        g = Group.objects.get(id=d.source_id)
        dups.append(g)
    return render(
        request,
        'collection.html',
        {'collection': collection, 'dups': dups},
    )


def merge(request, id):
    keep = Duplicate.objects.get(source_id=id)
    collection = keep.collection
    parent = Group.objects.get(id=keep.source_id)
    orphans = collection.duplicates.exclude(source_id=id)
    for orphan in orphans:
        drop = Group.objects.get(id=orphan.source_id)
        for contestant in drop.contestants.all():
            contestant.group = parent
            contestant.save()
        drop.delete()
    collection.delete()
    return redirect('website:collections')
