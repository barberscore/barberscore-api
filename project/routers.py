class BHSRouter(object):
    """A router to control all database operations on models in the bhs application."""

    def db_for_read(self, model, **hints):
        """Attempt to read bhs models go to bhs_db, otherwise to default."""
        models = [
            'bhs.human',
            'bhs.structure',
            'bhs.status',
            'bhs.membership',
            'bhs.subscription',
            'bhs.role',
            'bhs.join',
        ]
        if model._meta.label_lower in models:
            return 'bhs_db'
        return None

    def db_for_write(self, model, **hints):
        """Attempt to write bhs models go to bhs_db, otherwise to default."""
        models = [
            'bhs.human',
            'bhs.structure',
            'bhs.status',
            'bhs.membership',
            'bhs.subscription',
            'bhs.role',
            'bhs.join',
        ]
        if model._meta.label_lower in models:
            return 'bhs_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Reject relations if a model in the bhs app is involved."""
        models = [
            'bhs.human',
            'bhs.structure',
            'bhs.status',
            'bhs.membership',
            'bhs.subscription',
            'bhs.role',
            'bhs.join',
        ]
        if (obj1._meta.label_lower in models) and (obj2._meta.label_lower not in models):
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Make sure the bhs app only appears in the 'bhs_db' database."""
        models = [
            'human',
            'structure',
            'status',
            'membership',
            'subscription',
            'role',
            'join',
        ]
        if app_label == 'bhs' and model_name in models:
            return False
        return None
