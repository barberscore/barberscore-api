# Django
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model


def get_owner_users():
    """Return the users dynamically assigned as default owners.

    Active staff users, minus the accounts listed in
    settings.CONVENTION_OWNERS_EXCLUDE.  This is the queryset behind
    settings.CONVENTION_OWNERS / settings.SESSION_OWNERS.
    """
    User = get_user_model()
    return User.objects.filter(
        is_staff=True,
        is_active=True,
    ).exclude(
        email__in=settings.CONVENTION_OWNERS_EXCLUDE,
    ).order_by(
        'email',
    )


def is_super_user(user):
    """Return True for users allowed to manage other users.

    Super users may set passwords, grant staff access, and designate
    other super users via the Django admin.  The bootstrap list lives in
    settings.SUPER_USERS; additional super users are designated in the
    admin (stored on User.app_metadata['is_superuser']).
    """
    if not getattr(user, 'is_authenticated', False):
        return False
    if not user.is_staff or not user.is_active:
        return False
    if user.email in settings.SUPER_USERS:
        return True
    app_metadata = user.app_metadata or {}
    return bool(app_metadata.get('is_superuser'))


def get_owner_targets():
    """Return querysets of the in-progress objects that track staff owners.

    Owners are only refreshed on objects still in flight; completed or
    inactive Conventions, Sessions, and Rounds keep their owners as an
    historical record.
    """
    Convention = apps.get_model('bhs.convention')
    Session = apps.get_model('registration.session')
    Round = apps.get_model('adjudication.round')
    return [
        Convention.objects.filter(
            status__in=[
                Convention.STATUS.new,
                Convention.STATUS.built,
                Convention.STATUS.active,
            ],
        ),
        Session.objects.filter(
            status__in=[
                Session.STATUS.new,
                Session.STATUS.built,
                Session.STATUS.opened,
            ],
        ),
        Round.objects.filter(
            status__in=[
                Round.STATUS.new,
                Round.STATUS.built,
                Round.STATUS.started,
            ],
        ),
    ]


def add_user_to_owners(user):
    """Add a newly-staffed user as owner of all in-progress objects."""
    if not user.is_active:
        return
    if user.email in settings.CONVENTION_OWNERS_EXCLUDE:
        return
    for queryset in get_owner_targets():
        for obj in queryset.exclude(owners=user):
            obj.owners.add(user)


def remove_user_from_owners(user):
    """Remove a de-staffed user as owner of all in-progress objects."""
    for queryset in get_owner_targets():
        for obj in queryset.filter(owners=user):
            obj.owners.remove(user)


def sync_owners():
    """Refresh owners of all in-progress objects from the staff list.

    Strictly additive: every dynamic owner (see get_owner_users) is
    added to every in-progress Convention, Session, and Round.  Owners
    added ad hoc are never touched; removal is only ever done for a
    specific user (see remove_user_from_owners), either by the staff
    signal or explicitly via the refresh_owners command.  Returns a list
    of (model_label, object_count, added) tuples.
    """
    owners = list(get_owner_users())
    results = []
    for queryset in get_owner_targets():
        added = 0
        count = 0
        for obj in queryset:
            count += 1
            current = set(obj.owners.values_list('pk', flat=True))
            for owner in owners:
                if owner.pk not in current:
                    obj.owners.add(owner)
                    added += 1
        results.append(
            (queryset.model._meta.label, count, added)
        )
    return results
