# Django
from django.apps import apps
from django.db.models import Manager

class ContestManager(Manager):
    def update_or_create_contest(self, contest):
        if not isinstance(contest, dict):
            raise ValueError("Must be dict")

        pk = contest['id']

        # remove id from dict
        if 'id' in contest: del contest['id']

        record, created = self.update_or_create(
            id=pk,
            defaults=contest,
        )
        return record, created

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

class AssignmentManager(Manager):
    def update_or_create_assignment(self, assignment):
        if not isinstance(assignment, dict):
            raise ValueError("Must be dict")

        pk = assignment['id']

        # remove id from dict
        if 'id' in assignment: del assignment['id']

        record, created = self.update_or_create(
            id=pk,
            defaults=assignment,
        )
        return record, created

class EntryManager(Manager):
    def update_or_create_entry(self, entry):
        if not isinstance(entry, dict):
            raise ValueError("Must be dict")

        pk = entry['id']

        # remove id from dict
        if 'id' in entry: del entry['id']

        record, created = self.update_or_create(
            id=pk,
            defaults=entry,
        )
        return record, created

    def update_contestentry_status(self, sf_entry):
        entry_id = sf_entry['entry_id']
        contest_id = sf_entry['contest_id']

        Entry = apps.get_model('registration.entry')

        entry = Entry.objects.get(pk=entry_id)

        if sf_entry['deleted']:
            entry.contests.remove(contest_id)
        else:
            entry.contests.add(contest_id)

        return entry