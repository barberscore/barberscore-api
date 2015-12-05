from django.contrib.auth.models import (
    BaseUserManager,
)

from django.db import (
    models,
)

from django.db.models.query import (
    QuerySet,
)


class ContestantQuerySet(QuerySet):
    def accepted(self):
        return self.filter(
            status=self.model.STATUS.accepted,
        )

    def official(self):
        return self.filter(
            status=self.model.STATUS.official,
        )


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.model(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
