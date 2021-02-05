# Django
from django.apps import apps
from django.db.models import Manager

class SessionManager(Manager):
    def update_or_create_session(self, session):
        if not isinstance(session, dict):
            raise ValueError("Must be dict")

        pk = session['id']

        # remove id from dict
        if 'id' in session: del session['id']

        group, created = self.update_or_create(
            id=pk,
            defaults=session,
        )
        return group, created