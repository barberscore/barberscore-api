# Django
from django.apps import apps
from django.db.models import Manager
from django.contrib.auth import get_user_model

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

        Organization = apps.get_model('organizations.organization')
        Session = apps.get_model('registration.session')
        legacy = Session.objects.filter(id=pk).first()

        # Session packaging changed by function below
        package_session = False
        if session['status'] == self.model.STATUS.packaged and legacy is not None and legacy.status is not self.model.STATUS.packaged:
            session['status'] = self.model.STATUS.verified
            package_session = True

        # remove id from dict
        if 'id' in session: del session['id']

        sess, created = self.update_or_create(
            id=pk,
            defaults=session,
        )

        # Add default owners
        if sess.organization:
            owners = sess.organization.default_owners
        else:
            if sess.district == Session.DISTRICT.hi:
                org = Organization.objects.filter(abbreviation="HI").first()
            else:
                org = Organization.objects.filter(abbreviation="BHS").first()
            owners = org.default_owners

        for owner in owners.all():
            sess.owners.add(owner.id)

        # Package Session ("build rounds")
        if package_session:
            sess.package()
            sess.save()

        return sess, created

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

        # Set any ADM/PC/CA on assignment to own both Convention and Session
        if record.session_id and record.category in [self.model.CATEGORY.adm, self.model.CATEGORY.pc]:

            # Get JWT User record
                # 1. record.email
            User = get_user_model()
            owner = User.objects.filter(email=record.email).first()

            # Session
            Session = apps.get_model('registration.session')
            session = Session.objects.filter(id=record.session_id).first()
            session.owners.add(owner.id)

            # Convention
            Convention = apps.get_model('bhs.convention')
            convention = Convention.objects.filter(id=session.convention_id).first()
            convention.owners.add(owner.id)

        return record, created

class EntryManager(Manager):
    def update_or_create_entry(self, entry):
        if not isinstance(entry, dict):
            raise ValueError("Must be dict")

        Organization = apps.get_model('organizations.organization')
        Session = apps.get_model('registration.session')

        pk = entry['id']

        # remove id from dict
        if 'id' in entry: del entry['id']

        record, created = self.update_or_create(
            id=pk,
            defaults=entry,
        )

        # Add default owners
        if record.session.organization:
            owners = record.session.organization.default_owners
        else:
            if record.session.district == Session.DISTRICT.hi:
                org = Organization.objects.filter(abbreviation="HI").first()
            else:
                org = Organization.objects.filter(abbreviation="BHS").first()
            owners = org.default_owners

        for owner in owners.all():
            record.owners.add(owner.id)

        return record, created

    def update_contestentry_status(self, sf_entry):
        entry_id = sf_entry['entry_id']
        contest_id = sf_entry['contest_id']

        Entry = apps.get_model('registration.entry')

        entry = Entry.objects.get(id=entry_id)

        if entry:
            if sf_entry['deleted']:
                entry.contests.remove(contest_id)
            else:
                entry.contests.add(contest_id)

        return entry