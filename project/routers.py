class BHSRouter(object):
    """A router to control all database operations on models in the bhs application."""

    def db_for_read(self, model, **hints):
        """Attempt to read bhs models go to bhs_db."""
        if model._meta.app_label == 'bhs' and model._meta.model_name == 'person':
            return 'default'
        elif model._meta.app_label == 'bhs':
            return 'bhs_db'
        return None

    def db_for_write(self, model, **hints):
        """Attempt to write bhs models go to bhs_db."""
        if model._meta.app_label == 'bhs' and model._meta.model_name == 'person':
            return 'default'
        if model._meta.app_label == 'bhs':
            return 'bhs_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relations if a model in the bhs app is involved."""
        # if obj1._meta.app_label == 'bhs' or obj2._meta.app_label == 'bhs':
        #     return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Make sure the bhs app only appears in the 'bhs_db' database."""
        if app_label == 'bhs' and model_name == 'person':
            return True
        if app_label == 'bhs':
            return False
        return None
