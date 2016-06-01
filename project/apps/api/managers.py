# Django
from django.contrib.auth.models import BaseUserManager
from django.db.models import (
    Manager,
    Sum,
    QuerySet,
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


class ScoreQuerySet(QuerySet):
    def officials(self):
        return self.filter(
            kind=self.model.KIND.official,
        ).exclude(
            points=None,
        )


class ScoreManager(Manager):
    def get_queryset(self):
        return ScoreQuerySet(self.model, using=self._db)

    def official_totals(self):
        return self.get_queryset().officials().aggregate(
            s=Sum('points'))['s']
